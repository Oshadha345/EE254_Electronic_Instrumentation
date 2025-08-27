clear all;
close all;

% Load signal processing package
pkg load signal;

% Read the signal and select first 100,000 samples
[x,Fs] = audioread('S:\Semester 4\EE254 - Instrumentation\My Work\EE254_Electronic_Instrumentation\problem_based_learning_activity_book\Noise shaping and OSR\danith.wav');
x = x(1:100000);
N = length(x);

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
Ns = length(ynew);

% Quantization without noise shaping (regular quantization)
xq = 0.5*(floor(x/0.5) + 0.5);

% Create subplots
figure;

% Subplot 1: Quantization noise spectrum (without noise shaping)
subplot(211);
quantization_noise = x - xq;
plot(abs(fftshift(fft(quantization_noise)))/(N/2));
title('Quantization noise (a). Without noise shaping');
xlabel('Frequency bin');
ylabel('Magnitude');
grid on;

% Subplot 2: Sigma-delta noise spectrum (with noise shaping)
subplot(212);
sigma_delta_noise = x - ynew;
plot(abs(fftshift(fft(sigma_delta_noise)))/(N/2));
title('Sigma-delta noise (b). With noise shaping');
xlabel('Frequency bin');
ylabel('Magnitude');
grid on;
