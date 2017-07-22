# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
from os import system, remove	# shell commands from python

def calculate_r_ij(U_ij_neu, U_ij_alt):
	r_ij_max = -10.0
	r_ij = 0.0

	for y in range(0, dim_y):
		for x in range(0, dim_x):
			r_ij = abs(U_ij_neu[y][x] - U_ij_alt[y][x])
			if (r_ij > r_ij_max):
				r_ij_max = r_ij

	return r_ij_max

f_dir = 'laplace_files/'

# pl_ko30x30.dat
"""
dim_x = 30
dim_y = 30
fname_file = 'pl_ko' + str(dim_x) + 'x' + str(dim_y)
fname = f_dir + fname_file + '.dat'
"""

#zyl-100x100-20-49-0.dat
"""
dim_x = 100
dim_y = 100
fname_file = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-20-49-0'
fname = f_dir + fname_file + '.dat'
"""

#loch_ko60x60.dat.dat
"""
dim_x = 60
dim_y = 60
fname_file = 'loch_ko' + str(dim_x) + 'x' + str(dim_y) + ''
fname = f_dir + fname_file + '.dat'
"""

#dach_l_ko60x60.dat
"""
dim_x = 60
dim_y = 60
fname_file = 'dach_l_ko' + str(dim_x) + 'x' + str(dim_y) + ''
fname = f_dir + fname_file + '.dat'
"""

#zyl_1040x1040_400_500_0.dat
"""
dim_x = 1040
dim_y = 1040
fname_file = 'zyl_' + str(dim_x) + 'x' + str(dim_y) + '_400_500_0'
fname = f_dir + fname_file + '.dat'
"""

#dach_ko60x60.dat
"""
dim_x = 60
dim_y = 60
fname_file = 'dach_ko' + str(dim_x) + 'x' + str(dim_y)
fname = f_dir + fname_file + '.dat'
"""

#zyl-100x100-40-50-0.dat
"""
dim_x = 100
dim_y = 100
fname_file = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-40-50-0'	
fname = f_dir + fname_file + '.dat'
"""

#zyl-100x100-20-49-0.dat
"""
dim_x = 100
dim_y = 100
fname_file = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-20-49-0'	
fname = f_dir + fname_file + '.dat'
"""

#zyl-200x200-40-98-40.dat
"""
dim_x = 200
dim_y = 200
fname_file = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-40-98-40'	
fname = f_dir + fname_file + '.dat'
"""

#pl_ko60x60_kreuz.dat

dim_x = 60
dim_y = 60
fname_file = 'pl_ko' + str(dim_x) + 'x' + str(dim_y) + '_kreuz'	
fname = f_dir + fname_file + '.dat'

#zyl-260x260-100-125-0
"""
dim_x = 260
dim_y = 260
fname_file = 'zyl-' + str(dim_x) + 'x' + str(dim_y) + '-100-125-0'	
fname = f_dir + fname_file + '.dat'
"""

with open(fname) as f:
	content = f.readlines() # Zeilenweises einlesen

read_array = list(content) # generiere Liste -> string Liste ; Listenarray

Pot_read = [[0 for x in range(dim_x)] for y in range(dim_y)] # Potential aus der Datei
Pot_fix = [[0 for x in range(dim_x)] for y in range(dim_y)]  # Fixierte Potentialwerte (Rand, Potentialwerte, ...)

index_x = 0
index_y = 0

# parse the file into an array
for y in range(0, len(read_array)): # Anzahl der Zeilen in der Liste
	wert = ''
	for x in range(0, len(read_array[y])): # len(read_array[1]) ... Anz. Zeichen in der Zeile der Liste
		if (read_array[y][x] == '*'):   # STERN
			Pot_fix[index_y][index_x] = 1
		elif (read_array[y][x] != ' '): # ZAHL
			wert += read_array[y][x]
		else:                           # LEERZEICHEN
			if (wert != ""):
				Pot_read[index_y][index_x] = int(wert)
				index_x += 1
			wert = ''

	index_x = 0
	index_y += 1
# parse the file into an array

Pot_read_new = [[0 for x in range(dim_x)] for y in range(dim_y)] # neues Potential

#U_ij = Pot_read
#U_ij^neu = Pot_read_new

folder_out = 'pot_out/'

var = 1
i = 0

file_p_counter = 0
file_name_counter = 0

stop_threshold = 1e-1

