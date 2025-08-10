import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Signal parameters
f0 = 5  # signal freq in Hz
T = 1   # duration in seconds
t_cont = np.linspace(0, T, 10000)  # fine grid for continuous signal
x_cont = np.sin(2 * np.pi * f0 * t_cont)

# Sampling frequencies to test
fs_list = np.linspace(2 * f0 + 1, 20 * f0, 40)  # avoid exact Nyquist

# Lagrange interpolation function
def lagrange_interp(x, x_points, y_points):
    total = 0
    n = len(x_points)
    for i in range(n):
        xi, yi = x_points[i], y_points[i]
        Li = 1
        for j in range(n):
            if j != i:
                Li *= (x - x_points[j]) / (xi - x_points[j])
        total += yi * Li
    return total

# Newton interpolation helpers
def divided_diff(x_points, y_points):
    n = len(x_points)
    coef = np.copy(y_points).astype(float)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j-1:n-1]) / (x_points[j:n] - x_points[0:n-j])
    return coef

def newton_poly(coef, x_points, x):
    n = len(coef)
    result = coef[-1]
    for k in range(n - 2, -1, -1):
        result = result * (x - x_points[k]) + coef[k]
    return result

# Prepare MSE lists
mse_zoh = []
mse_li = []
mse_lagrange = []
mse_newton = []

# Calculate MSE for each method over sampling frequencies
for fs in fs_list:
    Ts = 1 / fs
    t_samples = np.arange(0, T + Ts, Ts)
    x_samples = np.sin(2 * np.pi * f0 * t_samples)

    # Zero-order hold
    indices = np.searchsorted(t_samples, t_cont, side='right') - 1
    indices[indices < 0] = 0
    x_zoh = x_samples[indices]

    # Linear interpolation
    interp_func = interp1d(t_samples, x_samples, kind='linear', fill_value="extrapolate")
    x_li = interp_func(t_cont)

    # Lagrange interpolation
    x_lag = np.array([lagrange_interp(x, t_samples, x_samples) for x in t_cont])

    # Newton interpolation
    coef = divided_diff(t_samples, x_samples)
    x_newt = np.array([newton_poly(coef, t_samples, x) for x in t_cont])

    # MSE calculations
    mse_zoh.append(np.mean((x_cont - x_zoh) ** 2))
    mse_li.append(np.mean((x_cont - x_li) ** 2))
    mse_lagrange.append(np.mean((x_cont - x_lag) ** 2))
    mse_newton.append(np.mean((x_cont - x_newt) ** 2))

# Plot all MSEs on one figure
plt.figure(figsize=(10, 6))
plt.plot(fs_list, mse_zoh, 'r-o', label='Zero-Order Hold')
plt.plot(fs_list, mse_li, 'g-x', label='Linear Interpolation')
plt.plot(fs_list, mse_lagrange, 'm-s', label='Lagrange Interpolation')
plt.plot(fs_list, mse_newton, 'c-d', label='Newton Interpolation')
plt.xlabel('Sampling Frequency (Hz)')
plt.ylabel('Mean Square Error (MSE)')
plt.title('MSE vs Sampling Frequency for Various Interpolation Methods')
plt.legend()
plt.grid(True)
plt.show()
