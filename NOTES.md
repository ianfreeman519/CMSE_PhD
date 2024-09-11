# Research "Notebook"
To track changes made in certain scripts and codes

## 08/25 - Broken Smoothing Schemes

New smoothing scheme doesn't work either.

## 08/20 - New Smoothing Scheme

My last smoothing scheme sucked. It was not monotonic which is problematic for this problem, and produced a ton of instabilites in the fields (see below). [This](https://www.desmos.com/calculator/rdb0bibnb8) is a new one that is continuous and smooth. At the end of the day I don't care what I "cutoff" to, I just care that the fields flatten out. I'm going to implement this and see what it fixes.

<img src="athena_files/figures/cycle0_smooth_v1_1d-Profile_radius_pressure.png" alth="initial_pressure_in_smoothed_tanh" width="400"/>
<img src="athena_files/figures/smooth_magnoh_pressure_profile_v1_1d-Profile_radius_pressure.png" alth="unstable_pressure_in_smoothed_tanh" width="400"/>

This is the initial conditions, and just 20 time steps after the initial conditions. Is Bad.

## 08/19

Made smooth_magnoh.cpp to try to implement a [tanh damping term](https://www.desmos.com/calculator/g0bljxj00h).

TODO see if Devin has any suggestions for NSF GRFP / CSGF

TODO switch account for slurm stuff using #SBATCH -A galaxies

I discovered that almost none of the simulations stay stable except for the initial conditions. Initially I made the parameterspace with the roe solver, but it is actually comically bad. I must have made a mistake when I initially tested everything because every single analysis I did indicated the pressure was flooring out (which is was because Roe is not capable of solving this problem).

I am re running the parameter space with the lhlle solver because I'm tired of dealing with unstable simulations.

## 08/16
Moved a bunch of files in athena_files directory to athena_files/figures to clean up this repo

Made a new script called plot3dmin.py to explore the 5d parameter space of simulations described below. The HPCC is moving very slow today.

## 08/14
I wrote an 'input_generator.py' in CMSE_PhD which generates a bunch of input files that span the following alpha, beta, pcoeff, d and b values (see below for scaling):
```python
alpha_values = [0, 1, 3, 5, 7]
beta_values = [0, 1, 2, 3, 5]
pcoeff_values = [1e-8, 1e-7, 1e-6]
d_values = [1.218085e-5, 1.218085e-4, 1.218085e-3]
b_values = [5e4, 5e5, 5e6] 
```

The files are in $SCRATCH/roe_pspace1 with inputs athinput.al#-be#-p#-d#-b# and al#-be#-p#-d#-b#.out2.#####.athdf where # is replaced with indices of the above arrays. This was just to make the exploration a little easier

## 08/12
Try Roe and lHHLD solver

Roe is fast, and lhhld is slow, but I don't see noticable effects of choosing one over the other. I'm going to go with roe for the sampling of phase space. The following scaling as a function of radius is how the initial conditions are set up:

$$ B = \frac{\text{bhpi or bz}}{\beta-1}*r^{\beta+1} $$
$$ \rho = \text{d} r^{\alpha} $$
$$ P = 4\pi \text{pcoeff}  * r^{2 \beta} (\text{bz}^2 + \text{bphi}^2)$$
$$ u = \rho * \text{vr} x/r$$

By default, $\alpha=5$, $\beta=3$, pcoeff $=10^{-7}$, $vr=-2\times 10^7$, $bphi=bz=5\times 10^5$, $d=1.2\times 10^{-4}$.

I want to span each of the exponents from roughly 0 to twice their current value, with about 6 points in between. I want to span each of the coefficients by orders of magnitude with 3 points in between.

$$ \alpha \in (0,10) \times 6 $$ 
$$ \beta \in (0, 6)  \times 6 $$ 
$$ p \in (p/10, 10p) \times 3 $$ 
$$ d \in (d/10, 10d) \times 3 $$ 
$$ b \in (b/10, 10b) \times 3 $$ 

$3\times3\times3\times6\times6=972$ simultations... 

## 07/30 - Trying to get Athena++ to stabilize its pressure fields

TODO see if averaging out neighboring cells if below a pressure floor rather than set the pressure/energy to the floor - in src/eos/general/general_eos.cpp? Try getting flash compiled again.


## ACCESS Grant Writing 07/29

Accurate and efficient models of plasma experiments are crucial to understanding the viability and efficacy of fusion devices and experiments. One such experiment, the plasma focus, involves symmetrically pinching a plasma into a small region, producing significant amounts of x-rays and neutrons. Within the pinch, the plasma can be modeled using the magnetohydrodynamic (MHD) equations. While originally intended for use in astrophysical scenarios, the publically available Athena++ (Done citation and spelling needed / check) software package has shown promise in simulating these systems (Done Giuliani 2012). Most simulations of these experiments are wholly symmetric, or rely on symmetric perturbations to the pinches which do not closely mirror the laboratory experiments. When nonsymmetric flows are present, magnetic reconnection (semi-spontaneous reconfiguration of the magnetic field geometry) can occur. While some fluid codes written for CPUs--namely GORGON (Done citation needed, cannot find)--have been able to successfully simulate and model laboratory reconnection experiments like the Magnetic Reconnection on Z (MARZ) experiments (Done Datta 2024), publically available simulation codes like Athena++ or the newer, GPU based code AthenaPK have been used to recreate this success.

Ideally, we would like to capture the particle effect of magnetic reconnection as it relates to laboratory fusion experiments in a fluid code. Athena++ and AthenaPK use non-ideal MHD, where the diffusion of fields is captured using a diffusive term, depending on the ohmic resistivity of the plasma. While sufficient to simulate reconnection, further investigation and comparison to laboratory experiments is needed to determine the accuracy of these reconnection effects. Depending on the current efficacy of the resistive MHD implementation to resolve reconnection, more accurate simulations of MARZ will be conducted. ... Done there is more to say here, ask Brian, maybe mention the symmetry of the problem?

The N main phenomena we intend to explore:
- The magnetic reconnection environment, and the efficacy of non-ideal MHD modeling, as it relates to the MARZ experiments.
- The internal energy densities, and the efficacty of non-ideal MHD modeling in the plasma focus.

Computation time estimates:
- Around 100 (Done motivate why) 2D CPU simulations of the MARZ setup, with a 1000x1000 grid, out to probably 1000 timesteps (roughly 10,000 CPU hours, with 2GB on each core, 10TB of hard drive space)
- Around 100 (Done motivate why) 2D GPU simulations of the MARZ setup, with a 2000x2000 grid, out to probably 1000 timesteps (roughly 15,000 GPU hours, Done how much RAM for GPU?, 40TB of hard drive space)
- Around 50 2D (Done motivate why) Plasma Focus simulations with nonsymmetrical flow, with a 2000x2000 grid for about 1000x timesteps (roughly 8,0000 GPU hours, Done RAM?, 20TB of storage)

Make sure that it compiles, and make sure the citations are in there.

We believe that radiative cooling and resitivity are important for reconnection rate, and we intend to explore parameter space ..._ ___ 

There are microphysical effects of weakly collisional plasmas and their compositions have dramatic effect on the reconnection rate and resistivity which we would like to capture in fluid codes. 2009 schekochihin

## Updates to the path to success 07/24

Ben suggested increasing pressure to drive down the initial Mach number, because the internal energy is not evolved separately. Additionally I could reduce the CFL number or order of spatial reconstruction to make the solver more diffusive.

I have not completed the path to success yet, because finding the problem appeared sooner than I thought. Upon closer inspection of the 'out of the box' problem input files, the pressure fields act strangely at cycle steps close to 200. Along the horizontal/vertical lines and diagonals on the shock front, the pressure has a habit of jumping to machine epsilon, then climbing back up to become smooth again with its neighbors a few timesteps later. This does not happen in any of the other fields, just in the pressure. Plots of the energy reservoirs over time are shown below.

<img src="athena_files/figures/ratio_mv_195.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_196.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_197.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_198.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_199.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_200.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_201.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_202.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_203.png" alth="default_problem_energy_ratios" width="400"/>
<img src="athena_files/figures/ratio_mv_204.png" alth="default_problem_energy_ratios" width="400"/>

## Up to July 15

4 step program to salvation:
1. Redownload Athena++ from a fork of the repository
  - This gives version control, make sure to track everything
  - Verify installation with a quick simulation
  - **DONE**
2. Run Magnetized Noh problem 2D again
  - Revisit original paper
  - Verify early times in default
    + **DONE** - had to modify output frequency to plot, but changed nothing else about input file
  - Copy it as `magnoh_copy.cpp` and run it again. Verify changing input files works
  - Commit to repo
    + **DONE** No problem so far.
3. Modify input file (NOT PROBLEM GENERATOR)
  - First, modify it slightly, to verify it still works
  - Modify it to make it more extreme (higher velocity, more intense density distribution, etc.)
    + Changed mesh block size and CFL number (m1-m3), and no obvious problems appeared
    + Changed Bz=0 (m4) and notice small points of zero pressure preceeding the shock (see m4 frame 50, 51, 52)
<<<<<<< HEAD
      - <img src="athena_files/figures/m4_50.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m4_51.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m4_52.png" alth="grid_size_discrepancy" width="400"/>
    + Changed vr=-2e4 (3 oom smaller) and huge regions of discontinuity in the pressure appears, but disappears a few timesteps later.
      - <img src="athena_files/figures/m6_0.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m6_1.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m6_2.png" alth="grid_size_discrepancy" width="400"/> 
      - <img src="athena_files/figures/m6_3.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m6_4.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m6_5.png" alth="grid_size_discrepancy" width="400"/> 
      - <img src="athena_files/figures/m6_6.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m6_7.png" alth="grid_size_discrepancy" width="400"/>
    + Toned down the change: vr=-1e7 (just half of the original speed...)
      - <img src="athena_files/figures/m8_99.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m8_100.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m8_101.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/figures/m8_102.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m8_103.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/figures/m8_104.png" alth="grid_size_discrepancy" width="400"/>
=======
      - <img src="athena_files/m4_50.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m4_51.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m4_52.png" alth="grid_size_discrepancy" width="400"/>
    + Changed vr=-2e4 (3 oom smaller) and huge regions of discontinuity in the pressure appears, but disappears a few timesteps later.
      - <img src="athena_files/m6_0.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m6_1.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m6_2.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m6_3.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m6_4.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m6_5.png" alth="grid_size_discrepancy" width="400"/> 
      - <img src="athena_files/m6_6.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m6_7.png" alth="grid_size_discrepancy" width="400"/>
    + Toned down the change: vr=-1e7 (just half of the original speed...)
      - <img src="athena_files/m8_99.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m8_100.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m8_101.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m8_102.png" alth="grid_size_discrepancy" width="400"/>
      - <img src="athena_files/m8_103.png" alth="grid_size_discrepancy" width="400"/> <img src="athena_files/m8_104.png" alth="grid_size_discrepancy" width="400"/>
>>>>>>> 7607ad1c2cb5d89924bddd298b19f8edfdd62ac6
  - Commit and make notes to everything
4. Convert it to the pinch problem I have been working on
  - Start with very small changes, verifying everything works as expected
  - Start with small $\alpha$ and $\beta$ terms in the input files (<<1)
  - Build up to original problem from there
  - Commit after every change

I am still waiting on a so-called fix from the Couch group for FLASH compilation, but in the meantime I reinstalled Anaconda (in the hopes that it would fix the mpi4py problems -- it did not...), and started work on simplifying the athena problem. 

Running on different spatial scales seems to have different effects on the behavior. For example, here is a 16x16 meshblock grid with 128x128 cells in each meshblock over time (YT won't plot t=0 case...) at time steps 1, 10, 100, 1000:

<img src="athena_files/figures/128_x_128_test1_press_1.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/128_x_128_test1_press_10.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/128_x_128_test1_press_100.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/128_x_128_test1_press_1000.png" alth="grid_size_discrepancy" width="400"/>

Here is a 16x16 meshblock grid with 64x64 cells in each meshblock at timesteps 0, 1, 10:

<img src="athena_files/figures/64_x_64_test2_press_0.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/64_x_64_test2_press_1.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/64_x_64_test2_press_10.png" alth="grid_size_discrepancy" width="400"/>

And finally a 16x16 meshblock grid with 32x32 cells in each in timesteps 0, 1, 10:

<img src="athena_files/figures/32_x_32_test3_press_0.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/32_x_32_test3_press_1.png" alth="grid_size_discrepancy" width="400"/>
<img src="athena_files/figures/32_x_32_test3_press_10.png" alth="grid_size_discrepancy" width="400"/>


## Up to July 10
Things to try to fix flash:

- check other makefiles from other clusters to compare and see if they work better (they did not)
- ask for help from:
  + astro (Sean)
  + Steve Fromm
  + Brandon Barker
  + (I reached out to Brandon, and TBD)
- look into docker

Start of ACCESS proposal:

Accurate and efficient models of plasma experiments are crucial to understanding the viability and efficacy of fusion devices and experiments. One such experiment, the plasma focus, involves symmetrically pinching a plasma into a small region, producing significant amounts of x-rays and neutrons. Within the pinch, the plasma can be modeled using the magnetohydrodynamic (MHD) equations. While originally intended for use in astrophysical scenarios, the AthenaPK (citation and spelling needed / check) software is capable of accurately and efficiently modeling such systems. 

The physics within the plasma focus pinch is similar to other plasma experiments like the Z pinch (citation needed), or even indirect laser drives (citation needed), all of which are rich sources of neutrons and x-rays. The cylindrical symmetry of plasma focus devices, however, allows for a drastic reduction in computational costs of simulations. 2D simulations of a slice of the plasma focus suffice to extract rich physics from the simulations. 

Another experiment with similar properties to the plasma pulse is the magnetic reconnection on Z (MARZ) experiments. In MARZ experiments, a large current pulse is driven through an exploding wire array which produces a radiatively cooled plasma and is a ripe testing ground for magnetic reconnection. MARZ experiments are unique because they are well modeled by MHD simulation packages, but exhibit features usually present in the kinetic (low density, fast timescale) limits (citation needed). As the name implies, MARZ experimentes are rich computational testing grounds for magnetic reconnection, which is an important phenomenon to understand for fusion experiments.

The N main phenomena we intend to explore:
- The magnetic reconnection environment, and the efficacy of non-ideal MHD modeling, as it relates to the MARZ experiments.
- The internal energy densities, and the efficacty of non-ideal MHD modeling in the plasma focus.
- thing N

Computational time varies beased on what specific experiment we are modeling.

### notes to fix proposal

We are essentially trying to recreate the gorgon Datta paper, but create a more robust, faster code for simulating magnetic reconnection events using AthenaPK. 

## Up to July 1
- I went to Ann Arbor for HEDSS
- TDO fill out reimbursement form
- Still trying to fix the animation script - for some reason now module command is not found?
- HPCC has been very strange since I came back from A2, and I have spent most of Wed-Friday of last trying to get it to cooperate
- That said, I did read, then reread, then reread again the Drake section on magnetic reconnection and it is starting to make some sense to me but I have a few (basic) questions:
  + All of the animations and simulations I have seen for reconnection are 2D, and the cross product of B-field and velocity flow is into/out of the page, which doesn't make sense to me. Why would Ions deflect perpendicular away from the reconnection region (fig 10.8 of Drake) in the page plane, and not into or out of the page?
  + Reconnection just seems to happen, but I have an itch for an answer that is more robust: how? How do the magnetic field lines reorganize themselves? For a brief moment, wouldn't $\nabla\cdot\textbf{B}\neq 0$ at the center of the reconnection region? Or would the two opposing magnetic field regions instantaneously communicate between one another? 
  + The reconnection rate seems to be how frequent it happens, and with units of velocity...

For the ACCESS grant, I think I want to do some PIC animations and cross-reference them with MHD simulations. Everyone in HEDSS talked a lot about PIC, and not a lot about MHD, so I'm wondering if that is a skill I should pick up this summer too. An idea I've been mulling over for a paper \/\/\/ is below and I don't know where to start for that either.

I really want to be working on a concept for a paper soon, but I'm not super sure where to start. I'm mulling over an idea for PIC where the number of super-particles can multiply or divide, kind of like an adaptive mesh refinement, depending on the region they enter or leave. High density regions don't need _more_ super particles, they need a sufficient number of representative particles to capture macroscopic behavior, while low density regions can be inaccurate if there aren't enough particles. So **maybe** there is a middle ground of, when a particle enters a 'low' density region without enough particles, it splits into two smaller superparticles. Coversely, when a particle enters a 'dense' region with too many particles, it merges with the particle to speed up the code.

## June 17
I've done some things: To recap from last week's tdo list here is what I have left:
- Fill out a pre-approval trip form for ZFS
- Register for the Z-fundamental science on account number RC114586 (charmNET DOE number)
- After I get back, make sure to pull DOE funding first, then CharmNET will pay for rest.
- Think about what simulations i wanna run for the next year and how long/how much they will cost

## June 8/10

### TDO
- Fill out a pre-approval trip form for both HEDSS and ZFS
- Register for the Z-fundamental science on account number RC114586 (charmNET DOE number)
- After I get back, make sure to pull DOE funding first, then CharmNET will pay for rest.
- Sign up to request student support (look at forwarded email from Brian)
- Think about what simulations i wanna run for the next year and how long/how much they will cost

- Possibile sources of goofy mach numbers:
  + resistivity (?)
    - Double check the units (orders of mag off?)
    - 1 Set resistivity to 0?
  + reconstruction method (?)
    - default is linear
    - 2 try setting to "PLM applied to characteristic variables" [go here](https://github.com/PrincetonUniversity/athena/wiki/The-Input-File)
  + Integrator (?)
    - currently set to vl2
  + Riemann solver (?)
    - currently set to HLLE
- [FLASH docs might be helpful](https://flash.rochester.edu/site/flashcode/user_support/flash4_ug_4p8/node192.html#SECTION010124000000000000000) 

I reformatted the movies!!! But I also learned my resolution was **TOO** high because you can't actually make out the center regions in the multi-plot animations. I need to rerun the simulations with a lower resolution (probably half) so you can make out the details in the center interesting region (see below). For reference in the future, here is the command which did it:

`ffmpeg -i simulation_animation.mp4 -vf "crop=in_w*8/10:in_h*5/10:in_w/10:in_h*30/100" -c:a copy cropped_animation.mp4`

the `-vf "crop=final_width:final_height:top_left_pixel_x:top_left_pixel_y` option is finnicky because there is no feedback, but a good way to format the output pixel positions and final dimensions is in relation to the input `in_h` and `in_w` pixel counts. You can also use `out_w` and `out_h` but I didn't try this. The code above: `"crop=in_w*8/10:in_h*5/10:in_w/10:in_h*30/100"` crops the input width to 8/10 the original value, and the heigh to 5/10 the original value. Similarly, it puts the top left corner (measured from the original top left corner) 1/10 of the original input width to the right, and 3/10 the original input height down. For a better explanation with pictures, [go here](https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg).  [Also, here is a useful cheat sheet with other ffmpeg commands](https://eruhinim.com/h/ffmpeg/).

Mach speeds and scaling relations for ideal gasses (anything that uses a $P=\rho^\gamma$ scaling relation is an ideal gas):

| Name | Formula |
| ---- | ------- |
| Alfven Speed | $VA=\frac{B}{\sqrt{4\pi\rho}}$ |
| Magnetic Mach Number | $MA=\frac{u}{VA}$ |
| Sound Speed | $CS=\sqrt{\gamma P}{\rho}\propto T^{1/2}$ |
| Sonic Mach Number | $MS = \frac{u}{CS}$ |
| Ideal Gas law | $P=nkT$ |
| Density Definition | $\rho=n m_p \mu$ |
| Mean Molecular Mass | $\mu = \text{Mass Density (wrt proton)} = \frac{\langle m \rangle}{m_p}$ |
| Plasma Parameter | $\beta=\frac{P(thermal)}{P(magnetic)}\propto\frac{T}{B^2}$ |

YT Calculates the `('gas', 'mach_number')` parameter from a ratio of velocity magnitude to sound speed, and calculates sound speed from the above equation directly. Things that *could* affect mach numbers going crazy (near simple_magpinch_animation2 frame 159 - 161):
  - fluid speed
  - sound speed
    + very large pressure (upon closer inspection, along the center line, the pressure actually approaches 0 - for demonstration purposes look at the gas or athena_pp field data for pressure to see along the edges of the collision region (y=0), the pressure goes to 0 in the cell NEXT to the center two cells. This does not explain the high mach numbers, but it is concerning and interesting.)
      - high number density (not sure how to check because athena uses mass density, but this is also stable)
      - high temperature
    + very small density (not the case - density plots seem stable and reasonable, but there is a SHARP increase near the edges)

## June 6

TDO Sign up for Z fundamental workshop and ask for student funding for travel support

## Updates as of June 4

I added a 'smoothness' parameter to the problem generator to allow a little more fine-tuning in the tanh functions without having to recompile.

I wrote an animation script that works on slurm so I can make a bunch of simulation animations simultanously, but they keep running out of memory. I need to figure out how to fix that so they stop crashing on me. Regardless, I got reconnection to happen!

Below is the magpinchsimple.cpp problem generator, with the following physical properties:

$$\rho=(1.4\times 10^{-6}) |x|^1.25$$
$$\gamma = 1.2$$
$$P = 4 \pi |B|^2 \times 10^{-6} \times x^5$$
$$\text{specific int energy}=\frac{P}{\gamma-1}+\frac{1}{2}\rho vx^2$$
$$vx = 1.4\times 10^7 \text{tanh}(Lx/'smoothness')(1+\frac{1}{2}cos(\frac{2N\pi y}{L}))$$

I'm not super confident the $P/(\gamma-1)$ makes sense physically, and I'm also concerned about the density being zero near the origin, but the simulation outputs look really promising (**each timestep is 0.1ns**):

<img src="athena_files/figures/magpinchrealistic_reconnection_event_0.png" alth="reconnection_ICs" width="400"/>

<img src="athena_files/figures/magpinchrealistic_reconnection_event_100.png" alth="reconnection_midstep" width="400"/>

<img src="athena_files/figures/magpinchrealistic_reconnection_event_400.png" alth="reconnection_midstep" width="400"/>

## May 30 2024

I made the units wiki page, which is going to be very helpful for this next step, which is matching up the Athena++ simulations with the simulations from [the radiative cooling plasmoid paper](https://arxiv.org/abs/2401.04643). In it, the preshock velocity is about 140km/s, and the magnetic field is around 4T=4e4Gauss. This is what I will be attempting to adopt into my simulations.

In preparation for this I tweaked the `magpinchsimple.cpp` problem generator to include the following line (and accept appropriate inputs from athinput):

```c++
  vx = -vin*std::tanh(x1/(10*dx))*(1+0.5*std::cos(N*2*M_PI*x2/L));
```

They say that they achieve reconnection at lundquist numbers of 120. Canonically, we consider the critical lundquist number of 10,000, so I will meet them in the middle and aim for a Lundquist number of 1000. This should allow me to estimate an order of magnitude for the resistivity:


The paper claims an ion density of around 6e18 cm$^-3$ which means I need to input 1.4 x mp(g) x 6e18 = 1.4e-6

$$SL = Lv_A/\eta$$
$$S_L= 10^3 = \frac{B*L}{\eta\sqrt{\mu0 \rho}}$$
$$\longrarrow \eta = \frac{B*L}{1e3 \sqrt{\mu0 \rho}}$$
$$\longrarrow \eta = \frac{4e4 * 0.6}{1e3 \sqrt{1 * 1.4e-6}}$$

According to this calculation, the resistivity is 2e4...

## May 28 2024

I fixed the multi-plot movie. ChatGPT, coupled with some difficult-to-find forum posts from years ago allowed me to come up with the `makeMovie.py` stored within the athena_files directory. It utilizes this chunk of code (which I still don't _entirely_ understand, but it works so I'm not going to complain too much):
```python
    # Save the figure to a buffer with increased DPI
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200)  # Increase DPI
    buf.seek(0)
    frames.append(np.array(plt.imread(buf)))
    buf.close()
    plt.close(fig)  # Close the figure to avoid displaying it
```
The script converts the YT plot to matplotlib objects fig and ax, which then get saved using matplotlib commands. Then the raw data is saved as a buffer which makes the pointer point to the end of the buffer. The `buf.seek(0)` sets the pointer to the beginning of the buffer so the `frames.append(np.array(plt.imread(buf)))` can read the buffer from the beginning as an np.array image. Then the resources used with the buffer are closed, and the plt figure is closed, because it has been saved in the frames array.

Brian suggested that I make a github wiki page on the units, which I need to remember to link within this document for my own personal records. That is what I will be working on today.

## After May 20

After an intense amount of experimentation, I discovered the 'prim' dataset in athdf files are full matrices representing first the density, then pressure, then velocity fields. Now, what the difference between that and x1v and x1f are, I have absolutely no clue.

Making the plots has proven a lot more difficult than I originally thought it would. For some reason when I submit a script to slurm it doesn't like it, but when I run the python command to make the movie it does it no problem.

## Early summer 2024

I got sick... But I read some papers and wrote the magpinchsimple problem generator:

```c++
  for (int k=ks; k<=ke; k++) {
    for (int j=js; j<=je; j++) {
      for (int i=is; i<=ie; i++) {
        // Volume centered coordinates and quantities
        Real x1,x2,dx;
      
        x1 = pcoord->x1v(i);
        dx = pcoord->x1v(i+1) - x1;
        x2 = pcoord->x2v(j);

        Real rho = rho0*std::pow(std::abs(x1), alpha/4);
        Real P   = P0  *std::pow(std::abs(x1), 2*beta);

        phydro->u(IDN,k,j,i) = rho;         // Density

        // x momentum
        phydro->u(IM1,k,j,i) = -rho*vin*std::tanh(x1/(2*dx))*(1+0.01*std::cos(x2/2));

        phydro->u(IM2,k,j,i) = 0.0;         // Momentum in x2
        phydro->u(IM3,k,j,i) = 0.0;         // Momentum in x3
        phydro->u(IEN,k,j,i) = P/gm1 + 0.5*rho*SQR(vin); // Total energy
        debug_tester = P/gm1 + 0.5*rho*SQR(vin); // TDO REMOVE
      }
    }
  }

    Real x1, dx;
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {    // j loop for(int j=0; j<=je+js; i++)
          x1 = pcoord->x1v(i);
          dx = pcoord->x1v(i+1) - x1;
          pfield->b.x2f(k,j,i) = b*std::tanh(x1/(2*dx));
        }
      }
    }
```

Unfortunately, I'm getting weird zeros (?) all over the place in a region close to the origin. Here is the initial conditions at t=0 (when using std::cos() on left and std::sin() on right):

<img src="athena_files/figures/magpinchsimple_test_funky_pressure_may_16.png" alth="unfixed_simple_magpinch" width="400"/>
<img src="athena_files/figures/magpinchsimple_test_funky_pressure_sin_may_16.png" alth="unfixed_simple_magpinch" width="400"/>

Things to try:
- try setting athinput.magpinchsimple $\beta=1$

Things to look up:
- running simulations/analysis on a galaxy node (see pinned mattermost messages)
- shared partition
- temporary disk space (/mnt/tmp)
- RAM Disk (/mnt/ramddisk???)

## Meeting with Brian May 2 2024

We are pushing the simulations very hard...

Consider trying the magnetic field to be on order $tanh(x/2\Delta x)$, and the velocity to be on order $tanh(x/\Delta x)$

To be more precise:

$$v_x=-v0 tanh(x/2\Delta x)$$

$$B_y=btanh(x/ 2\Delta x)$$

Then make velocity to be on order equivalent to Magnetic Field, and thermal pressure ($v^2~B^2~P_th$), and set density and thermal pressure to be constant.

## Comprehensive list of everything attempted as of May 1 2024
The original goal was to simulate the z-pinch to give me a grasp of how Athena++ works. This, initially, was successful, and can be seen at athena_files/figures/zpinch5_density_Bfield.mp4. To get closer to the MARZ experiment, we added a slight perturbation in the radial direction, and set the resistivity (eta_ohm) in the athinput file to be nonzero to trigger magnetic reconnection. In the complicated simulation, we got this to work, and can be seen in athena_files/figures/zpinchCP3_density_velocity.mp4.

We then wanted to isolate the magnetic reconnection bit, so we decided to 'flatten out' the radial component, and make an inflow along the x-direction, strongest at $y=0$, and put opposing B-fields in the $x>0$ and $x\leq0$ regions. The full initial conditions set up is as follows:

$$\textbf{u}=(-sgn(x)\frac{\rho v_{in}}{y+1/3},0,0)$$

$$\textbf{B}=(0,sgn(x) \frac{b}{\beta+1} (x)^{\beta+1},0)$$ 

By default, $\beta=2.5$, $v_in=2e7$ (usually), and $b=5e5$ (usually, more on that later). This configuration should yield the y and z velocities to be 0 everywhere, and the x and z magnetic fields to be 0. Originally, I borrowed the problem generator from the magnoh problem, and removed the radial component. I didn't realize the magnetic field needed to be face-centered, so I unintentionally deleted one of the for loops that handled this case, and it entirely broke. For a few weeks we dealt with that error. Originally, the magnoh problem set the b-field with the following loops (I include pressure here as well):

```c++
  if (MAGNETIC_FIELDS_ENABLED) {
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie+1; i++) {
          Real geom_coeff = 1.0;
          if (std::strcmp(COORDINATE_SYSTEM, "cylindrical") == 0) {
            geom_coeff = 1.0/pcoord->x1f(i);
          }
          pfield->b.x1f(k,j,i) = geom_coeff*(az(j+1,i) - az(j,i))/pcoord->dx2f(j);
        }
      }
    }
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {
          Real geom_coeff = 1.0;
          if (std::strcmp(COORDINATE_SYSTEM, "cylindrical") == 0) {
            geom_coeff = -1.0; // Left hand system?
          }
          pfield->b.x2f(k,j,i) = geom_coeff*(az(j,i) - az(j,i+1))/pcoord->dx1f(i);
        }
      }
    }
    for (int k=ks; k<=ke+1; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie; i++) {
          Real rad;
          if (std::strcmp(COORDINATE_SYSTEM, "cylindrical") == 0) {
            rad = pcoord->x1v(i);
          } else {
            rad = std::sqrt(SQR(pcoord->x1v(i)) + SQR(pcoord->x2v(j)));
          }
          pfield->b.x3f(k,j,i) = bz*std::pow(rad,beta);
        }
      }
    }
    if (NON_BAROTROPIC_EOS) {
      for (int k=ks; k<=ke; k++) {
        for (int j=js; j<=je; j++) {
          for (int i=is; i<=ie; i++) {
            phydro->u(IEN,k,j,i) +=
                // second-order accurate assumption about volume-averaged field
                0.5*0.25*(SQR(pfield->b.x1f(k,j,i) + pfield->b.x1f(k,j,i+1))
                          + SQR(pfield->b.x2f(k,j,i)  + pfield->b.x2f(k,j+1,i))
                          + SQR(pfield->b.x3f(k,j,i) + pfield->b.x3f(k+1,j,i)));
          }
        }
      }
    }
```

When I tried to implement the field configuration we wanted originally, this is what I came up with:

```c++
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {    // j loop for(int j=0; j<=je+js; i++)
          auto debug_var = js;
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }
    if (NON_BAROTROPIC_EOS) {
      for (int k=ks; k<=ke; k++) {
        for (int j=js; j<=je; j++) {
          for (int i=is; i<=ie; i++) {
            phydro->u(IEN,k,j,i) +=
                // second-order accurate assumption about volume-averaged field
                0.5*0.25*(SQR(pfield->b.x1f(k,j,i) + pfield->b.x1f(k,j,i+1))
                          + SQR(pfield->b.x2f(k,j,i)  + pfield->b.x2f(k,j+1,i))
                          + SQR(pfield->b.x3f(k,j,i) + pfield->b.x3f(k+1,j,i)));
          }
        }
      }
    }
```

This does not work, because the face-centered fields were only being set in the j-direction, and not in the i- or k-directions. To hunt down this problem, we set the magnetic fields to zero, but recall, the pressure is set to the average magnetic pressure in the center of each cell. There were a few weeks earlier this semester where we hunted down *why* the pressure (and thermal energy) was so noisy in the initial conditions, and this is why. The pressure was being set to 0 when the magnetic fields were set to 0, which was filling the pressure fields with noise on order of machine precision ($1e-18$ to $1e-16$). Athena is smart, however, and after a single time step stabalized the pressure fields. Along the strongest velocities, the boundaaries gave us NaNs or 0s (I'm still not entirely sure how to check this) from the boundaries afterward. I used the VSCode debugger to hunt down the problem, because we thought the 'bad values' were coming from the boundary conditions. Through the debugger, I verified the boundary conditions within Athena's `bvals` methods were being handled correctlu. This was 'fixed' late in March (details/notes/few figures below). I decided instead of trying to debug the pressure fields in the case where $B=0$, to just resort to fixing the $B\neq0$ case because that is required for the interesting reconnection to occur, However, the B-fields were still not being set properly, so those instabilities/issues were just hiding the issues with the pressure, which eventually returned.

So the new and improved problem generator magnetic field loops, which are closely mirrored from the magnoh.cpp problem generator look like this:

```c++
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {    // j loop for(int j=0; j<=je+js; i++)
          auto debug_var = js;
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }
    for (int k=ks; k<=ke+1; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie; i++) {    // k loop
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie+1; i++) {    // i loop
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }
```

But very problematically, the top edges (or maybe bottom?) of the simulation cells are/were not being filled in properly, but they are still nonzero? We haven't quite figured out what is happening here. Below is the colorplot with the annotated magnetic fields (black arrows) and the y-direction magnetic field strength using the above magnetic field loops.

<img src="athena_files/figures/magnetic_field_y_three_looped_magpinch.png" alth="unfixed_magpinch" width="400"/>

This for loop structure is actually what I/we have returned to, because the other things we have tried have not yielded good results. Regardless, Brian suggested I try filling in all the values deep into the ghost zones of everything, to give me total control over whats happening. Unfortunately, this does not work either. Here is the loop I tried to do for that:

```c++
    for (int k=0; k<=ke+ks+1; k++) {
      for (int j=0; j<=je+js+1; j++) {
        for (int i=0; i<=ie+is+1; i++) {    // j loop for(int j=0; j<=je+js; i++)
          x1 = pcoord->x1v(i);
          if (x1 >= 0.0) {
            pfield->b.x2f(k,j,i) = (b/(beta+1))*std::pow(x1,beta+1);
          } else {
            pfield->b.x2f(k,j,i) = -1.0*(b/(beta+1))*std::pow(std::abs(x1),beta+1);
          }
          pfield->b.x1f(k,j,i) = 0.0;
          pfield->b.x3f(k,j,i) = 0.0;
        }
      }
    }

    if (NON_BAROTROPIC_EOS) {
      for (int k=ks; k<=ke; k++) {
        for (int j=js; j<=je; j++) {
          for (int i=is; i<=ie; i++) {
            phydro->u(IEN,k,j,i) +=
                // second-order accurate assumption about volume-averaged field
                0.5*0.25*(SQR(pfield->b.x1f(k,j,i) + pfield->b.x1f(k,j,i+1))
                          + SQR(pfield->b.x2f(k,j,i)  + pfield->b.x2f(k,j+1,i))
                          + SQR(pfield->b.x3f(k,j,i) + pfield->b.x3f(k+1,j,i)));
                          // Internal Energy is adjusted based on magnetic energy
          }
        }
      }
    }
```

This does not fill in the magnetic fields properly (all constant and 0), but I'm not 100% sure why yet. Every time I run a simulation with this initial condition, the code compiles and runs, but OpenMP dumps the core information out, and spits a ton of errors. I believe this is a product of reaching into the "far corner" of the array domain. I believe (I have not confirmed this yet) all entries of the pfield.b is defined except for `pfield->b.x#f(ke+ks+1, je+js+1, ie+is+1)`. This would explain some of the pointer errors I get after running the simulation:

```
*** Error in `athenaEXE': free(): invalid pointer: 0x00000000009f31f0 ***
*** Error in `athenaEXE': free(): invalid pointer: 0x00000000016d4e90 ***
*** Error in `athenaEXE': free(): invalid pointer: 0x000000000296c030 ***
```

Regardless, this is the output of the initial conditions when generated with the 'full' magpinch case:

<img src="athena_files/figures/magnetic_field_y_one_looped_magpinch.png" alth="unfixed_magpinch" width="400"/>

I have resorted back to the three-looped problem generator above, and intend on experimenting with different starting and ending indices. 

I have also been trying to train ChatGPT on Athena to help with debugging, and it has started to give better and better suggestions. It seems to be convinced that the error I'm experiencing stems from the fact that I am not using a vector potential, and therefore simulating unphysical magnetic field conditions. While true, I do not believe this is the cause issue. After a little prodding, it pointed out that I am setting the x-, y-, and z-directions in all three loops. Instead, in the `for (int j=js; j<=je+1; j++)` loop, I should only be setting the `b.x2f` variable, because at `je+1`, the `b.x1f` and `b.x1f` are undefined. Similarly, in the x- and z-loops, I should only be setting the x- and z-magnetic fields (respectively). **THIS FIXES THE MAGNETIC FIELD PROBLEM**, and all the magnetic fields are fully filled in (as of today, May 1). Below are some plots about this issue, because it is the most recent.

Below is the initial magnetic field configuration, with color representing magnetic fields in the y-direction, and vectors representing the directionality of the magnetic field of the fully fixed problem generator:

<img src="athena_files/figures/magnetic_field_y_three_looped_fixed_magpinch.png" alth="fixed_magpinch" width="400"/>

Here are the initial pressure fields (left) of the initial conditions, and the pressure fields (right) after a single time-step:

<img src="athena_files/figures/pressure_three_looped_fixed_magpinch_0.png" alth="fixed_magpinch_pressure_0" width="400"/>     <img src="athena_files/figures/pressure_three_looped_fixed_magpinch_1.png" alth="fixed_magpinch_pressure_1" width="400"/>

Observe that despite the apparent correctness of the initial conditions, the pressure field is still broken over time, drawing in unknown errors from the boundary along fast inflows. The actual directory with real outputs is `magpinch_fixed_may1` for this simulation. Below are some multiplots showing other details:

<img src="athena_files/figures/multiplot_three_looped_fixed_magpinch_0.png" alth="multiplot_magpinch_pressure_0" width="400"/>     <img src="athena_files/figures/multiplot_three_looped_fixed_magpinch_1.png" alth="multiplot_magpinch_pressure_1" width="400"/>

## 05/01/24
I have attempted to fill in everything, but the velocity, pressure, and density fields break when the indices are filled in with the following loop:
```c++
for (int k=0; k<=ke+ks+1; k++) {
    for (int j=0; j<=je+ks+1; j++) {
        for (int i=0; i<=ie+is+1; i++) {
```
Regardless, the magnetic fields are reaching far into the ghost zones and the instabilities below are still not cooperating.

I lied. ChatGPT figured it out. The face-centered magnetic fields only have face-values above je, ke, and ie in the j-, k-, and i-direction respectively. Therefore, we should only set the x, y, and z magnetic field when we iterate over ie+1, je+1, and ke+1, respectively. This fixes the magnetic field issue (pictures above, in the section called Comprehensive List of Everything... May 1). It does *not* fix the pressure issue where NaNs/zeros inflow from the boundary. This is now the same problem we had March 21, which kick-started this whole investigation.

## 04/09/24 - meeting with Brian
Things to try:
- make sure x&z values are set to 0 out into the ghost zones for mag fields
- make sure all y values are set INTO the ghost zones
- Confirm the size of b.x1f, b.x2f, b.x3f have sizes (n+1)xnx1, etc. 
- As a sanity check: change the code in `magpinch.cpp` to set the magnetic field in EVERY cell for EVERY dimension - make the loops go from i,j,k = 0 to i,j,k = MAX (MAX might be is+ie+1)?  **DO THIS IN A NEW .CPP FILE - PROTECT YOURSELF FROM YOURSELF**
- Ask Ben or Google how to make experimental branches of git repos

## 04/07/24 - Discussion with Ben
I talked with Ben who asked me some simple questions about pressure and temperature in the simulations, and I realized I need to figure out how the units in Athena work. He asked about Pressure, so I went to double check the pressure definition in `magpinch.cpp` and it is set to the magnetic pressure. That is why the initial pressure plots look so bad for the B=0 case. That said, I have a few things I need to try to fix the bad values coming in from the boundaries.
 - The mach number at those bad values are also bad, which Ben thinks is an issue with the initial speed. The simulation that was plotted below on 03/21 had initial velocities of 2e7, which is *fast*, but not too fast. Therefore we should set the velocity to a mach number somewhere between 2 and 5, to force a shock at the center, but not push the simulation too much.
 - The pressure wholly depends on magnetic field, so I need to add a base case where the mach number is 2 or 3, and add it to the pressure in the problem generator to ensure that when the magnetic field is 0, the pressure is still nonzero.

As a reminder to myself ($\gamma=2.0$), sound speed is $c_{s}=\sqrt{\gamma\frac{p}{\rho}}$, mach number is $v/c_s$, and the initial velocity profile ($x>0$) is given by $u=-\frac{\rho v_{in}}{y+1/3}$ with $v_{in}$ from the athinput file. Additionally, magnetic fields are filled in with $B=\pm \frac{B_0}{\beta+1} (x)^{\beta+1}$ which peaks at $x=3$, and should yield 0 at the center. By default $\beta=2.5$ (this is defined in athinput file as well).

As a litmus test, I set the magnetic field to 5e3, $v_{in}$ to 2e4, and when I check the magnetic field strenght plot in YT, it is not fully uniform in the y direction which it needs to be.

I reordered the way magnetic fields are set again within the problem generator in order of execution:
```c++
    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {

    for (int k=ks; k<=ke+1; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie; i++) {

    for (int k=ks; k<=ke; k++) {
      for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie+1; i++) {
```

 Below are the outputs of this problem generator, with $B_0$ set to 5e3, $v_{in}$ to 2e4. This fixed the sloppy initial conditions. More work needs to be done on completing the problem generator to fully describe all fields inside each meshblock. On **the left is t=0, on the right is t=1**. The files which generate this are in the aptly named `new_pgen_magpinch` file in the scratch directory.

<img src="athena_files/figures/reordered_pgen_with_med_b_med_v_0.png" alth="unfixed_magpinch" width="400"/>      <img src="athena_files/figures/reordered_pgen_with_med_b_med_v_0.png" alth="unfixed_magpinch" width="400"/>


## 04/02/24 - Debugging time
When I run the debugger, I put breakpoints all throughout the OutflowInnerX1() method in the `src/bvals/cc/outflow_cc.cpp` file. From one step to the next, it looks like it is pulling 0s from the boundary and placing them in the simulation zone. It is working exactly as it should, so I think it is really a root cause in my problem generator...

## 04/01/24 - Investigating Boundary Value Problems
I FOUND IT. There was a folder called `src/bvals` which has all the code that runs the boundary value problems... How elegant. The specific outflow file is in `src/bvals/cc/outflow_cc.cpp` which is only 137 lines long...

TDO I just thought of this as I was skimming through the Athena++ methods paper... There is a chance that this issue could come from the fact that I have set up a situation where in the center the divergence of the magnetic field is infinite at the center slice. I don't anticipate this being an issue because Athena++ solves iteratively, but maybe (?)...




## 03/27/24 & 04/01/24 - Notes on Athena++ flow
 - [Athena++ Method Paper](https://ui.adsabs.harvard.edu/abs/2020ApJS..249....4S/abstract)
 - Added a few alias commansd in ~/.bashrc to make working in this document easier.
 - Started a flow chart for athena, and I have the following questions:
    + There are a whole lot of MPI_Finalize() calls floating around, but not a lot of initialization calls going around. I know [MPI_Finalize does not actually destroy any information](https://stackoverflow.com/a/2290951/893863), but I don't understand why MPI is working the way it is in this code.

Inside Athena++, main.cpp is the brain of the operation. There are 10 main steps:
 1. (Line 71) Initializing environment
 2. (Line 117) Grabbing command line arguments
 3. (Line 216) Parsing input file and command line arguments.
    - When MPI is initialized, the input file is read by every process
    - This part of the code relies wholly on src/parameter_input.cpp (and .hpp)
        + It grabs all the important data about meshblocks and the specific problem generator from the athinput.* file.
 4. (Line 264) Constructing and initializing mesh
    - This part of the code works out of src/mesh/mesh.cpp (and .hpp)
        +  at first glance, this is only responsible for AMR and initialization, NOT dealing with boundary conditions in the middle of runs.
 5. (Line 325) Constructing a "TaskList" for the integrator
    - This part goes WAY over my head, because its full of `if (integrator == "thing") {` commands, which I understand at face value, but the details of this step are lost on me.
    - I believe this step is initializing the integrator so it can be called faster (?) in the future.
 6. (Line 364) Initial conditions from problem generator.
    - This is where the "Initialize()" function is called, but I cannot find *where* this is defined. (old to do) find where Initialize function is defined.
 7. (Line 390) Create output object, and output ICs
    - This part is not the problem part, and there is nothing immediately confusing about it, so I am moving on.
    - Run from src/outputs/outputs.cpp (and .hpp)
    - `pouts` object is what acutally makes the outputs.
    - `pouts->MakeOutputs(mesh,input)` method is what actually makes the files
 8. (Line 420) Main integration loop
    - Conditions for integration loop: `(pmesh->time < pmesh->tlim) && (pmesh->nlim < 0 || pmesh->ncycle < pmesh->nlim)`
    - On rank 0, `pmesh->OutputCycleDiagnostics()`
    - By default, we don't have supertimestepping enabled, so we skip lines 437-357
    - By default, we don't have driven turbulence enabled, so we skip line 459
    - Inside the main loop is the following for loop:
    ```c++
        for (int stage=1; stage<=ptlist->nstages; ++stage) {
            ptlist->DoTaskListOneStage(pmesh, stage);
            //Then a bunch of self_gravity checks
        }
    ```
    - The `DoTaskListOneStage(pmesh, stage)` calls `DoAllAvailableTasks(mesh, stage)`, which at some point digs into meshblock.cpp to run the time measurement schemes.
    - Next it calls `pmesh->UserWorkInLoop()` which I **finally found** in the src/mesh/mesh.cpp (line 1679). Looks like the code that is responsible for setting the boundary buffers is the call of `pmb->pscalars->sbvar.SendBoundaryBuffers()` or the mesh function `SetBlockSizeAndBoundaries`
    - The method paper claims that boundary conditions are applied on the coarse buffer of each meshblock on 'step 5' of the meshblock communication cycle.
 9. (Line 524) Output final cycle diagnostics
    - Makes the output files for the last timestep in case it doesn't align with the stopping time
 10. (Line 555) Print diagnostic messages related to end of simulation
    - Namely what the termination conditions were, how many cycles Athena++ went through, and what the time limit was.
    - Deletes a lot of variables, and finalizes MPI
    

## 03/25/24
To do list (completed)
 - Make a custom flow chart to track what Athena is actually doing
 - Set up debugger to track boundary conditions, and values. Make sure it is actually just copying rows and columns of data across to the boundary and that the zero-gradient is doing what I need it to be doing
 - Make plots of LOTS of fields and values to see if we can spot where the bad values are arriving.

## 03/21/24
The issue is not, in fact, fixed. Turns out there are 3 dimensions in real life, and all three need fields defined. I added those definitions, but the temperature is still doing really weird things. This is an image from the standard inputs, with 128x128 cells, 16x16 blocks, B0=5e5, v0=2e7 (fixed_magpinch) (left), and the same setup with B=0 (right). These plots are both at the end of the simulation time.
- <img src="athena_files/figures/unfixed_pgen_1.png" alth="unfixed_magpinch" width="400"/>      <img src="athena_files/figures/unfixed_pgen_no_B_20.png" alth="unfixed_magpinch" width="400"/>

The changes I made to the problem generator (I added two more nested for loops to account for the y- and z- direction B-field in each meshblock...):

```c++
for (int k=ks; k<=ke; k++) {
    for (int j=js; j<=je+1; j++) {
        for (int i=is; i<=ie; i++) {
            // Same as x-direction
        }
    }
}
for (int k=ks; k<=ke+1; k++) {
    for (int j=js; j<=je; j++) {
        for (int i=is; i<=ie; i++) {
            // Same as x-direction
        }
    }
}
```

For some reason, it looks like the bad values of pressure and temperature are coming in from the boundaries that have velocity pointing away from them. I don't know what to make of that. There is also something goofy going on with the velocity magnitude at the +/-y boundaries, which doesn't make sense because the y-velocity at the boundaries should be 0.


## 03/20/24 - Fixed checkerboard issue
Brian noticed a few days ago that it very well might be a face-centered field initialization problem in my problem generator. The face centered fields for some reason need to be set from i=1 to i=ie+1 and j=1 to j=je+1. I originally missed this when I made this problem generator.
+ This fixed the issue:
    - <img src="athena_files/figures/magpinch_new_pgen.png" alth="fixed_magpinch" width="600"/>

## 03/18/24

I am trying to hunt down what is causing checkerboard instabilities in simple Athena++ geometries. Specifically in the "magpinch.cpp" problem generator. Currently, it seems to be a problem with the y-velocity, and likely a halo exchange (each processor grabbing the required ghost zones to do the solve) in the positive y edge of each block. 

Old to do list:
+ (done) Make a Research Notebook
+ Change the meshblocks of the Athena++ input file to be larger (than 4x4), because the ghost zones might be reaching too far into the neighboring blocks which might be causing the instabilities
    - I ran a 32x32 with 16x16 blocks and the issue persists (big_mesh_magpinch/):
    - <img src="athena_files/figures/magpinch_big_16x16block_0.png" alt="time0" width="400"/>        <img src="athena_files/figures/magpinch_big_16x16block_1.png" alt="time1" width="400"/>
+ Set the magnetic fields to 0, and see what if the instabilities and errors persist. This will probably tell us if it is an MHD problem or a hydro problem, or some combination of the two.
    - Using the 16x16 blocks, and the same problem generators as above, the errors change, and now they are no longer at the halo but in the center of the region, at the intersection of all of them? Makes me think the issue isn't with the halos... (no_B_magpinch)
    - <img src="athena_files/figures/magpinch_no_B_0.png" alt="time0" width="400"/>        <img src="athena_files/figures/magpinch_no_B_1.png" alt="time1" width="400"/>
    - On a whim, I tried it again with v=0, and it didn't change the above outputs (no_B_no_V_magpinch).
    - Trying again with $B=0$, $v\neq 0$, back to the small meshes (no_B_small_mesh_magpinch) gave no difference to the above output.
    
+ Run a magnoh.cpp problem and a magpinch problem side by side to see if the errors are present for the problem generator I don't write.

If these things don't work, I need to sit down and make a flow chart that describes how the code runs so I can use vscode debugger to track the values of the halo exchange.
