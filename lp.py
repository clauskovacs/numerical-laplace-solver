# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
from os import system, remove	# shell commands from python


# folder where the gemetries defining the problems are stored
f_dir = 'input_geometries/'

# folder where the electric potentials (for each iteration) are stored
folder_out = 'pot_out/'

# folder where the *.plt files are stored (and invoked by Gnuplot)
gnuplot_generator_dir = "gnuplot_generators/"

# some sample geometries:
"""
Sample two-dimensional problem sets.
Use them according the information provided here.
"""

"""
# pl_ko30x30.dat
dim_x = 30
dim_y = 30
input_file_geometry = 'pl_ko' + str(dim_x) + 'x' + str(dim_y)
input_file = f_dir + input_file_geometry + '.dat'
"""


#zyl-100x100-20-49-0.dat
dim_x = 100
dim_y = 100
input_file_geometry = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-20-49-0'
input_file = f_dir + input_file_geometry + '.dat'


"""
#loch_ko60x60.dat.dat
dim_x = 60
dim_y = 60
input_file_geometry = 'loch_ko' + str(dim_x) + 'x' + str(dim_y) + ''
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#dach_l_ko60x60.dat
dim_x = 60
dim_y = 60
input_file_geometry = 'dach_l_ko' + str(dim_x) + 'x' + str(dim_y) + ''
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#zyl_1040x1040_400_500_0.dat
dim_x = 1040
dim_y = 1040
input_file_geometry = 'zyl_' + str(dim_x) + 'x' + str(dim_y) + '_400_500_0'
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#dach_ko60x60.dat
dim_x = 60
dim_y = 60
input_file_geometry = 'dach_ko' + str(dim_x) + 'x' + str(dim_y)
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#zyl-100x100-40-50-0.dat
dim_x = 100
dim_y = 100
input_file_geometry = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-40-50-0'	
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#zyl-100x100-20-49-0.dat
dim_x = 100
dim_y = 100
input_file_geometry = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-20-49-0'	
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#zyl-200x200-40-98-40.dat
dim_x = 200
dim_y = 200
input_file_geometry = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-40-98-40'	
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#pl_ko60x60_kreuz.dat
dim_x = 60
dim_y = 60
input_file_geometry = 'pl_ko' + str(dim_x) + 'x' + str(dim_y) + '_kreuz'	
input_file = f_dir + input_file_geometry + '.dat'
"""

"""
#zyl-260x260-100-125-0
dim_x = 260
dim_y = 260
input_file_geometry = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-100-125-0'	
input_file = f_dir + input_file_geometry + '.dat'
"""

# read the file (line by line)
with open(input_file) as f:
	content = f.readlines()

#generate a list of the read content
read_array = list(content)

"""
initiate two arrays (one for the fixed values indicated by the star (*) and
one for the potential. The array marking the fixed potential values (potential_fix)
is realised using a mask, i.e., if the entry is one, the corresponding value
in potential_read may be subject to change.
"""
potential_read = [[0 for x in range(dim_x)] for y in range(dim_y)] # read file values
potential_fix = [[0 for x in range(dim_x)] for y in range(dim_y)]  # mask for fixed values

index_x = 0
index_y = 0

# parse the file into an array
for y in range(0, len(read_array)):
	value = ''
	for x in range(0, len(read_array[y])):
		if (read_array[y][x] == '*'):	# star (fixed value)
			potential_fix[index_y][index_x] = 1
		elif (read_array[y][x] != ' '): # a non-fixed value
			value += read_array[y][x]
		else:	# space -> write the value into the array
			if (value != ""):
				potential_read[index_y][index_x] = int(value)
				index_x += 1
			value = ''

	index_x = 0
	index_y += 1

def maximum_norm(U_ij_new, U_ij_old):
	""" Function which calculates the maximum norm between two iterations.

	This value is used to stop the iterative solver, i.e., it acts as a break
	condition. For each grid point, the maximum norm of the difference between
	two iterations (given by the function arguments) is calculated and the
	greatest value is returned by this function.
	"""
	r_ij_max = float('-inf')
	r_ij = 0.0

	for y in range(0, dim_y):
		for x in range(0, dim_x):
			r_ij = abs(U_ij_new[y][x] - U_ij_old[y][x])
			if (r_ij > r_ij_max):
				r_ij_max = r_ij

	return r_ij_max

iteration_counter = 0	# total number of iterations of the program

"""
the variable *skip_iterations* is used to reduce the number of iterations
saved. Output files for iterations (potential saved in the directory pot_out/
and its graphical visualisation saved in the folder gnuplot_figs/) are performed
each nth number with n being the variable *skip_iterations*. For example setting
this number to 3 means, each third iteration will be stored and out of these pictures
the animation will be created (and stored in the folder electric_field_and_animation/).
"""
skip_iterations = 1		# save a snapshot of every nth iteration
file_name_counter = 0	# total number of files (0 ... ~iteration_counter/skip_iterations)

stop_threshold = 1e-2	# stop the iterations when this threshold has been reached

# the potential after the finite difference iteration
potential_iteration = [[0 for x in range(dim_x)] for y in range(dim_y)]

