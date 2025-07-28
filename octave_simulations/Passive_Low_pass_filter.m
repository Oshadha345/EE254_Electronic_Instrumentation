R = 1e3;  % 1 kOhm
C = 0.1e-6;  % 0.1 uF
f = logspace(1, 6, 1000); % frequency from 10 Hz to 1 MHz
w = 2 * pi * f;
H = 1 ./ (1 + j*w*R*C);

% Plot Magnitude and Phase
subplot(2,1,1);
semilogx(f, 20*log10(abs(H)));
grid on;
xlabel('Frequency (Hz)');
ylabel('Magnitude (dB)');
title('RC Low Pass Filter - Bode Magnitude');

subplot(2,1,2);
semilogx(f, angle(H) * 180/pi);
grid on;
xlabel('Frequency (Hz)');
ylabel('Phase (degrees)');
title('RC Low Pass Filter - Bode Phase');

