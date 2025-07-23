import os
import re
import numpy as np
import h5py
import yt
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

print(yt.__version__)
os.system("python --version")
yt.set_log_level(50)        


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


def get_simulation_time(hdf5_file):
    """
    Extracts the simulation time from an Athena++ HDF5 output file.

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
            # Check if the 'Time' attribute exists at the root
            if 'Time' in hdf.attrs:
                return hdf.attrs['Time']
            else:
                print(f"'Time' attribute not found at the root of the HDF5 file: {hdf5_file}.")
    except Exception as e:
        print(f"Error while reading HDF5 file '{hdf5_file}': {e}")
    
    return None


def parse_input_file(filename):
    # Initialize variables to None
    P0 = None
    rho0 = None
    v0 = None
    b0 = None
    L = None
    
    # Open and read the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Look for the relevant lines
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("P0"):
            P0 = float(stripped_line.split('=')[1].strip())
        elif stripped_line.startswith("rho0"):
            rho0 = float(stripped_line.split('=')[1].strip())
        elif stripped_line.startswith("v0"):
            v0 = float(stripped_line.split('=')[1].strip())
        elif stripped_line.startswith("b0") or stripped_line.startswith("d\t"):  # Match only if 'd' is followed by space or tab
            b0 = float(stripped_line.split('=')[1].strip())
        elif stripped_line.startswith("L"):
            L = float(stripped_line.split('=')[1].strip())
    
    return P0, rho0, v0, b0, L


def grabFileSeries(
    scratchdirectory,
    fn=None,
    basename="output_name",
    f0=0,
    step=1,
    width=5,
    scratchPath="/mnt/gs21/scratch/freem386/",
    outputnum="out2"
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

    Returns
    -------
    list of str
        A list of file paths matching the specified pattern, each ending with ".athdf".
    """
    
    # If fn is None, find the max index by scanning the directory for matching files
    if fn is None:
        dir_path = os.path.join(scratchPath, scratchdirectory)
        # Regex to match files like basename.out2.00000.athdf (with variable width)
        pattern = rf"^{re.escape(basename)}\.{re.escape(outputnum)}\.(\d+)\.athdf$"

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
            + ".athdf"
        )
        files.append(filename)

    return files

directoryDict = {'rh1': 'recon_harris1/', 'rw1': 'recon_wire1/', 'rh2': 'recon_harris2/',
                 'rh3': 'recon_harris3/', 'rg1': 'recon_GEM1/', 'rb1': 'recon_bhat1/', 
                 'rb2': 'recon_bhat2/', 'rb3': 'recon_bhat3/',
                 'rf1': 'recon_freem1/', 'rf2': 'recon_freem2/', 'rf3': 'recon_freem3/',
                 'rf4': 'recon_freem4/', 'rf5': 'recon_freem5/', 'rf6': 'recon_freem6/',
                 'rf7': 'recon_freem7/', 'rf8': 'recon_freem8/',
                 'np0': 'non_periodic_test/', 'np2': 'non_periodic_test2/',
                 'rs1': 'recon_fast1/', 'rs2': 'recon_fast2/', 'rs3': 'recon_fast3/',
                 'rs4': 'recon_fast4/', 'rs6': 'recon_fast6/',
                 'rt1': 'recon_test1/', 'rt2': 'recon_test2/', 'rt3': 'recon_test3/', 'rt4': 'recon_test4/',
                 'rt5': 'recon_test5/', 'rt6': 'recon_test6/', 'rt7': 'recon_test7/', 'rt8': 'recon_test8/',
                 'st3': 'scaling_test_e3/', 'st5': 'scaling_test_e5/', 'st7': 'scaling_test_e7/',
                 }

## Plotting a list of datasets
for index in range(2000):
    print(index/2000)
    dictkey, basename = "np2", "recon_fast"
    inputname = "athinput." + basename
    fileseries = grabFileSeries(directoryDict[dictkey], index, basename=basename)# , outputnum="out3")
    ts = yt.DatasetSeries(fileseries)
    time = get_simulation_time(fileseries[index])
    ds = ts[index]

    field = ('gas', 'pressure')
    p = yt.SlicePlot(ds, "z", field) #, window_size=(8,6))

    p.zoom(2)
    p.set_figure_size(12)
    # p.pan((1,0))
    # xmin, xmax, ymin, ymax = -0.00625, 0.00625, -0.027778, 0.027778
    # draw_xy_box(p, xmin, xmax, ymin, ymax)

    # p.annotate_velocity()
    p.annotate_streamlines(("gas", "magnetic_field_x"), ("gas", "magnetic_field_y"))

    p.set_log(field, False)
    # p.annotate_grids()

    p.annotate_title(f'Time t={time:.6f}, {dictkey}, {basename}')
    # xrange, yrange = 1, 0.1
    fig = p.export_to_mpl_figure((1,1))
    # fig.set_size_inches(20,12)
    # fig.axes[0].set_ylim(-yrange,yrange)
    # fig.axes[0].set_xlim(-xrange,xrange)
    # fig.axes[0].set_box_aspect(0.333)
    fig.savefig(f"figures/{dictkey}_t{str(index).zfill(5)}_full.png")