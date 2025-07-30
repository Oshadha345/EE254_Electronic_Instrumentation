pkg load control signal;

% Design parameters
f_c = 1000;        % Cutoff frequency in Hz
order = 2;
w_c = 2*pi*f_c;    % Convert to rad/s

% Design Butterworth analog filter
[num, den] = butter(order, w_c, "s");
H = tf(num, den);

% Bode plot
bode(H); grid on;
title("Butterworth Low-Pass Filter");

