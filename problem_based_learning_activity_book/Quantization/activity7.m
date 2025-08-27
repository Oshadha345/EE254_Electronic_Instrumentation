clear all;
close all;
dx=0.001; % step size
x_min=-1; % minimum value of x
x_max=1; % maximum value of x
x=x_min:dx:x_max-dx; % create x
N=3; % Number of bits
q=(x_max-x_min)/(2^N);
xq=q*(floor(x/q)+0.5);
plot(x,xq,'k','LineWidth',4);
xlabel('input signal (x)');
ylabel('quantized signal (xq)');
grid on;
axis square;

