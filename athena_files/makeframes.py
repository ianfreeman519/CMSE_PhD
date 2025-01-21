import os
import yt
import numpy as np
import matplotlib.pyplot as plt
import h5py
from mpl_toolkits.axes_grid1 import AxesGrid
from utils import grabFileSeries

print(yt.__version__)
os.system("python --version")
yt.set_log_level(50)        
"""
Possible values of set_log_level by increasing level:
        0 or "notset"
        1 or "all"
        10 or "debug"
        20 or "info"
        30 or "warning"
        40 or "error"
        50 or "critical"
"""

# To parse input files for parameters
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


# Start with plotting a single dataset
index = 0
dictkey = "rf2"
basename = "recon_freem"
inputname = "athinput." + basename       # MagNoh2 for most problems
fileseries = grabFileSeries("recon_freem3/", index, basename=basename )# , outputnum="out3")
print(fileseries[index])
ts = yt.DatasetSeries(fileseries)
outputfreq = 10
