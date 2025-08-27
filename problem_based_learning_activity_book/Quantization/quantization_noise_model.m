x_max=1;x_min=-1;
N=4;
q=(x_max-x_min)/(2^N);
x=1-2*rand(10000,1);
xq=q*(floor(x/q)+0.5);
qe=x-xq;
[h,scl]=hist(qe,10);
figure;bar(scl,h);
xlabel('quantization region');
ylabel('Frequency of occurrance');
% Quantization oise power
NP_m=std(qe)^2; % measured value
NP_c=(q^2)/12;
[NP_m NP_c]

