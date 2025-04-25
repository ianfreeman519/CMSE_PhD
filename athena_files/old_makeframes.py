import os
import yt
import numpy as np
import matplotlib.pyplot as plt
import h5py
from mpl_toolkits.axes_grid1 import AxesGrid
import sys

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

if len(sys.argv) != 3:
    print("Usage: python makeframes.py <dictkey> <directoryname>")
    sys.exit(1)

dictkey = sys.argv[1]
directoryname = sys.argv[2]

basename = "recon_fast"
inputname = "athinput." + basename
fileseries = grabFileSeries(directoryname + "/", 6000, basename=basename)
ts = yt.DatasetSeries(fileseries)
for index in np.arange(100, 6000, 1, dtype=int):
    print(index, flush=True)
    time = get_simulation_time(fileseries[index])
    ds = ts[index]

    field = ("gas", "pressure")
    p = yt.SlicePlot(ds, "z", field) #, window_size=(8,6))

    # p.pan([np.sqrt(2)/8, 0.0])
    p.zoom(20)
    # p.set_zlim(field, zmin=1.8, zmax=2.8)

    p.annotate_streamlines(("gas", "magnetic_field_x"), ("gas", "magnetic_field_y"))
    
    # Plot a white box over the region I calculate energies
    xmin, xmax = -0.00625, 0.00625
    ymin, ymax = -0.027778, 0.027778
    p.annotate_line((xmin, ymin,0), (xmax, ymin,0), coord_system="data")
    p.annotate_line((xmax, ymin,0), (xmax, ymax,0), coord_system="data")
    p.annotate_line((xmax, ymax,0), (xmin, ymax,0), coord_system="data")
    p.annotate_line((xmin, ymax,0), (xmin, ymin,0), coord_system="data")

    p.annotate_title(f'Time t={time:.6f}, {dictkey}, {basename}')
    fig = p.export_to_mpl_figure((1,1))
    fig.savefig(f"figures/{dictkey}_x20_Xnull_{index:05}.png")
    plt.close(fig)
