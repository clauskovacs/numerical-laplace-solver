set term png enhanced size 5000,5000
set output "electric_field_and_animation/pl_ko60x60_kreuzaefeld.png"
e(x,y)=x/sqrt(x**2+y**2)
factor = 0.5
xyf = 1
set style arrow 1 head filled size screen 1.03,15 ls 2
plot "efeld.dat" using ($2*xyf):($1*xyf):(e($4,$3)*factor):(e($3,$4)*factor) with vectors head filled size screen 0.01,15 ls 4
