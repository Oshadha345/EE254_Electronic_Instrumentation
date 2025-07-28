R = 1e3;
C = 0.1e-6;
f = logspace(0,7.3,1000);
w = 2*pi*f;

T = j*w*R*C ./ (J*w*R*C + 1 ) ;


subplot(2,1,1);
semilogx(f, 20*log10(abs(T)));
grid on;
xlabel('Frequency (Hz)');
ylabel('Magnitude (dB)');
title('RC High Pass Filter - Bode Magnitude');

subplot(2,1,2);
semilogx(f,angle(T)*180/pi);
grid on;
xlabel('Frequency (Hz)');
ylabel('Phase (degrees)');
title('RC High Pass Filter - Bode Magnitude');
