// A simple plot of z = f(x,y)
t=[0:0.3:2*%pi]'; 
z=sin(t)*cos(t');
plot3d(t,t,z);
xs2eps(0, 'output.eps');
quit();
