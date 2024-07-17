import yt
yt.set_log_level(40)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import io
import time

# Paths and file settings
scratchPath = "/mnt/gs21/scratch/freem386/simple_magpinch_animation2/"
basename = "MPsimple"
f0, fn = 0, 200
step, width = 1, 5
files = [scratchPath + basename + ".out2." + str(f).zfill(width) + ".athdf" for f in np.arange(f0, fn+1, step, dtype=int)]

# Making timing list so estimates on completion can be calculated:
times = np.zeros(fn-f0+1)
times[:] = np.nan

# Load dataset series
ts = yt.DatasetSeries(files)
print("number of files: ", len(files), flush=True)

# Initialize an empty list to store frames as image buffers
frames = []

# Loop through indices
for index in range(len(files)):  # Ensure to loop over available datasets
    time0 = time.time()
    print("Writing index ", index, " \nEstimated time remaining: ", (fn-index)*np.nanmean(times), flush=True)
    ds = ts[index]
    fields = [
        ('athena_pp', 'vel1'), ('gas', 'magnetic_field_x'), ('gas', 'mach_number'), ('gas', 'pressure'),
        ('athena_pp', 'vel2'), ('gas', 'magnetic_field_y'), ('gas', 'density'), ('gas', 'specific_thermal_energy'),
        ('athena_pp', 'vel3'), ('gas', 'magnetic_field_z'), ('gas', 'magnetic_field_strength'), ('gas', 'magnetic_pressure')
    ]

    # Create a SlicePlot
    p = yt.SlicePlot(ds, "z", fields)

    # Export to a Matplotlib figure
    fig = p.export_to_mpl_figure((3, 4))
    fig.set_size_inches((16, 12))  # Resize the figure
    fig.suptitle(f"Timestep {str(index)}")

    # Adjust the layout
    fig.tight_layout(rect=[0, 0, 1, 1.0])  # Adjust rect to prevent overlap with suptitle
    fig.subplots_adjust(wspace=0.05, hspace=0.01)  # Set small values for minimal spacing

    # Iterate over each axis in the figure to modify the colorbar labels
    for ax, field in zip(fig.axes, fields):
        if hasattr(ax, 'images') and ax.images:
            img = ax.images[0]
            cbar = img.colorbar
            if cbar is not None:
                # Set the font size for the colorbar labels
                cbar.ax.tick_params(labelsize=8)
                # Set the custom label for the colorbar
                cbar.set_label(field[1], fontsize=14)

    # Save the figure to a buffer with increased DPI
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200)  # Increase DPI
    buf.seek(0)
    frames.append(np.array(plt.imread(buf)))
    buf.close()
    plt.close(fig)  # Close the figure to avoid displaying it
    times[index] = time.time() - time0

# Create an animation from frames
fig, ax = plt.subplots()
def update(frame):
    ax.clear()
    ax.imshow(frame)
    ax.axis('off')  # Turn off the axis

animation = FuncAnimation(fig, update, frames=frames, interval=500)  # 100 milliseconds per frame

# Save the animation as an mp4 with increased DPI
animation.save('simulation_animation.mp4', fps=2, dpi=400)  # Increase DPI for the animation
