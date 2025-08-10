import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Original signal
def signal(t):
    return np.sin(3*t) + 0.5 * np.cos(5*t)

# Sampling points
t_start, t_end = 0, 2 * np.pi
n_samples = 20
t_samples = np.linspace(t_start, t_end, n_samples)
y_samples = signal(t_samples)

# Fine grid for "original" signal plot
t_fine = np.linspace(t_start, t_end, 1000)
y_fine = signal(t_fine)

# 1. Zero-order hold
def zero_order_hold(t_query, t_samples, y_samples):
    idx = np.searchsorted(t_samples, t_query, side='right') - 1
    idx[idx < 0] = 0
    return y_samples[idx]

# 2. Linear interpolation using scipy interp1d
linear_interp = interp1d(t_samples, y_samples, kind='linear', fill_value="extrapolate")

# 3. Lagrange interpolation
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

# 4. Newton interpolation
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

coefficients = divided_diff(t_samples, y_samples)

# Calculate interpolated values on fine grid
y_zoh = zero_order_hold(t_fine, t_samples, y_samples)
y_linear = linear_interp(t_fine)
y_lagrange = np.array([lagrange_interp(x, t_samples, y_samples) for x in t_fine])
y_newton = np.array([newton_poly(coefficients, t_samples, x) for x in t_fine])

# Plot all methods
fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)

# ZOH
axs[0, 0].plot(t_fine, y_fine, 'k-', label='Original Signal')
axs[0, 0].step(t_fine, y_zoh, 'r-', where='post', label='Zero-Order Hold')
axs[0, 0].scatter(t_samples, y_samples, color='blue')
axs[0, 0].set_title('Zero-Order Hold')
axs[0, 0].legend()
axs[0, 0].grid(True)

# Linear Interpolation
axs[0, 1].plot(t_fine, y_fine, 'k-', label='Original Signal')
axs[0, 1].plot(t_fine, y_linear, 'g-', label='Linear Interpolation')
axs[0, 1].scatter(t_samples, y_samples, color='blue')
axs[0, 1].set_title('Linear Interpolation')
axs[0, 1].legend()
axs[0, 1].grid(True)

# Lagrange Interpolation
axs[1, 0].plot(t_fine, y_fine, 'k-', label='Original Signal')
axs[1, 0].plot(t_fine, y_lagrange, 'm-', label='Lagrange Interpolation')
axs[1, 0].scatter(t_samples, y_samples, color='blue')
axs[1, 0].set_title('Lagrange Interpolation')
axs[1, 0].legend()
axs[1, 0].grid(True)

# Newton Interpolation
axs[1, 1].plot(t_fine, y_fine, 'k-', label='Original Signal')
axs[1, 1].plot(t_fine, y_newton, 'c-', label='Newton Interpolation')
axs[1, 1].scatter(t_samples, y_samples, color='blue')
axs[1, 1].set_title('Newton Interpolation')
axs[1, 1].legend()
axs[1, 1].grid(True)

plt.suptitle('Interpolation Methods Comparison\nSignal: sin(3t) + 0.5cos(5t) with {} samples'.format(n_samples), fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
