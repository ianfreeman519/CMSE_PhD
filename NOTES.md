# Research "Notebook" to track changes made in certain scripts and codes

## 04/01/24 - Investigating Boundary Value Problems
I FOUND IT. There was a folder called `src/bvals` which has all the code that runs the boundary value problems... How elegant. The specific outflow file is in `src/bvals/cc/outflow_cc.cpp` which is only 137 lines long...

TODO I just thought of this as I was skimming through the Athena++ methods paper... There is a chance that this issue could come from the fact that I have set up a situation where in the center the divergence of the magnetic field is infinite at the center slice. I don't anticipate this being an issue because Athena++ solves iteratively, but maybe (?)...




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
    - This is where the "Initialize()" function is called, but I cannot find *where* this is defined. TODO find where Initialize function is defined.
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
TODO from meeting today:
 - Make a custom flow chart to track what Athena is actually doing
 - Set up debugger to track boundary conditions, and values. Make sure it is actually just copying rows and columns of data across to the boundary and that the zero-gradient is doing what I need it to be doing
 - Make plots of LOTS of fields and values to see if we can spot where the bad values are arriving.

## 03/21/24
The issue is not, in fact, fixed. Turns out there are 3 dimensions in real life, and all three need fields defined. I added those definitions, but the temperature is still doing really weird things. This is an image from the standard inputs, with 128x128 cells, 16x16 blocks, B0=5e5, v0=2e7 (fixed_magpinch) (left), and the same setup with B=0 (right). These plots are both at the end of the simulation time.
- <img src="athena_files/unfixed_pgen_1.png" alth="unfixed_magpinch" width="400"/>      <img src="athena_files/unfixed_pgen_no_B_20.png" alth="unfixed_magpinch" width="400"/>

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
    - <img src="athena_files/magpinch_new_pgen.png" alth="fixed_magpinch" width="600"/>

## 03/18/24

I am trying to hunt down what is causing checkerboard instabilities in simple Athena++ geometries. Specifically in the "magpinch.cpp" problem generator. Currently, it seems to be a problem with the y-velocity, and likely a halo exchange (each processor grabbing the required ghost zones to do the solve) in the positive y edge of each block. 

Old to do list:
+ (done) Make a Research Notebook
+ Change the meshblocks of the Athena++ input file to be larger (than 4x4), because the ghost zones might be reaching too far into the neighboring blocks which might be causing the instabilities
    - I ran a 32x32 with 16x16 blocks and the issue persists (big_mesh_magpinch/):
    - <img src="athena_files/magpinch_big_16x16block_0.png" alt="time0" width="400"/>        <img src="athena_files/magpinch_big_16x16block_1.png" alt="time1" width="400"/>
+ Set the magnetic fields to 0, and see what if the instabilities and errors persist. This will probably tell us if it is an MHD problem or a hydro problem, or some combination of the two.
    - Using the 16x16 blocks, and the same problem generators as above, the errors change, and now they are no longer at the halo but in the center of the region, at the intersection of all of them? Makes me think the issue isn't with the halos... (no_B_magpinch)
    - <img src="athena_files/magpinch_no_B_0.png" alt="time0" width="400"/>        <img src="athena_files/magpinch_no_B_1.png" alt="time1" width="400"/>
    - On a whim, I tried it again with v=0, and it didn't change the above outputs (no_B_no_V_magpinch).
    - Trying again with $B=0$, $v\neq 0$, back to the small meshes (no_B_small_mesh_magpinch) gave no difference to the above output.
    
+ Run a magnoh.cpp problem and a magpinch problem side by side to see if the errors are present for the problem generator I don't write.

If these things don't work, I need to sit down and make a flow chart that describes how the code runs so I can use vscode debugger to track the values of the halo exchange.