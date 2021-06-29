# numerical-laplace-solver

Using the finite difference method (FDM) which is described for example in
<http://www.iosrjournals.org/iosr-jm/papers/Vol6-issue4/K0646675.pdf>, this program solves the laplace equation on a two-dimensional geometry.

## Folder Structure

This project has the following folder structure
```
.
├── electric_field_and_animation
├── gnuplot_figs
├── gnuplot_generators
├── input_geometries
├── lp.py
└── pot_out
```
In the folder **electric_field_and_animation** the final results are stored. These are The electric potential for the given two-dimensional geometry as well as an image of the same data. Additionally, in this folder an animation of the evolution of the algorithm, i.e., the visualisation of the electric potential vs. iterations, is given.  

The folder **gnuplot_figs** contains the images of the electric potential for each iteration. If the variable `skip_iterations` is set to a value grater than one, every nth iteration is saved as an image. For example, setting this variable to three means every third iteration an image is being generated (which also impacts the generated animation found in the folder **electric_field_and_animation**.  

The folder **gnuplot_generators** contains the Gnuplot files which are used to generate the animation of the electric potential vs. iteration number as well as the final image of the electric field. Both, image an animation are saved in the folder **electric_field_and_animation**.  

Input sample geometries can be found in the folder **input_geometries**. These represent two-dimensional grids of numbers, with starred values representing electric potential values which are _not_ subject to change, i.e., they remain the same during computation. Use these files as shown in the source code of the file `lp.py`.  

The main program performing the (numerical) solution of the laplace equation is called `lp.py`.  

In the folder **pot_out**, the resulting electric potentials for each iteration can be found. Please note that the variable `skip_iterations` also impacts the iterative resolution of these files (see second paragraph).

## Dependencies

To generate the figures and the animation, **Gnuplot** as well as **FFmpeg** is required. Additional information about these can be found at:  
<https://www.ffmpeg.org/>  
and  
<http://www.gnuplot.info/>  

## Executing the program

Run the program with `python lp.py`

## Program settings

The following settings may be done to the program `lp.py`:
1. Input geometries as shown at the begining of the program.
2. The variable `skip_iterations` which controls the resolution of the data saved. A value of one means, the electric potential will be saved each iteration. A value of two means every second iteration will be saved, etc.
3. The variable `stop_threshold` defines the value at which the iterative solver stops. Using the function `maximum_norm(U_ij_new, U_ij_old)` calculates the maximum norm over the whole geometry (as a difference between two iterations). If this value returned by the function is smaller than the set threshold, the program stops.

## Additional information

A video of the propagation of the algorithm will be created, as well as a plot of the electric field. Animated results showing the electric potential vs. iterations can be found exemplarily at: <https://www.youtube.com/watch?v=tzwLN4l16k4> and <https://youtu.be/FtZGFcEHYiQ>
