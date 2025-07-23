import yt
yt.set_log_level(50)  
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import trange
from utils import grabFileSeries, get_simulation_time, change_in_box
from utils import draw_xy_box, parse_input_file, div2D, dFdx, dFdy, rolling_average, fill_zeros_with_previous

# Calculating aspect ratio of force-free sheet
# Standard dataset initialization
max_index = 120
scratch_dirname = "forcetest/"
# scratch_dirname = "forcetest/"
inputname = "athinput.recon_gauss_harris"
input_params = parse_input_file(f'/mnt/gs21/scratch/freem386/{scratch_dirname}{inputname}')
fileseries = grabFileSeries(scratch_dirname, max_index, basename="recon_fast")
ts = yt.DatasetSeries(fileseries)

# Actually fitting the data:
def funcg(x, A, mu, sig, c):
    return A*np.exp(-((x-mu)/sig)**2) + c
print(f"time, 1sd gauss rho, J length, Bfrac length, current L/d, Bfrac L/d, v_A\t, mach_A_in", flush=True)

for index in range(10, max_index):
    time = get_simulation_time(fileseries[index])
    ds = ts[index]

    # Casting yt data into numpy data to analyze
    # Defining analysis box limits (in code units of x and y)
    xminbox, xmaxbox = -0, 1.2
    yminbox, ymaxbox = -0.5, 0.5

    # Creating the covering grid using YT to cast yt data
    level = input_params["refinement1_level"]   # Max refinement level - highest resolution needed for numpy array
    Nx = input_params["mesh_nx1"] * 2**(level)  # Nx, Ny is the number of cells in each direction of the WHOLE simulation domain
    Ny = input_params["mesh_nx2"] * 2**(level)
    xmin, xmax = input_params["mesh_x1min"], input_params["mesh_x1max"] # This is the dimension of the WHOLE simulation domain
    ymin, ymax = input_params["mesh_x2min"], input_params["mesh_x2max"]
    dx, dy = (xmax - xmin)/Nx, (ymax - ymin)/Ny     # grid resolution at highest refinement level
    i0, j0 = int(np.floor((xminbox -  xmin  )//dx)), int(np.floor((yminbox -  ymin  )//dy))     # Index for starting x and y positions within the covering grid
    iN, jN = int(np.floor((xmaxbox - xminbox)//dx)), int(np.floor((ymaxbox - yminbox)//dy))   # Length of the covering grid data in x/y

    # Finally the real covering grid:
    cg = ds.covering_grid(level=level, left_edge=[xminbox, yminbox, 0], dims=[iN, jN, 1])
    # Grabbing mesh information using numpy
    X, Y = np.reshape(cg["athena_pp","x"].v, (iN, jN)), np.reshape(cg["athena_pp","y"].v, (iN, jN))
    x = X[:,0]
    y = Y[0,:]

    # Now grab relevant fluid quantities (sliced along x, y, then reducing dimension with [...,0], elminating YT units with .v)
    vx = cg["gas", "velocity_x"][:,:,0].v
    vy = cg["gas", "velocity_y"][:,:,0].v
    Bx = cg["gas", "magnetic_field_x"][:,:,0].v
    By = cg["gas", "magnetic_field_y"][:,:,0].v
    vA = cg["gas", "alfven_speed"][:,:,0].v
    rho =cg["gas", "density"][:,:,0].v

    # Ez = u x B = eta*Jz, so current is:
    J = (vx*By - vy*Bx) / input_params["problem_eta_ohm"]

    # By / |B|
    B = np.sqrt(Bx*Bx + By*By)
    B_ratio = By**2 / B**2 - Bx**2 / B**2
    
    # find width of sheet from current:
    i = 0
    while i <= iN:
        if np.abs(J[i, jN//2]) > 1000:     # arbitrary threshold to determine nonzero current
            current_L = X[i, jN//2]
            i += iN     # This should kill the loop
        else:
            current_L = 0   # TODO figure out better handling
        i += 1
    
    # find width of sheet from B ratios
    i = 0
    while i <= iN:
        if B_ratio[i, jN//2] > 0:
            Bratio_L = X[i, jN//2]
            i += iN
        else:
            Bratio_L = 0
        i += 1
    
    # find the height of sheet using density fwhm
    rho_slice = rho[0,:]
    param_boundsg = ([-np.inf, -1, 0, -np.inf], [np.inf, 1, np.inf, np.inf])
    poptg, pcovg = curve_fit(funcg, y, rho_slice, bounds=param_boundsg, maxfev=1e7)
    sig = poptg[2]
    dens_d = sig / 2 # FWHM of gaussian (divided by 2 - consistent with N&L 2011)
    index_d = int(dens_d / dx + jN / 2)
    
    aspect_current = current_L / dens_d
    aspect_Bratio  = Bratio_L / dens_d
    mach_A_in = np.sqrt(vy[0, index_d]**2 + vx[0, index_d]**2) / vA[0, index_d]
    
    print(f"{time:.5f}, {dens_d:.6f}, {current_L:.6f}, {Bratio_L:.6f}, {aspect_current:.6e}, {aspect_Bratio:.6e}, {vA[0, index_d]:.6e}, {mach_A_in:.6e}", flush=True)
    