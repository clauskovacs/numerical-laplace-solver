# E-Feld
sf=2000.
e(x,y)=x/sqrt(x**2+y**2)

lf=10.
xyf=1000.


plot 'gradient.tmp' u ($1*xyf):($2*xyf):(e($3,$4)/lf):(e($4,$3)/lf) w vec
pause -1
