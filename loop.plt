filename = "pot_out/pot_pl_ko60x60_kreuz_".i.".dat"
plotfile = "gnuplot_figs/graph".i.".png"

set term png enhanced size 1280,720
set pm3d
print "Fig: ", i, " / ", n, "\r"
#set label 1
set label 1 sprintf("i = %i",i) left at screen 0.885, screen 0.85 font "arialbd,20"
#set key default
set title "pl_ko60x60_kreuz.dat" font "arialbd,25" noenhanced
set palette
set view 60, 120
unset surface
set pm3d at s scansforward

set output plotfile
splot filename notitle

set output
i=i+1
if (i <= n) reread
