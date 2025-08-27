import numpy as np
import matplotlib.pyplot as plt

# Activity 4-6: Mid-tread Quantizer Implementation and Analysis
def mid_tread_quantizer(x, N, x_min=-1, x_max=1):
    """N-bit mid-tread quantizer"""
    q = (x_max - x_min) / (2**N)
    xq = q * np.floor((x / q) + 0.5)
    return xq, q

def mid_riser_quantizer(x, N, x_min=-1, x_max=1):
    """N-bit mid-riser quantizer"""
    q = (x_max - x_min) / (2**N)
    xq = q * (np.floor(x / q) + 0.5)
    return xq, q

def plot_quantizer_characteristics():
    """Plot input-output characteristics for both quantizer types"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12), constrained_layout=True)
    
    # Input signal range
    x = np.linspace(-1, 1, 10000)
    
    # 2-bit and 3-bit quantizers
    for i, N in enumerate([2, 3]):
        # Mid-tread quantizer
        xq_tread, q_tread = mid_tread_quantizer(x, N)
        
        axes[0, i].plot(x, xq_tread, 'b-', linewidth=2, label=f'{N}-bit Mid-tread')
        axes[0, i].plot(x, x, 'k--', alpha=0.5, label='Ideal (x=x)')
        axes[0, i].set_xlabel('Input (x)')
        axes[0, i].set_ylabel('Output (xq)')
        axes[0, i].set_title(f'{N}-bit Mid-tread Quantizer')
        axes[0, i].grid(True, alpha=0.3)
        axes[0, i].legend()
        axes[0, i].set_xlim(-1, 1)
        
        # Add quantization levels and binary codes
        levels = np.arange(-2**(N-1), 2**(N-1)) * q_tread
        for j, level in enumerate(levels):
            if abs(level) <= 1:
                binary = format(j, f'0{N}b') if j < 2**N else format(2**N-1, f'0{N}b')
                axes[0, i].axhline(y=level, color='red', alpha=0.3, linestyle=':')
                if i == 1:  # Only label for 3-bit
                    axes[0, i].text(0.8, level, binary, fontsize=8, 
                                  bbox=dict(boxstyle="round,pad=0.1", facecolor="white", alpha=0.8))
        
        # Mid-riser quantizer
        xq_riser, q_riser = mid_riser_quantizer(x, N)
        
        axes[1, i].plot(x, xq_riser, 'r-', linewidth=2, label=f'{N}-bit Mid-riser')
        axes[1, i].plot(x, x, 'k--', alpha=0.5, label='Ideal (x=x)')
        axes[1, i].set_xlabel('Input (x)')
        axes[1, i].set_ylabel('Output (xq)')
        axes[1, i].set_title(f'{N}-bit Mid-riser Quantizer')
        axes[1, i].grid(True, alpha=0.3)
        axes[1, i].legend()
        axes[1, i].set_xlim(-1, 1)
        
        # Add quantization levels for mid-riser
        levels_riser = (np.arange(-2**(N-1), 2**(N-1)) + 0.5) * q_riser
        for j, level in enumerate(levels_riser):
            if abs(level) <= 1:
                axes[1, i].axhline(y=level, color='red', alpha=0.3, linestyle=':')
    
    plt.show()

# Activity 8-9: Quantization Noise Analysis
def analyze_quantization_noise():
    """Analyze quantization noise properties"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
    
    # Generate random signal
    np.random.seed(42)
    x = 2 * np.random.rand(10000) - 1  # Random signal in [-1, 1]
    
    N = 4  # 4-bit quantizer
    xq, q = mid_riser_quantizer(x, N)
    qe = x - xq  # Quantization error
    
    # Histogram of quantization error
    axes[0, 0].hist(qe, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].axvline(-q/2, color='red', linestyle='--', label=f'-q/2 = {-q/2:.4f}')
    axes[0, 0].axvline(q/2, color='red', linestyle='--', label=f'+q/2 = {q/2:.4f}')
    axes[0, 0].axhline(1/q, color='green', linestyle='--', label=f'1/q = {1/q:.2f}')
    axes[0, 0].set_xlabel('Quantization Error')
    axes[0, 0].set_ylabel('Probability Density')
    axes[0, 0].set_title('Quantization Error Distribution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Noise power verification
    NP_measured = np.var(qe)
    NP_theoretical = (q**2) / 12
    
    axes[0, 1].bar(['Measured', 'Theoretical'], [NP_measured, NP_theoretical], 
                   color=['blue', 'red'], alpha=0.7)
    axes[0, 1].set_ylabel('Noise Power')
    axes[0, 1].set_title(f'Quantization Noise Power\nMeasured: {NP_measured:.6f}\nTheoretical: {NP_theoretical:.6f}')
    axes[0, 1].grid(True, alpha=0.3)
    
    # SQNR Analysis for different bit depths
    N_values = np.arange(1, 17)
    sqnr_measured = []
    sqnr_theoretical = []
    
    for N in N_values:
        xq_temp, q_temp = mid_riser_quantizer(x, N)
        qe_temp = x - xq_temp
        
        sqnr_m = 20 * np.log10(np.std(x) / np.std(qe_temp))
        sqnr_t = 6.02 * N + 1.76
        
        sqnr_measured.append(sqnr_m)
        sqnr_theoretical.append(sqnr_t)
    
    axes[1, 0].plot(N_values, sqnr_measured, 'bo-', label='Measured SQNR', markersize=6)
    axes[1, 0].plot(N_values, sqnr_theoretical, 'r^-', label='Theoretical SQNR', markersize=6)
    axes[1, 0].set_xlabel('Number of Bits (N)')
    axes[1, 0].set_ylabel('SQNR (dB)')
    axes[1, 0].set_title('SQNR vs Number of Bits')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Quantization effect visualization
    t = np.linspace(0, 1, 1000)
    x_sine = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave
    
    for i, N in enumerate([2, 8]):
        xq_sine, _ = mid_tread_quantizer(x_sine, N)
        if i == 0:
            axes[1, 1].plot(t[:200], x_sine[:200], 'k-', linewidth=2, label='Original')
            axes[1, 1].plot(t[:200], xq_sine[:200], 'b-', linewidth=2, label=f'{N}-bit Quantized')
        else:
            axes[1, 1].plot(t[:200], xq_sine[:200], 'r--', linewidth=2, label=f'{N}-bit Quantized')
    
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Amplitude')
    axes[1, 1].set_title('Effect of Quantization on Sine Wave')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.show()
    
    return NP_measured, NP_theoretical, sqnr_measured[-1], sqnr_theoretical[-1]

# Activity 4: Aliasing demonstration
def demonstrate_aliasing():
    """Demonstrate aliasing effect with different sampling rates"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
    
    # Original signal parameters
    f_signal = 50  # 50 Hz signal
    t_continuous = np.linspace(0, 0.2, 2000)
    x_continuous = np.sin(2 * np.pi * f_signal * t_continuous)
    
    # Different sampling frequencies
    fs_values = [80, 120]  # Below and above Nyquist (100 Hz)
    
    for i, fs in enumerate(fs_values):
        # Sample the signal
        t_sample = np.arange(0, 0.2, 1/fs)
        x_sample = np.sin(2 * np.pi * f_signal * t_sample)
        
        # Reconstruct using linear interpolation
        x_reconstructed = np.interp(t_continuous, t_sample, x_sample)
        
        axes[i, 0].plot(t_continuous, x_continuous, 'k-', linewidth=2, label='Original 50Hz')
        axes[i, 0].plot(t_continuous, x_reconstructed, 'r--', linewidth=2, 
                       label=f'Reconstructed (fs={fs}Hz)')
        axes[i, 0].plot(t_sample, x_sample, 'ro', markersize=6, label='Sample points')
        axes[i, 0].set_xlabel('Time (s)')
        axes[i, 0].set_ylabel('Amplitude')
        axes[i, 0].set_title(f'Sampling at {fs} Hz ({"Above" if fs > 100 else "Below"} Nyquist)')
        axes[i, 0].legend()
        axes[i, 0].grid(True, alpha=0.3)
        
        # Frequency domain analysis
        X_fft = np.fft.fft(x_reconstructed)
        freqs = np.fft.fftfreq(len(X_fft), t_continuous[1] - t_continuous[0])
        
        axes[i, 1].plot(freqs[:len(freqs)//2], np.abs(X_fft[:len(X_fft)//2]))
        axes[i, 1].axvline(f_signal, color='red', linestyle='--', label=f'Original {f_signal}Hz')
        axes[i, 1].set_xlabel('Frequency (Hz)')
        axes[i, 1].set_ylabel('Magnitude')
        axes[i, 1].set_title(f'Frequency Spectrum (fs={fs}Hz)')
        axes[i, 1].legend()
        axes[i, 1].grid(True, alpha=0.3)
        axes[i, 1].set_xlim(0, 100)
    
    plt.show()

# Run all analyses
print("=== Activity 1: Sampling and Reconstruction ===")
print("Running sampling analysis...")

print("\n=== Activities 4-7: Quantizer Characteristics ===")
plot_quantizer_characteristics()

print("\n=== Activities 8-9: Quantization Noise Analysis ===")
np_m, np_t, sqnr_m, sqnr_t = analyze_quantization_noise()
print(f"Noise Power - Measured: {np_m:.6f}, Theoretical: {np_t:.6f}")
print(f"16-bit SQNR - Measured: {sqnr_m:.2f} dB, Theoretical: {sqnr_t:.2f} dB")

print("\n=== Activity 4: Aliasing Demonstration ===")
demonstrate_aliasing()
