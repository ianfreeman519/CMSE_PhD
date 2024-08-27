import h5py
from mpi4py import MPI
import numpy as np
import pickle

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

pressure_min = np.zeros((5, 5, 3, 3, 3, 300))

directory = "/mnt/gs21/scratch/freem386/lhlld_pspace2/"

al_max, be_max, p_max, d_max, b_max = 5, 5, 3, 3, 3
t_max = 300
window_min, window_max = 150, 250

for i1 in range(al_max): # Iterate through alpha values
    for i2 in range(be_max): # Iterate through beta values
        for i3 in range(p_max): # Iterate through pressure coefficients
            for i4 in range(d_max): # Iterate through density coefficients
                for i5 in range(b_max): # Iterate through magnetic coefficients
                    if rank == 0:   # Diagnostic information for slurm
                        print(f"Working on loop {i1+1}/{al_max}, {i2+1}/{be_max}, {i3+1}/{p_max}, {i4+1}/{d_max}, {i5+1}/{b_max}", flush=True)
                    index_list = np.arange(0, t_max, 1, dtype=int)
                    for i in index_list[rank::size]: # Iterate through timesteps
                        filename = f"al{i1}_be{i2}_p{i3}_d{i4}_b{i5}.out2." + str(i).zfill(5) + ".athdf"
                        try:
                            fileh5 = h5py.File(directory + filename)
                            dset = fileh5['prim']
                            pressure_min[i1, i2, i3, i4, i5, i] = np.min(dset[1, 0, 0, window_min:window_max, window_min:window_max])
                            fileh5.close()
                        except:
                            pressure_min[i1, i2, i3, i4, i5, i] = np.nan
                            fileh5.close()

summed_array = np.zeros_like(pressure_min)

comm.Reduce(pressure_min, summed_array, op=MPI.SUM, root=0)

if rank == 0:
    filewriter = open("lhlld2_stability.pkl", 'wb')   
    pickle.dump(summed_array, filewriter)
    filewriter.close()
