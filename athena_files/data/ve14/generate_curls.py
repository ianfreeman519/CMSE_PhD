import yt
yt.set_log_level(50)  
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
sys.path.append('/mnt/home/freem386/CMSE_PhD/athena_files')
from utils import grabFileSeries, get_simulation_time
from utils import parse_input_file
from utils import dFdx_1d_non_U_grid, dFdy_1d_non_U_grid, dFdx_mesh, dFdy_mesh
import pickle as pkl
import gc

for index in range(200):
    print(f"{index / 2}% complete", end="\t", flush=True)
    # Standard dataset initialization
    scratch_dirname = "vary_eta_force_free_IC/1e-7/"
    # scratch_dirname = "forcetest/"
    inputname = "athinput.recon_gauss_harris"
    input_params = parse_input_file(f'/mnt/gs21/scratch/freem386/{scratch_dirname}{inputname}')
    fileseries = grabFileSeries(scratch_dirname, index, basename="recon_fast")
    ts = yt.DatasetSeries(fileseries)
    time = get_simulation_time(fileseries[index])
    ds = ts[index]
    
    print("Loading data", end="\t", flush=True)
    # Casting yt data into numpy data to analyze
    # Defining analysis box limits (in code units of x and y)
    xminbox, xmaxbox = -1.2, 1.2
    yminbox, ymaxbox = -0.1, 0.1

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
    vx = cg["gas", "velocity_x"][:,:,0]
    vy = cg["gas", "velocity_y"][:,:,0]
    Bx = cg["gas", "magnetic_field_x"][:,:,0]
    By = cg["gas", "magnetic_field_y"][:,:,0]
    vA = cg["gas", "alfven_speed"][:,:,0]
    rho =cg["gas", "density"][:,:,0]

    # Ez = u x B = eta*Jz, so current is:
    J = (vx*By - vy*Bx) / input_params["problem_eta_ohm"]

    # Plotting velocity instead
    # J = np.sqrt(vx**2+vy**2)
    # J = np.sqrt(Bx**2+By**2)

    # By / |B|
    # B = np.sqrt(Bx*Bx + By*By)
    # J = By**2 / B**2 - Bx**2 / B**2

    print("Calculating Curls", end="\t", flush=True)
    dBydx = dFdx_mesh(By, x)
    dBxdy = dFdy_mesh(Bx, y)
    curlB = dBydx - dBxdy
    field = curlB
    
    print("Plotting", end="\t", flush=True)
    plt.clf() # Found to be effective to get rid of weird plots floating around

    # Four total subplots (bottom right is deleted), largest in the top left, and thin on the right column and bottom row
    gs_kw = dict(width_ratios=[1.0, 0.25, 0.25], height_ratios=[1.0, 0.5, 0.5])    # Gridspec (gs) keywords for defining subplots
    fig, ax = plt.subplots(3, 3, gridspec_kw=gs_kw, layout='constrained')
    fig.delaxes(ax[1,1]); fig.delaxes(ax[1,2]); fig.delaxes(ax[2,1]); fig.delaxes(ax[2,2]) # Delete unused axis (bottom right)

    # current colormesh, colorbar, magnetic field streamplot (top left plot)
    p1 = ax[0,0].pcolormesh(X, Y, np.abs(field), norm=colors.LogNorm())
    cbar = plt.colorbar(p1, location="top", pad=0)
    ax[0,0].streamplot(x, y, Bx.T, By.T, color="gray")
    # ax[0,0].contour(X, Y, field, colors="black", levels=50)
    cbar.ax.set_ylabel(f"current (code units)", rotation=0, loc="top")
    ax[0,0].set_ylabel(f"y (code units) | res={Y.shape[1]}")

    # y=0 slice (middle bottom left plot)
    ax[1,0].plot(X[:,jN//2], field[:,jN//2])
    ax[1,0].set_ylabel(f"|current| (code units) along y=0")
    # ax[1,0].set_yscale("log")

    # y=0 x-derivative (bottom left)
    ax[2,0].plot(X[:,jN//2], dFdx_1d_non_U_grid(field[:,jN//2], x))
    ax[2,0].set_ylabel(f"|dJ/dx| (code units) along y=0")
    ax[2,0].set_xlabel(f"x (code units) | resolution={X.shape[0]}")
    # ax[2,0].set_yscale("log")

    # x=0 slice (middle top right)
    ax[0,1].plot(field[iN//2,:], Y[iN//2,:])
    ax[0,1].set_xlabel(f"current (code units) along x=0")

    # x=0 y-derivative (top right)
    ax[0,2].plot(dFdy_1d_non_U_grid(field[iN//2,:], y), Y[iN//2,:])
    ax[0,2].set_xlabel(f"dJdy (code units) along x=0")

    # Force axes to match:
    for i in range(3): ax[i, 0].set_xlim(xminbox, xmaxbox)
    for j in range(3): ax[0, j].set_ylim(yminbox, ymaxbox)

    # Supertitle
    fig.suptitle(f"{scratch_dirname}, t={time:.6f}", fontsize=24)
    fig.set_size_inches(20, 10)
    
    print("Saving & Cleaning up memory", flush=True)
    
    fig.savefig(f"plot_{index:05}.png")
    
    # Cleaning up memory:
    del ds, X, Y, x, y, rho, Bx, By, dBxdy, dBydx, J, curlB, vA, vx, vy
    plt.close(fig)
    gc.collect()