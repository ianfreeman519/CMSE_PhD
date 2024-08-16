import yt
import numpy as np

def grabFileSeries(scratchdirectory, fn, f0=0, step=1, width=5, 
                   basename="MPsimple", scratchPath="/mnt/gs21/scratch/freem386/"):
    """Returns a list of files with the form 
    <scratchPath>/<scratchdirectory>/<basename>.out2/#####.athdf,
    starting at f0, ending at fn with stepsize step.

    Args:
        scratchdirectory (str): Directory within scratchPath of desired files
        fn (int): final (stopping point) output number
        f0 (int, optional): initial output number. Defaults to 0.
        step (int, optional): output number step. Defaults to 1.
        width (int, optional): width of 0 in filenames. Defaults to 5.
        basename (str, optional): <basename>.out2.#####.athdf . Defaults to "MPsimple".
        scratchPath (str, optional): value stored in $SCRATCH. Defaults to "/mnt/gs21/scratch/freem386/".

    Returns:
        array[str]: List of filenames including paths
    """
    files = []
    for f in np.arange(f0, fn+1, step, dtype=int):
            files.append(scratchPath + scratchdirectory + basename + ".out2." + str(f).zfill(width) + ".athdf")
    return files

def grabAllData(filename):
    """Returns a covering grid of filename at AMR level 0

    Args:
        filename (str): Full path of desired file

    Returns:
        yt.covering_grid: AMR level 0 covering grid of filename
    """
    ds = yt.load(filename)
    max_level = ds.index.max_level      # Max AMR level - included for if AMR is turned on later
    low = ds.domain_left_edge           # Domain left edge for numpy conversion starting region
    dims = ds.domain_dimensions         # Dimensions of full domain
    all_data_level_0 = ds.covering_grid(level=max_level, left_edge=low, dims=dims)
    return all_data_level_0

def main():
    fileseries = grabFileSeries("roe_pspace1/", 300, basename="al0_be1_p1_d1_b1")
    cGrid = grabAllData(fileseries[20])
    pGrid = np.array(cGrid["gas", "pressure"])

    print(np.any(pGrid < 1e-10))
    
    cGrid = grabAllData(fileseries[0])
    pGrid = np.array(cGrid["gas", "pressure"])
    print(np.any(pGrid < 1e-10))
    
main()
