import os
import numpy as np
import h5py
import yt
import re
from scipy.interpolate import CubicSpline
from pathlib import Path
from typing import Any, Dict

_block_re   = re.compile(r"<\s*([^>]+?)\s*>")     # captures whatever is between '<' and '>'
_comment_re = re.compile(r"#.*$")                 # strip inline comments

def collapse_refinement(arr1d, pos1d, epsilon=1e-8):
    """
    Collapse regions of constant values in a refined 1D dataset.

    Parameters
    ----------
    arr1d : ndarray
        1D array of values (e.g., field data).
    pos1d : ndarray
        1D array of corresponding positions.
    epsilon : float
        Threshold for considering two values different.

    Returns
    -------
    fout : list
        Collapsed field values.
    xout : list
        Mean position of each collapsed region.
    lout : list
        Length of each collapsed region in number of original cells.
    """
    if arr1d.shape != pos1d.shape:
        raise ValueError("arr1d and pos1d must have the same shape")

    fout, xout, lout = [], [], []
    istartblock = 0

    for i in range(len(arr1d) - 1):
        if np.abs(arr1d[i] - arr1d[i + 1]) > epsilon:
            fout.append(arr1d[i])
            xout.append(np.mean(pos1d[istartblock:i + 1]))
            lout.append(i + 1 - istartblock)
            istartblock = i + 1

    # Final block
    fout.append(arr1d[-1])
    xout.append(np.mean(pos1d[istartblock:]))
    lout.append(len(arr1d) - istartblock)

    return fout, xout, lout


def derivative1d_on_mesh(arr1d, pos1d, epsilon=1e-8):
    """
    Compute the derivative of a 1D function sampled at unevenly spaced points 
    using a cubic spline over collapsed refinement regions.

    Parameters
    ----------
    arr1d : ndarray
        The array of data values.
    pos1d : ndarray
        The positions corresponding to arr1d.
    epsilon : float, optional
        Tolerance used in collapse_refinement to identify flat regions.

    Returns
    -------
    deriv : ndarray
        The derivative of arr1d evaluated at pos1d.
    """
    fout, xout, lout = collapse_refinement(arr1d, pos1d, epsilon)
    cs = CubicSpline(xout, fout)
    return cs(pos1d, 1)

def dFdx_mesh(arr2d, pos1d, epsilon=1e-8):
    """
    Compute the partial derivative ∂F/∂x across a 2D array of values sampled 
    on a potentially uneven mesh in the x-direction (columns).

    Parameters
    ----------
    arr2d : ndarray
        2D array representing the function values on a 2D mesh.
    pos1d : ndarray
        1D array representing the physical x-positions of the columns.
    epsilon : float, optional
        Tolerance for identifying uniform regions in the refinement collapse.

    Returns
    -------
    dFdx : ndarray
        2D array of partial derivatives with respect to x.
    """
    dFdx = np.zeros_like(arr2d)
    for j in range(len(arr2d[0, :])):
        dFdx[:, j] = derivative1d_on_mesh(arr2d[:, j], pos1d, epsilon)
    return dFdx

def dFdy_mesh(arr2d, pos1d, epsilon=1e-8):
    """
    Compute the partial derivative ∂F/∂y across a 2D array of values sampled 
    on a potentially uneven mesh in the y-direction (rows).

    Parameters
    ----------
    arr2d : ndarray
        2D array representing the function values on a 2D mesh.
    pos1d : ndarray
        1D array representing the physical y-positions of the rows.
    epsilon : float, optional
        Tolerance for identifying uniform regions in the refinement collapse.

    Returns
    -------
    dFdy : ndarray
        2D array of partial derivatives with respect to y.
    """
    dFdy = np.zeros_like(arr2d)
    for i in range(len(arr2d[:, 0])):
        dFdy[i, :] = derivative1d_on_mesh(arr2d[i, :], pos1d, epsilon)
    return dFdy


def _current_eta_z(field, data):
    Jz = data["gas", "velocity_x"]*data["gas", "magnetic_field_y"] - data["gas", "velocity_y"]*data["gas", "magnetic_field_x"]
    return Jz
yt.add_field(
    name=("gas", "current_eta_z"),
    function=_current_eta_z,
    sampling_type="local",
    units="code_magnetic*code_velocity",
    force_override=True,
)

