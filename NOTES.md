# Research "Notebook" to track changes made in certain scripts and codes

## 03/21/24
The issue is not, in fact, fixed. Turns out there are 3 dimensions in real life, and all three need fields defined. I added those definitions, but the temperature is still doing really weird things. This is an image from the standard inputs, with 128x128 cells, 16x16 blocks, B0=5e5, v0=2e7 (fixed_magpinch) (left), and the same setup with B=0 (right). These plots are both at the end of the simulation time.
- <img src="athena_files/unfixed_pgen_1.png" alth="unfixed_magpinch" width="400"/>      <img src="athena_files/unfixed_pgen_no_B_20.png" alth="unfixed_magpinch" width="400"/>

The changes I made to the problem generator (I added two more nested for loops to account for the y- and z- direction B-field in each meshblock...):

``` c++
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