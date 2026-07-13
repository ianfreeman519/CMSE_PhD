from matplotlib.colors import LogNorm
from utils import grabFileSeries
import yt
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------
basename = "parthenon"
output_type = "out0"
scratch_dir = "pulsed_recon/a_rk12/"

fileseries = grabFileSeries(
    scratch_dir,
    basename=basename,
    outputnum=output_type,
    extension="phdf",
)

for i in range(250, 450):
    ds = yt.load(fileseries[i])

    field = ("parthenon", "prim_pressure")

    # ------------------------------------------------------------
    # Desired plotting region
    # ------------------------------------------------------------
    x_min, x_max = -0.0, 3.0
    y_min, y_max = -0.05, 0.35

    y_line = 0.15

    x_center = 0.5 * (x_min + x_max)
    y_center = 0.5 * (y_min + y_max)

    x_width = x_max - x_min
    y_width = y_max - y_min

    # Use the center of the z domain
    z_slice = ds.domain_center[2]

    # FRB resolution
    nx = 800
    ny = 400

    # ------------------------------------------------------------
    # Create yt slice and fixed-resolution buffer
    # ------------------------------------------------------------
    slc = ds.slice("z", z_slice)

    frb = slc.to_frb(
        width=ds.arr([x_width, y_width], "code_length"),
        resolution=(nx, ny),
        center=ds.arr(
            [x_center, y_center, z_slice.to_value("code_length")],
            "code_length",
        ),
    )

    pressure_image = frb[field].to_value()

    # yt should return the array as (ny, nx). Correct it if needed.
    if pressure_image.shape == (nx, ny):
        pressure_image = pressure_image.T

    if pressure_image.shape != (ny, nx):
        raise RuntimeError(
            f"Unexpected FRB shape {pressure_image.shape}; "
            f"expected {(ny, nx)}."
        )

    # ------------------------------------------------------------
    # Coordinates of FRB pixel centers
    # ------------------------------------------------------------
    dx = x_width / nx
    dy = y_width / ny

    x = np.linspace(
        x_min + 0.5 * dx,
        x_max - 0.5 * dx,
        nx,
    )

    y = np.linspace(
        y_min + 0.5 * dy,
        y_max - 0.5 * dy,
        ny,
    )

    # ------------------------------------------------------------
    # Extract the row nearest y_line
    # ------------------------------------------------------------
    iy = np.argmin(np.abs(y - y_line))
    actual_y = y[iy]

    pressure_line = pressure_image[iy, :]

    valid_line = (
        np.isfinite(x)
        & np.isfinite(pressure_line)
        & (pressure_line > 0.0)
    )

    x_line = x[valid_line]
    pressure_line = pressure_line[valid_line]

    if pressure_line.size == 0:
        raise RuntimeError(
            f"No finite positive pressure values found near y={actual_y}."
        )

    # ------------------------------------------------------------
    # Logarithmic color limits
    # ------------------------------------------------------------
    valid_image = pressure_image[
        np.isfinite(pressure_image) & (pressure_image > 0.0)
    ]

    if valid_image.size == 0:
        raise RuntimeError(
            "The selected slice contains no finite positive pressure values."
        )

    vmin = valid_image.min()
    vmax = valid_image.max()

    # ------------------------------------------------------------
    # Create side-by-side figure
    # ------------------------------------------------------------
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(14, 5),
        constrained_layout=True,
    )

    # ------------------------------------------------------------
    # Left: lineout
    # ------------------------------------------------------------
    ax[0].plot(
        x_line,
        pressure_line,
        linewidth=1.5,
    )

    ax[0].set_yscale("log")
    ax[0].set_xlim(x_min, x_max)

    ax[0].set_title(
        rf"prim_pressure along $x$ at $y={actual_y:.5f}$"
    )

    ax[0].set_xlabel("x (code length)")
    ax[0].set_ylabel("prim_pressure (code units)")
    ax[0].grid(True, which="both", alpha=0.25)

    # ------------------------------------------------------------
    # Right: pressure slice
    # ------------------------------------------------------------
    im = ax[1].imshow(
        pressure_image,
        origin="lower",
        extent=[x_min, x_max, y_min, y_max],
        aspect="auto",
        cmap="plasma",
        norm=LogNorm(vmin=vmin, vmax=vmax),
    )

    ax[1].axhline(
        actual_y,
        linestyle="--",
        linewidth=1.5,
        color="white",
        label=rf"lineout at $y={actual_y:.5f}$",
    )

    ax[1].set_xlim(x_min, x_max)
    ax[1].set_ylim(y_min, y_max)

    ax[1].set_title("prim_pressure slice")
    ax[1].set_xlabel("x (code length)")
    ax[1].set_ylabel("y (code length)")
    ax[1].legend(loc="upper right")

    cbar = fig.colorbar(
        im,
        ax=ax[1],
        pad=0.02,
    )

    cbar.set_label("prim_pressure (code units)")

    # plt.show()
    plt.savefig(f"figures/frames/prim_pressure_lineout_{i:05d}.png", dpi=300)
    # cleaning up memory
    plt.close(fig)