import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Signal parameters
f0 = 5  # signal freq in Hz
T = 1  # duration in seconds
t_cont = np.linspace(0, T, 10000)  # fine time grid
x_cont = np.sin(2 * np.pi * f0 * t_cont)

# Sampling frequencies to test
fs_list = np.linspace(2 * f0 + 1, 20 * f0, 40)  # avoid exact Nyquist

# Define Lagrange interpolation
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

# For MSE tracking
mse_zoh = []
mse_li = []
mse_lagrange = []
mse_newton = []

for fs in fs_list:
    Ts = 1 / fs
    t_samples = np.arange(0, T + Ts, Ts)
    x_samples = np.sin(2 * np.pi * f0 * t_samples)

    # ZOH reconstruction
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

    # Compute MSE
    mse_zoh.append(np.mean((x_cont - x_zoh)**2))
    mse_li.append(np.mean((x_cont - x_li)**2))
    mse_lagrange.append(np.mean((x_cont - x_lag)**2))
    mse_newton.append(np.mean((x_cont - x_newt)**2))

# Choose a fixed fs to plot reconstructions
fs_fixed = 10  # Hz
Ts_fixed = 1 / fs_fixed
t_samples_fixed = np.arange(0, T + Ts_fixed, Ts_fixed)
x_samples_fixed = np.sin(2 * np.pi * f0 * t_samples_fixed)

# Reconstructions at fixed fs
indices_fixed = np.searchsorted(t_samples_fixed, t_cont, side='right') - 1
indices_fixed[indices_fixed < 0] = 0
x_zoh_fixed = x_samples_fixed[indices_fixed]

interp_func_fixed = interp1d(t_samples_fixed, x_samples_fixed, kind='linear', fill_value="extrapolate")
x_li_fixed = interp_func_fixed(t_cont)

x_lag_fixed = np.array([lagrange_interp(x, t_samples_fixed, x_samples_fixed) for x in t_cont])
coef_fixed = divided_diff(t_samples_fixed, x_samples_fixed)
x_newt_fixed = np.array([newton_poly(coef_fixed, t_samples_fixed, x) for x in t_cont])

# Plotting
fig, axs = plt.subplots(3, 2, figsize=(14, 12))
axs = axs.flatten()

# ZOH plot
axs[0].plot(t_cont, x_cont, 'k-', label='Original')
axs[0].step(t_cont, x_zoh_fixed, 'r-', where='post', label='ZOH')
axs[0].scatter(t_samples_fixed, x_samples_fixed, color='blue')
axs[0].set_title('Zero-Order Hold')
axs[0].legend()
axs[0].grid(True)

# Linear interp plot
axs[1].plot(t_cont, x_cont, 'k-', label='Original')
axs[1].plot(t_cont, x_li_fixed, 'g-', label='Linear')
axs[1].scatter(t_samples_fixed, x_samples_fixed, color='blue')
axs[1].set_title('Linear Interpolation')
axs[1].legend()
axs[1].grid(True)

# Lagrange plot
axs[2].plot(t_cont, x_cont, 'k-', label='Original')
axs[2].plot(t_cont, x_lag_fixed, 'm-', label='Lagrange')
axs[2].scatter(t_samples_fixed, x_samples_fixed, color='blue')
axs[2].set_title('Lagrange Interpolation')
axs[2].legend()
axs[2].grid(True)

# Newton plot
axs[3].plot(t_cont, x_cont, 'k-', label='Original')
axs[3].plot(t_cont, x_newt_fixed, 'c-', label='Newton')
axs[3].scatter(t_samples_fixed, x_samples_fixed, color='blue')
axs[3].set_title('Newton Interpolation')
axs[3].legend()
axs[3].grid(True)

# MSE plot (bottom-right)
axs[4].plot(fs_list, mse_zoh, 'r-o', label='ZOH')
axs[4].plot(fs_list, mse_li, 'g-o', label='Linear')
axs[4].plot(fs_list, mse_lagrange, 'm-o', label='Lagrange')
axs[4].plot(fs_list, mse_newton, 'c-o', label='Newton')
axs[4].set_xlabel('Sampling Frequency (Hz)')
axs[4].set_ylabel('Mean Square Error (MSE)')
axs[4].set_title('MSE vs Sampling Frequency')
axs[4].legend()
axs[4].grid(True)

# Hide the unused subplot (bottom-right corner)
axs[5].axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle('Interpolation Methods & MSE vs Sampling Frequency', fontsize=18)
plt.show()