def dFdx_1d_non_U_grid(j, x):
    F = np.zeros_like(j)
    i = 0
    while i < len(F) and i != -1:
        ii = i
        while np.abs(j[ii] - j[i]) < 1e-6:
            ii = np.min([ii + 1, len(j)-1])
            # print(i, ii, np.min([ii + 1, len(j)]))
            f0 = j[i]
            if ii == len(j)-1:
                ii = -1
                break
        f1 = j[ii]
        dx = x[ii] - x[i]
        F[i:ii] = (f1 - f0) / dx
        i = ii
    return F

def dFdy_1d_non_U_grid(j, y):
    F = np.zeros_like(j)
    i = 0
    while i < len(F) and i != -1:
        ii = i
        while np.abs(j[ii] - j[i]) < 1e-6:
            ii = np.min([ii + 1, len(j)-1])
            # print(i, ii, np.min([ii + 1, len(j)]))
            f0 = j[i]
            if ii == len(j)-1:
                ii = -1
                break
        f1 = j[ii]
        dy = y[ii] - y[i]
        F[i:ii] = (f1 - f0) / dy
        i = ii
    return F

def rolling_average(f, a):
    out = np.copy(f)
    for idx, x in enumerate(f[a:-a]):
        i = idx + a
        out[i] = np.mean(f[i-a:i+a])
    return out
        

def div2D(Fx, Fy, dx, dy):
    return dFdx(Fx, dx) + dFdy(Fy, dy)

def dFdx(F, x):
    """
    Compute the derivative of F with respect to x, where x is a 1D array
    representing non-uniform grid positions along axis 0 (rows of F).

    Parameters:
    -----------
    F : np.ndarray
        2D array of shape (Nx, Ny)
    x : np.ndarray
        1D array of length Nx, giving grid positions along x-axis

    Returns:
    --------
    dFdx : np.ndarray
        Approximate derivative ∂F/∂x, same shape as F
    """
    Nx, Ny = F.shape
    dFdx = np.zeros_like(F)

    # Interior points: 3-point non-uniform central difference
    for i in range(1, Nx - 1):
        x0, x1, x2 = x[i-1], x[i], x[i+1]
        f0, f1, f2 = F[i-1], F[i], F[i+1]

        dx0 = x1 - x0
        dx1 = x2 - x1
        denom = dx0 * dx1 * (dx0 + dx1)

        # Coefficients derived from Lagrange interpolation polynomial
        a = -(2*dx1 + dx0) / (dx0 * (dx0 + dx1))
        b = (dx1 - dx0) / (dx0 * dx1)
        c = (2*dx0 + dx1) / (dx1 * (dx0 + dx1))

        dFdx[i, :] = a * f0 + b * f1 + c * f2

    # Forward difference at the first point
    dx = x[1] - x[0]
    dFdx[0, :] = (F[1, :] - F[0, :]) / dx

    # Backward difference at the last point
    dx = x[-1] - x[-2]
    dFdx[-1, :] = (F[-1, :] - F[-2, :]) / dx

    return dFdx
    
    
import numpy as np

def dFdy(F, y):
    """
    Compute the derivative of F with respect to y, where y is a 1D array
    representing non-uniform grid positions along axis 1 (columns of F).

    Parameters:
    -----------
    F : np.ndarray
        2D array of shape (Nx, Ny)
    y : np.ndarray
        1D array of length Ny, giving grid positions along y-axis

    Returns:
    --------
    dFdy : np.ndarray
        Approximate derivative ∂F/∂y, same shape as F
    """
    Nx, Ny = F.shape
    dFdy = np.zeros_like(F)

    # Interior points: 3-point non-uniform central difference
    for j in range(1, Ny - 1):
        y0, y1, y2 = y[j - 1], y[j], y[j + 1]
        dy0 = y1 - y0
        dy1 = y2 - y1
        denom = dy0 * dy1 * (dy0 + dy1)

        a = -(2 * dy1 + dy0) / (dy0 * (dy0 + dy1))
        b = (dy1 - dy0) / (dy0 * dy1)
        c = (2 * dy0 + dy1) / (dy1 * (dy0 + dy1))

        dFdy[:, j] = a * F[:, j - 1] + b * F[:, j] + c * F[:, j + 1]

    # Forward difference at the first column
    dy0 = y[1] - y[0]
    dFdy[:, 0] = (F[:, 1] - F[:, 0]) / dy0

    # Backward difference at the last column
    dy1 = y[-1] - y[-2]
    dFdy[:, -1] = (F[:, -1] - F[:, -2]) / dy1

    return dFdy