"""
go through the geometry as defined by potential_read and potential_fix,
calculate an iteration which is stored in potential_iteration. After each iteration,
the maximum value of difference between two iterations is determined using
maximum_norm and if this value goes below the limit (defined by
stop_threshold), the iteration stops.
"""
while (True):
	"""
	use the finite difference method to solve the Laplace equation.
	The most outer values of the problem are ignored since these values
	are always fixed ones.
	"""
	for y in range(1, dim_y - 1):
		for x in range(1, dim_x - 1):
			if (potential_fix[y][x] != 1):	# potential values may be subject to change
				potential_iteration[y][x] = (
					0.25 * (
						potential_read[y + 1][x]
						+ potential_read[y - 1][x]
						+ potential_read[y][x + 1]
						+ potential_read[y][x - 1]
					)
				)
			else:
				potential_iteration[y][x] = potential_read[y][x]

	# maximum norm (between two iterations)
	rij_max = maximum_norm(potential_iteration, potential_read)
	sys.stdout.write(
		"\riteration: %i | file counter: %i | maximum norm: %f | stop threshold: %f"
		% (iteration_counter, file_name_counter, rij_max, stop_threshold)
	)
	sys.stdout.flush()

	# replace the values of the old iteration with the new ones
	for j in range(0, dim_y):
		for k in range(0, dim_x):
			potential_read[j][k] = potential_iteration[j][k]

	# write the potential of this iteration into a file
	if (iteration_counter % skip_iterations == 0):
		potential_output = open(
			folder_out + 'pot_' + input_file_geometry + '_'
			+ str(file_name_counter) + '.dat', "w"
		)

		for j in range(0, dim_y):
			for k in range(0, dim_x):
				print >> potential_output, k, '   ', j, '   ', potential_read[k][j]
			print >> potential_output

		potential_output.close()
		file_name_counter += 1

	iteration_counter += 1

	# stop the iteration if the accuracy has been reached
	if (rij_max < stop_threshold):
		break

print

# calculate and save the electric field
efield_animation_folder = 'electric_field_and_animation/'

electric_field_output_name = efield_animation_folder \
	+ input_file_geometry + '_electric_field.dat'
electric_field_output_file = open(electric_field_output_name, "w")

# calculate values of the electric field and write them to the file
for y in range(1, dim_y - 1):
	for x in range(1, dim_x - 1):
		print >> electric_field_output_file, x, '   ', y , '   ', \
			-(potential_iteration[x][y] - potential_iteration[x - 1][y]), \
			-(potential_iteration[x][y] - potential_iteration[x][y - 1])
	print >> electric_field_output_file

electric_field_output_file.close()


'''write the Gnuplot files which generate plots'''

# plot the electric field
file_plot_efeld = open(gnuplot_generator_dir + 'plot_electric_field.plt', "w")

print >> file_plot_efeld, 'set term png enhanced size 5000, 5000'
print >> file_plot_efeld, 'set output "' + efield_animation_folder \
	+ input_file_geometry + '_electric_field.png"'
print >> file_plot_efeld, 'e(x, y) = x / sqrt(x**2 + y**2)'
print >> file_plot_efeld, 'factor = 0.5'
print >> file_plot_efeld, 'xyf = 1'
print >> file_plot_efeld, 'set style arrow 1 head filled ' \
	+ ' size screen 1.03, 15 ls 2'
print >> file_plot_efeld, 'plot "' + electric_field_output_name + '" \
using ($2*xyf):($1*xyf):(e($4, $3)*factor):(e($3, $4)*factor) \
with vectors head filled size screen 0.01, 15 ls 4'

file_plot_efeld.close()

print "Generating the electric field"
system('gnuplot ' + gnuplot_generator_dir + 'plot_electric_field.plt')	# invoke gnuplot


# set up the animation gnuplot files -> multiplot.plt
file_multiplot = open(gnuplot_generator_dir + 'multiplot.plt', "w")

print >> file_multiplot, 'i = 1'
print >> file_multiplot, 'n = ', file_name_counter - 1
print >> file_multiplot, 'set terminal jpeg'
print >> file_multiplot, 'load "' + gnuplot_generator_dir + 'loop.plt"'

file_multiplot.close()

print

# -> loop.plt
file_loop = open(gnuplot_generator_dir + 'loop.plt', "w")

filename_gp = input_file_geometry + '.dat'

print >> file_loop, 'filename = "pot_out/pot_' \
	+ input_file_geometry +'_".i.".dat"'
print >> file_loop, 'plotfile = "gnuplot_figs/graph".i.".png"'
print >> file_loop, ''
print >> file_loop, 'set term png enhanced size 1280, 720'
print >> file_loop, 'set pm3d'
print >> file_loop, 'print "Fig: ", i, " / ", n, "\\r"'
print >> file_loop, '#set label 1'
print >> file_loop, 'set label 1 sprintf("i = %i",i) ' \
	+ 'left at screen 0.885, screen 0.85 font "arialbd, 20"'
print >> file_loop, '#set key default'
print >> file_loop, 'set title "' + filename_gp + '" font "arialbd, 25" noenhanced'
print >> file_loop, 'set palette'
print >> file_loop, 'set view 60, 120'
print >> file_loop, 'unset surface'
print >> file_loop, 'set pm3d at s scansforward'
print >> file_loop, ''
print >> file_loop, 'set output plotfile'
print >> file_loop, 'splot filename notitle'
print >> file_loop, ''
print >> file_loop, 'set output'
print >> file_loop, 'i = i + 1'
print >> file_loop, 'if (i <= n) reread'

file_loop.close()

print "Creating plots using Gnuplot"
system('gnuplot ' + gnuplot_generator_dir + 'multiplot.plt')	# invoke gnuplot to create the animation

print

"""
generate the animation of the program results using FFmpeg.
The option "-y" overwrites any possible file.
"""
print "Creating the video animation using FFmpeg"
system('ffmpeg -framerate 10 -i gnuplot_figs/graph%d.png -c:v libx264' \
	+ ' -preset 0 -crf 0 -r 30 -pix_fmt yuv420p ' \
	+ efield_animation_folder + input_file_geometry +'.mp4 -y')