while (var == 1):
	# Laplace (Iteration)
	for y in range(1, dim_y-1):		# 1 - dim_y-1 ... Rand ignorieren
		for x in range(1, dim_x-1):	# 1 - dim_x-1 ... Rand ignorieren
			if (Pot_fix[y][x] != 1):	# Potential kann verändert werden != 1
	#			sys.stdout.write(str( Pot_read_new[y][x]) + ' ')
				Pot_read_new[y][x] = 0.25 * (Pot_read[y+1][x] + Pot_read[y-1][x] + Pot_read[y][x+1] + Pot_read[y][x-1])
			else:
				Pot_read_new[y][x] = Pot_read[y][x]
	# Laplace (Iteration)

	# maximum deviation (U_ij <-> U_ij^neu)
	rij_max = calculate_r_ij(Pot_read_new, Pot_read)
	sys.stdout.write("\ri:%i | %i  ||   MAX:%f | %f" % (i, file_name_counter, rij_max, stop_threshold))
	sys.stdout.flush()
	# maximum deviation (U_ij <-> U_ij^neu)

	# file IO
	for j in range(0, dim_y):
		for k in range(0, dim_x):
			Pot_read[j][k] = Pot_read_new[j][k]
	# copy the grid

	# Potential in Datei ausgeben
	if (file_p_counter == 0): # Großes Gitter -> nicht jede Iteration in eine Textdatei speichern (Festplattenspeicher, "Veränderung ist klein(Propagation)" -> 0 ... jede Iteration speichern, 1 ... jede 2-te, ...
		folder_out = 'pot_out/'
		pot_output = open(folder_out + 'pot_' + fname_file + '_' + str(file_name_counter) + '.dat', "w")

		for j in range(0, dim_y):
			for k in range(0, dim_x):
				print >> pot_output, k, '   ',j, '   ', Pot_read[k][j]
			print >> pot_output

		pot_output.close()
		file_name_counter+=1

		file_p_counter = 0 # reset the counter
	else:
		file_p_counter+=1
	# file IO

	i+=1

	if (rij_max < stop_threshold): # Genauigkeit erreicht -> abbrechen
		break

print

# gen the electric field

folder_out = ''

#pot_output = open(folder_out + 'efeld_' + fname_file + '_' + str(file_name_counter) + '.dat', "w")

pot_output = open('efeld.dat', "w")

for y in range(1, dim_y-1):
	for x in range(1, dim_x-1):
		print >> pot_output, x, '   ',y , '   ', -(Pot_read_new[x][y]-Pot_read_new[x-1][y]), -(Pot_read_new[x][y]-Pot_read_new[x][y-1])
	print >> pot_output

pot_output.close()
# gen the electric field


# Gnuplot - gen plots
file_plot_efeld = open('plot_ef.plt', "w")

print >> file_plot_efeld, 'set term png enhanced size 5000,5000'
print >> file_plot_efeld, 'set output "'+ fname_file +'efeld.png"'
print >> file_plot_efeld, 'e(x,y)=x/sqrt(x**2+y**2)'
print >> file_plot_efeld, 'factor = 0.5'
print >> file_plot_efeld, 'xyf = 1'
print >> file_plot_efeld, 'set style arrow 1 head filled size screen 1.03,15 ls 2'
print >> file_plot_efeld, 'plot "efeld.dat" using ($2*xyf):($1*xyf):(e($4,$3)*factor):(e($3,$4)*factor) with vectors head filled size screen 0.01,15 ls 4'

file_plot_efeld.close()
# Gnuplot - gen plots

print "gen E-field"
system('gnuplot plot_ef.plt')

# GNUPLOT
# multiplot.plt
file_multiplot = open('multiplot.plt', "w")

print >> file_multiplot, 'i = 1'
print >> file_multiplot, 'n = ', file_name_counter-1
print >> file_multiplot, 'set terminal jpeg'
print >> file_multiplot, 'load "loop.plt"'

file_multiplot.close()
# multiplot.plt

print

# loop.plt
file_loop = open('loop.plt', "w")

filename_gp = fname_file + '.dat'

print >> file_loop, 'filename = "pot_out/pot_'+ fname_file +'_".i.".dat"'
print >> file_loop, 'plotfile = "gnuplot_figs/graph".i.".png"'
print >> file_loop, ''
print >> file_loop, 'set term png enhanced size 1280,720'
print >> file_loop, 'set pm3d'
print >> file_loop, 'print "Fig: ", i, " / ", n, "\\r"'
print >> file_loop, '#set label 1'
print >> file_loop, 'set label 1 sprintf("i = %i",i) left at screen 0.885, screen 0.85 font "arialbd,20"'
print >> file_loop, '#set key default'
print >> file_loop, 'set title "' + filename_gp + '" font "arialbd,25" noenhanced'
print >> file_loop, 'set palette'
print >> file_loop, 'set view 60, 120'
print >> file_loop, 'unset surface'
print >> file_loop, 'set pm3d at s scansforward'
print >> file_loop, ''
print >> file_loop, 'set output plotfile'
print >> file_loop, 'splot filename notitle'
print >> file_loop, ''
print >> file_loop, 'set output'
print >> file_loop, 'i=i+1'
print >> file_loop, 'if (i <= n) reread'

file_loop.close()
# loop.plt
# GNUPLOT

print "creating plots using gnuplot"
system('gnuplot multiplot.plt')

print

print "creating the Video"
system('ffmpeg -framerate 10 -i gnuplot_figs/graph%d.png -c:v libx264 -preset 0 -crf 0 -r 30 -pix_fmt yuv420p '+ fname_file +'.mp4 -y') # -y -> überschreibt die alte Datei