def draw_xy_box(p, xmin, xmax, ymin, ymax):
    """Draws a two dimensional box in the xy plane of an xy slice plot p
    
    Args:
        p (yt plot): plot to draw a box on
        xmin, ymin (floats): bottom left corner of box (coord_system="data")
        xmax, ymax (floats): top right corner of box (coord_system="data")
    """
    p.annotate_line((xmin, ymin,0), (xmax, ymin,0), coord_system="data")
    p.annotate_line((xmax, ymin,0), (xmax, ymax,0), coord_system="data")
    p.annotate_line((xmax, ymax,0), (xmin, ymax,0), coord_system="data")
    p.annotate_line((xmin, ymax,0), (xmin, ymin,0), coord_system="data")

def change_in_box(quantity, u, v, dx, dy, dz, dt):
    """Calculate the integral of the flux through a bounding box in the x- and y- direction

    Args:
        quantity (numpy.ndarray): 2D quantity to calculate flux through (e.g. Energy)
        u (numpy.ndarray): 2D x-velocity in the box
        v (numpy.ndarray): 2D y-velocity in the box
        dx (float): grid size in x-direction
        dy (float): grid size in y-direction
        dz (float): grid size in z-direction
        dt (float): timestep
    """
    # Left edge of the box:
    vn1 = u[0,:]    # velocity normal to edge at edge cell
    vn2 = u[0,:]    # velocity normal to edge next to edge
    vn = (vn1 + vn2)/2      # Average (at cell face, one cell inside the box)
    Q1 = quantity[0,:]      # Quantity at edge cell
    Q2 = quantity[1,:]      # Quantity next to edge
    Q = (Q1 + Q2)/2         # Average (at cell face, one cell inside the box)
    da = dy*dz              # da of edge
    flux = np.sum(vn*Q*da)     # quantity change per time into edge
    total_change_left = flux*dt     # total quantity *into* edge
    
    # Bottom edge of the box:
    vn1 = v[:,0]    # velocity normal to edge at edge cell
    vn2 = u[:,1]    # velocity normal to edge next to edge
    vn = (vn1 + vn2)/2      # Average (at cell face, one cell inside the box)
    Q1 = quantity[:,0]      # Quantity at edge cell
    Q2 = quantity[:,1]      # Quantity next to edge
    Q = (Q1 + Q2)/2         # Average (at cell face, one cell inside the box)
    da = dx*dz      # da of edge
    flux = np.sum(vn*Q*da)     # quantity change per time into edge
    total_change_bottom = flux*dt     # total quantity *into* edge
    
    # Top edge of the box:
    vn1 = v[:,-1]    # velocity normal to edge at edge cell
    vn2 = v[:,-2]    # velocity normal to edge next to edge
    vn = (vn1 + vn2)/2      # Average (at cell face, one cell inside the box)
    Q1 = quantity[:,-1]      # Quantity at edge cell
    Q2 = quantity[:,-2]      # Quantity next to edge
    Q = (Q1 + Q2)/2         # Average (at cell face, one cell inside the box)
    da = dx*dz      # da of edge
    flux = np.sum(vn*Q*da)     # quantity change per time into edge
    total_change_top = flux*dt     # total quantity *into* edge
    
    # Right edge of the box:
    vn1 = u[-1,:]    # velocity normal to edge at edge cell
    vn2 = u[-2,:]    # velocity normal to edge next to edge
    vn = (vn1 + vn2)/2      # Average (at cell face, one cell inside the box)
    Q1 = quantity[-1,:]      # Quantity at edge cell
    Q2 = quantity[-2,:]      # Quantity next to edge
    Q = (Q1 + Q2)/2         # Average (at cell face, one cell inside the box)
    da = dy*dz      # da of edge
    flux = np.sum(vn*Q*da)     # quantity change per time into edge
    total_change_right = flux*dt     # total quantity *into* edge
    
    # Notice the sign for the right and top edge, because those da point INTO the box, i.e. -x, -y at right and top
    return total_change_bottom + total_change_left - total_change_right - total_change_top


import h5py

