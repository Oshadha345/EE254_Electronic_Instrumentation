% low pass filter characterization


% H(s) = 1/(1+sRC)  <--- transfer function

R = 1e3; % 1kOhm

c = 0.1e-6; %0.1uF

f = logspace(1,6,1000); % frequecy from 10Hz to 1MHz

w = 2*pi*f;

H = 1 / ( 1 + j*w*R*C);


%plot magnitude and phase
subplot(2,1,1);
semilogx(f, 20*log10(abs(H)));
grid on;
xlabel('Frequency(Hz)');
ylabel('Magnitude(dB)');
title('RC low pass filter - Bode Magnitude');

subplot(2,1,2);
semilogx(f, angle(H)*180/pi);
grid on;
xlabel('Frequency (Hz)');
ylabel('Phase (degrees)');
title('RC Low Pass Filter - Bode Phase');
