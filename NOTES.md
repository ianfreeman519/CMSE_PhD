# Research "Notebook" to track changes made in certain scripts and codes

## 03/20/24 - Fixed checkerboard issue
Brian noticed a few days ago that it very well might be a face-centered field initialization problem in my problem generator. The face centered fields for some reason need to be set from i=1 to i=ie+1 and j=1 to j=je+1. I originally missed this when I made this problem generator.
+ This fixed the issue:
    - <img src="athena_files/magpinch_new_pgen.png" alth="fixed_magpinch" width="600"/>

## 03/18/24

I am trying to hunt down what is causing checkerboard instabilities in simple Athena++ geometries. Specifically in the "magpinch.cpp" problem generator. Currently, it seems to be a problem with the y-velocity, and likely a halo exchange (each processor grabbing the required ghost zones to do the solve) in the positive y edge of each block. 

TODO:
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