def get_simulation_time(hdf5_file):
    """
    Extracts the simulation time from an Athena++ or AthenaPK HDF5 output file.

    Parameters:
    ----------
    hdf5_file : str
        Path to the HDF5 file.

    Returns:
    -------
    float or None
        The simulation time if found, or None if the time is not available or an error occurs.
    """
    try:
        with h5py.File(hdf5_file, 'r') as hdf:
            # Try root-level attribute (Athena++)
            if 'Time' in hdf.attrs:
                return hdf.attrs['Time']
            # Try 'Info' group attribute (AthenaPK)
            elif 'Info' in hdf and 'Time' in hdf['Info'].attrs:
                return hdf['Info'].attrs['Time']
            else:
                print(f"'Time' attribute not found in root or 'Info' group: {hdf5_file}.")
    except Exception as e:
        print(f"Error while reading HDF5 file '{hdf5_file}': {e}")
    
    return None


def parse_input_file(filename: str | Path) -> Dict[str, Any]:
    """
    Parse an Athena++/Athena-PK style input file.

    Returns
    -------
    dict
        Keys are "<block>_<variable>" (both lower-cased, no spaces),
        values are int, float, or str depending on what parses cleanly.
    """
    params: Dict[str, Any] = {}
    current_block = "global"                      # fallback for lines outside any block

    with open(filename, "r") as fp:
        for raw in fp:
            line = _comment_re.sub("", raw).strip()   # drop comments, whitespace
            if not line:
                continue                             # blank line → skip

            # ─── Block header? ─────────────────────────────────────────────
            block_match = _block_re.fullmatch(line)
            if block_match:
                current_block = block_match.group(1).strip().lower()
                continue

            # ─── key = value line? ────────────────────────────────────────
            if "=" not in line:
                continue                             # ignore lines with no '='

            var, val = (x.strip() for x in line.split("=", 1))

            # best-effort numeric conversion
            try:
                # int() will also parse hex/octal if prefixed (0x, 0o, 0b)
                val_parsed: Any = int(val, 0)
            except ValueError:
                try:
                    val_parsed = float(val)
                except ValueError:
                    val_parsed = val                       # keep raw string

            key = f"{current_block}_{var}".lower()
            params[key] = val_parsed

    return params

def grabFileSeries(
    scratchdirectory,
    fn=None,
    basename="output_name",
    f0=0,
    step=1,
    width=5,
    scratchPath="/mnt/gs21/scratch/freem386/",
    outputnum="out2",
    extension="athdf"
):
    """
    Generate a list of file paths for a series of Athena++ .athdf files.

    If `fn` is None, attempts to discover the largest index in the directory by
    matching any file that follows the pattern:
        {basename}.{outputnum}.{index}.athdf

    Parameters
    ----------
    scratchdirectory : str
        Name of the scratch directory where the files are located.
    fn : int or None, optional
        The final index for the series. If None, automatically discovers the
        largest index from existing files in the directory. Default is None.
    basename : str, optional
        The base name of the files (e.g., "mySimulation"). Default is "mySim".
    f0 : int, optional
        The starting index for the series. Default is 0.
    step : int, optional
        The step size between successive indices. Default is 1.
    width : int, optional
        The number of digits to which the index is zero-padded. Default is 5.
    scratchPath : str, optional
        The full path to the scratch directory. Default is "/mnt/gs21/scratch/freem386/".
    outputnum : str, optional
        The output identifier that appears in the file name (e.g., "out2"). Default is "out2".
    extension : str, optional
        the output extension

    Returns
    -------
    list of str
        A list of file paths matching the specified pattern, each ending with "extension".
    """
    
    # If fn is None, find the max index by scanning the directory for matching files
    if fn is None:
        dir_path = os.path.join(scratchPath, scratchdirectory)
        # Regex to match files like basename.out2.00000.athdf (with variable width)
        pattern = rf"^{re.escape(basename)}\.{re.escape(outputnum)}\.(\d+)\.{extension}$"

        max_index = None
        if os.path.isdir(dir_path):
            for fname in os.listdir(dir_path):
                match = re.match(pattern, fname)
                if match:
                    idx = int(match.group(1))
                    if max_index is None or idx > max_index:
                        max_index = idx

        if max_index is None:
            # If no matching files are found, you can decide to raise an error,
            # return an empty list, or default to 0. Here we raise an error:
            raise FileNotFoundError(
                f"No files matching the pattern '{basename}.{outputnum}.*.athdf' were found "
                f"in directory '{dir_path}'. Cannot determine largest index."
            )

        fn = max_index

    # Now generate the list of files from f0 up to and including fn
    files = []
    for f in np.arange(f0, fn + 1, step, dtype=int):
        filename = (
            scratchPath
            + scratchdirectory
            + basename
            + "."
            + outputnum
            + "."
            + str(f).zfill(width)
            + "."
            + extension
        )
        files.append(filename)

    return files