clear all;
close all;

% Load signal processing package
pkg load signal;

% Read the signal and select first 100,000 samples
[x,Fs] = audioread('S:\Semester 4\EE254 - Instrumentation\My Work\EE254_Electronic_Instrumentation\problem_based_learning_activity_book\Noise shaping and OSR\danith.wav');
x = x(1:100000);
N = length(x);

% Regular quantization (1-bit)
xq = 0.5*(floor(x/0.5) + 0.5);

% Sigma-Delta ADC implementation  
y = 0;
ynew = zeros(N,1);
for k = 1:N
    u = x(k) - y;
    if u > 0
        ynew(k) = 0.5;
    else
        ynew(k) = -0.5;
    end
    y = ynew(k);
end

% Design Butterworth lowpass filter and observe the effect
[b,a] = butter(8, 0.05);  % 8th order, cutoff at 0.05 normalized frequency
xf = filter(b, a, xq);    % Filter regular quantized signal
yf = filter(b, a, ynew);  % Filter sigma-delta quantized signal

% Plot results
figure;
subplot(3,1,1);
plot(x, 'k', 'LineWidth', 1);
hold on;
title('Original Signal');
xlabel('Sample');
ylabel('Amplitude');
grid on;

subplot(3,1,2);
plot(xf, 'r', 'LineWidth', 1);
hold on;
title('Filtered signals (a). Normally quantized');
xlabel('Sample');
ylabel('Amplitude');
grid on;

subplot(3,1,3);
plot(yf, 'b', 'LineWidth', 1);
hold on;
title('Filtered signals (b). Sigma-Delta quantized');
xlabel('Sample');
ylabel('Amplitude');
grid on;

% Change cutoff frequency and experiment
% until the quality of the reconstructed
% signals improves to a satisfactory level
fprintf('Experiment with different cutoff frequencies:\n');
fprintf('Try values like 0.01, 0.02, 0.05, 0.1, 0.2\n');
fprintf('Lower cutoff = better noise removal but more signal distortion\n');
fprintf('Higher cutoff = less noise removal but better signal preservation\n');