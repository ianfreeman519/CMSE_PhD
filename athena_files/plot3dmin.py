import yt
yt.set_log_level(40) 
import numpy as np
import pickle

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


def main():
    sim_size = (400, 400)
    full_pspace =  np.zeros((5, 5, 3, 3, 3, 300))
    for i1 in range(5):
        for i2 in range(5):
            for i3 in range(3):
                for i4 in range(3):
                    for i5 in range(3):
                        basename = f"al{i1}_be{i2}_p{i3}_d{i4}_b{i5}"
                        fileseries = grabFileSeries("lhlld_pspace2/", 300, basename=basename)
                        print(f"Working on {basename}")
                        for i in range(300):
                            print(i, end=" ")
                            try:
                                ds = yt.load(fileseries[i])
                            except:
                                break
                            cGrid = ds.all_data()
                            pGrid = np.array(cGrid["gas", "pressure"])
                            pGrid = np.reshape(pGrid, sim_size)
                            interior_pGrid = pGrid[150:250, 150:250]
                            full_pspace[i1, i2, i3, i4, i5, i] = np.min(interior_pGrid)
                            print(np.min(interior_pGrid))
    
    filename = "lhlld2_stability.pkl"
    filewriter = open(filename, 'wb')   
    pickle.dump(full_pspace, filewriter)
    print("dumped to file")
    filewriter.close()

main()
