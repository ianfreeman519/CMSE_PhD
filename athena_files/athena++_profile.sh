#!/bin/bash

module purge
module purge
module load GCC/10.3.0 
module load Conda/3 2> /dev/null
module load OpenMPI/4.1.1 
module load HDF5/1.10.7 
module load FFTW/3.3.9
module load powertools

conda activate research
