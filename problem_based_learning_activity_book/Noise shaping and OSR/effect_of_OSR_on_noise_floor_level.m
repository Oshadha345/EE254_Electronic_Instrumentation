clear all;
close all;
% Quantization parameters
x_max=1;
N=1;
q=2*x_max/2^N;
% Read the signal
pkg load signal;  % Load signal processing package for resample
[x,Fs]=audioread('S:\Semester 4\EE254 - Instrumentation\My Work\EE254_Electronic_Instrumentation\problem_based_learning_activity_book\Noise shaping and OSR\danith.wav');
x=x(1:100000); % select first 100k samples

% Define colors for different OSR values
colors = {'r', 'b', 'g', 'm', 'c', 'k', 'y', [0.5 0.5 0.5], [0.8 0.4 0], [0.4 0.8 0.4]};
legend_entries = {};

figure;
for OSR=1:10
 xr=resample(x,OSR*Fs,Fs);
 xq=q*(floor(xr/q)+0.5);
 [Pxq,F]=pburg(xq,4);
 %plot(F,20*log10(Pxr),'k');hold on;drawnow;
 plot(F,10*log10(Pxq),'Color',colors{OSR},'LineWidth',1.5);hold on;drawnow;
 legend_entries{OSR} = sprintf('OSR = %d', OSR);
end
xlabel('Frequency (Hz)');
ylabel('Power Spectral Density (dB)');
title('Effect of Oversampling Ratio (OSR) on Quantization Noise Floor');
legend(legend_entries, 'Location', 'best');
grid on;
