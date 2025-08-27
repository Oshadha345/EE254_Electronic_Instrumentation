import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Parameters
f0 = 5  # signal frequency in Hz
T = 1  # signal duration in seconds
t_cont = np.linspace(0, T, 10000)  # fine time grid for "continuous" signal

# Original continuous-time signal
x_cont = np.sin(2 * np.pi * f0 * t_cont)

# Sampling frequencies to test (from Nyquist to 20*f0)
fs_list = np.linspace(2 * f0 + 1, 20 * f0, 10000)  # avoid exactly Nyquist freq to prevent aliasing edge

mse_zoh = []
mse_li = []

for fs in fs_list:
    Ts = 1 / fs
    t_samples = np.arange(0, T + Ts, Ts)
    x_samples = np.sin(2 * np.pi * f0 * t_samples)

    # Zero-order hold reconstruction
    # For each point in t_cont, find the index of the last sample before it
    indices = np.searchsorted(t_samples, t_cont, side='right') - 1
    indices[indices < 0] = 0  # for t < first sample
    x_zoh = x_samples[indices]

    # Linear interpolation reconstruction
    interp_func = interp1d(t_samples, x_samples, kind='linear', fill_value="extrapolate")
    x_li = interp_func(t_cont)

    # Calculate MSE
    mse_zoh.append(np.mean((x_cont - x_zoh) ** 2))
    mse_li.append(np.mean((x_cont - x_li) ** 2))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(fs_list, mse_zoh, label='Zero-Order Hold')
plt.plot(fs_list, mse_li, label='Linear Interpolation')
plt.xlabel('Sampling Frequency (Hz)')
plt.ylabel('Mean Square Error (MSE)')
plt.title('MSE vs Sampling Frequency for ZOH and Linear Interpolation')
plt.legend()
plt.grid(True)
plt.show()
