 clear all; close all; clc;

% Read audio file
[y, Fs] = audioread('danith.wav');

% Get info (Octave doesn't have audioinfo, so use length and Fs)
L = length(y); % total samples
duration = L / Fs; % in seconds

% Time vector
t = (0:L-1) / Fs;

% Time domain plot
figure(1);
subplot(2,1,1);
plot(t, y);
xlabel('Time (s)');
ylabel('Audio Signal');

% Compute the FT of the signal
Y = fft(y);
P2 = abs(Y/L);
P1 = P2(1:floor(L/2)+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:floor(L/2))/L;

% Frequency domain plot
subplot(2,1,2);
plot(f, P1);
title('Single-sided Amplitude Spectrum of y(t)');
xlabel('Frequency (Hz)');
ylabel('|P1(f)|');

% Play sound
disp('Press any key to play the audio...');
pause;
sound(y, Fs);

disp('Press any key to continue...');
pause;

