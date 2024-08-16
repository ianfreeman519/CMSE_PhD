import os

# Define the parameters you want to vary
alpha_values = [0, 1, 3, 5, 7]
beta_values = [0, 1, 2, 3, 5]
pcoeff_values = [1e-8, 1e-7, 1e-6]
d_values = [1.218085e-5, 1.218085e-4, 1.218085e-3]
b_values = [5e4, 5e5, 5e6] 

# Read the template file
template = """<comment>
problem = Z-pinch; Magnetized Noh with axial and azimuthal field
configure = --prob=magnoh -b --flux=hlle -hdf5 -h5double
reference = Authored by A. Beresnyak. Mag Noh "Problem 2" from:

# "Self-similar solutions for the magnetized Noh problem with axial and azimuthal field",
# Giuliani, Velikovich, Beresnyak, Zalesak, Gianakon, Rousculp,
# Phys. of Plasmas, in prep (2018)

<job>
problem_id  = {out_name}    # problem ID: basename of output filenames

<output1>
file_type   = hst       # History data dump
dt          = 1e-11     # time increment between outputs
data_format = %12.5e    # Optional data format string

<output2>
file_type = hdf5        # HDF5 data dump
variable  = prim        # variables to be output
# dt        = 1.5e-8      # time increment between outputs
dcycle      = 1

<time>
cfl_number = 0.45        # The Courant, Friedrichs, & Lewy (CFL) Number
nlim       = 300         # cycle limit
tlim       = 2.0e-8     # time limit
integrator  = vl2       # time integration algorithm
xorder      = 2         # order of spatial reconstruction
ncycle_out  = 1         # interval for stdout summary info

<mesh>
nx1        = 300        # Number of zones in X1-direction
x1min      = -3.0       # minimum value of X1
x1max      =  3.0       # maximum value of X1
ix1_bc     = outflow    # Inner-X1 boundary condition flag
ox1_bc     = outflow    # Outer-X1 boundary condition flag

nx2        = 300        # Number of zones in X2-direction
x2min      = -3.0       # minimum value of X2
x2max      =  3.0       # maximum value of X2
ix2_bc     = outflow    # Inner-X2 boundary condition flag
ox2_bc     = outflow    # Outer-X2 boundary condition flag

nx3        = 1          # Number of zones in X3-direction
x3min      = -1.0       # minimum value of X3
x3max      = 1.0        # maximum value of X3
ix3_bc     = periodic   # Inner-X3 boundary condition flag
ox3_bc     = periodic   # Outer-X3 boundary condition flag

refinement = static

<refinement1>
x1min = -0.4
x1max =  0.4
x2min = -0.4
x2max =  0.4
x3min =  0.0
x3max =  0.0
level =  1

<refinement2>
x1min = -0.2
x1max =  0.2
x2min = -0.2
x2max =  0.2
x3min =  0.0
x3max =  0.0
level =  2

<meshblock>
nx1        = 100        # Number of zones in X1-direction
nx2        = 100        # Number of zones in X2-direction
nx3        = 1          # Number of zones in X3-direction

<hydro>
gamma      = 2.0        # gamma = C_p/C_v

<problem>
alpha      = {alpha}
beta       = {beta}        
pcoeff     = {pcoeff}
d          = {d}
vr         = -2e7
bphi       = {b}
bz         = {b}
perturb    = 0.0
mphi       = 1.0
"""

# Loop over all parameter combinations and generate files
file_counter = 1
for i1, alpha in enumerate(alpha_values):
    for i2, beta in enumerate(beta_values):
        for i3, pcoeff in enumerate(pcoeff_values):
            for i4, d in enumerate(d_values):
                for i5, b in enumerate(b_values):
                    # Generate the content by replacing placeholders with actual values
                    out_name = f"al{i1}_be{i2}_p{i3}_d{i4}_b{i5}"
                    content = template.format(alpha=alpha, beta=beta, pcoeff=pcoeff, d=d, b=b, out_name=out_name)

                    # Define the output filename
                    filename = f"athinput.{out_name}"

                    # Write the content to the file
                    with open(filename, 'w') as file:
                        file.write(content)

                    print(f"Generated {filename}")
                    file_counter += 1

print(f"Generated {file_counter} files successfully")
