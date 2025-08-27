f_c = 1000;
order = 4;
w_c = 2*pi*f_c;

% Butterworth
[nb, db] = butter(order, w_c, "s");
Hb = tf(nb, db);

% Bessel
[nbes, dbes] = besself(order, w_c);
Hbes = tf(nbes, dbes);

% Chebyshev I (0.5 dB ripple)
[nc1, dc1] = cheby1(order, 0.5, w_c, "s");
Hc1 = tf(nc1, dc1);

% Compare magnitude response
f = logspace(2, 5, 1000);
w = 2 * pi * f;

Hb_mag = freqs(nb, db, w);
Hbes_mag = freqs(nbes, dbes, w);
Hc1_mag = freqs(nc1, dc1, w);

semilogx(f, 20*log10(abs(Hb_mag)), "b", ...
         f, 20*log10(abs(Hbes_mag)), "g", ...
         f, 20*log10(abs(Hc1_mag)), "r");
grid on;
legend("Butterworth", "Bessel", "Chebyshev I");
xlabel("Frequency (Hz)");
ylabel("Magnitude (dB)");
title("Filter Type Comparison");

