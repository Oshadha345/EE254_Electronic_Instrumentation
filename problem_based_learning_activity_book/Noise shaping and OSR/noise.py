import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt, resample

# Activity 12: Effect of Oversampling on Noise Floor
def demonstrate_oversampling_effect():
    """Demonstrate the effect of oversampling on quantization noise floor"""
    
    # Generate a test signal (sum of sinusoids)
    fs_base = 1000  # Base sampling frequency
    t_duration = 1.0
    t = np.linspace(0, t_duration, int(fs_base * t_duration), endpoint=False)
    
    # Create a band-limited signal (bandwidth = 100 Hz)
    x = (np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*80*t) + 
         0.3*np.sin(2*np.pi*120*t))
    x = x / np.max(np.abs(x))  # Normalize
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1-bit quantizer
    def one_bit_quantize(signal):
        return np.where(signal >= 0, 0.5, -0.5)
    
    # Test different OSR values
    osr_values = [1, 2, 4, 8]
    colors = ['blue', 'green', 'red', 'orange']
    
    # Theoretical noise floor calculation
    for i, (osr, color) in enumerate(zip(osr_values, colors)):
        # Oversample the signal
        fs_over = fs_base * osr
        if osr > 1:
            x_over = resample(x, len(x) * osr)
        else:
            x_over = x.copy()
        
        # 1-bit quantization
        x_quantized = one_bit_quantize(x_over)
        
        # Calculate power spectral density
        f, Pxx = signal.welch(x_quantized, fs_over, nperseg=1024)
        
        # Plot PSD
        axes[0, 0].semilogy(f, Pxx, color=color, label=f'OSR = {osr}')
        
        # Calculate noise floor level in signal bandwidth (0-200 Hz)
        signal_bw = 200  # Hz
        noise_in_band = np.mean(Pxx[f <= signal_bw])
        
        # Theoretical noise floor reduction: 3 dB per doubling of OSR
        theoretical_reduction = 10 * np.log10(osr)
        print(f"OSR {osr}: Noise floor reduction ≈ {theoretical_reduction:.1f} dB")
    
    axes[0, 0].set_xlabel('Frequency (Hz)')
    axes[0, 0].set_ylabel('Power Spectral Density')
    axes[0, 0].set_title('Effect of Oversampling on Noise Floor')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_xlim(0, fs_base/2)
    
    # Show time domain comparison
    t_show = np.linspace(0, 0.05, int(0.05 * fs_base))
    x_show = (np.sin(2*np.pi*50*t_show) + 0.5*np.sin(2*np.pi*80*t_show))
    x_show = x_show / np.max(np.abs(x_show))
    
    axes[0, 1].plot(t_show, x_show, 'k-', linewidth=2, label='Original')
    
    for osr, color in zip([1, 4], ['blue', 'red']):
        if osr > 1:
            t_over = np.linspace(0, 0.05, int(0.05 * fs_base * osr))
            x_over_show = (np.sin(2*np.pi*50*t_over) + 0.5*np.sin(2*np.pi*80*t_over))
            x_over_show = x_over_show / np.max(np.abs(x_over_show))
        else:
            t_over = t_show
            x_over_show = x_show
        
        x_q_show = one_bit_quantize(x_over_show)
        
        if osr > 1:
            # Downsample for visualization
            x_q_show_down = x_q_show[::osr]
            t_down = t_show
        else:
            x_q_show_down = x_q_show
            t_down = t_over
        
        axes[0, 1].plot(t_down, x_q_show_down, color=color, linewidth=2, 
                       alpha=0.7, label=f'1-bit Quantized (OSR={osr})')
    
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].set_title('Time Domain: Effect of Oversampling')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    return fig, axes

# Activity 14-15: Sigma-Delta Quantization
def sigma_delta_quantizer(x, order=1):
    """First-order sigma-delta quantizer"""
    y = np.zeros(len(x))
    integrator = 0
    
    for i in range(len(x)):
        # Integrate the error
        integrator += (x[i] - (y[i-1] if i > 0 else 0))
        
        # Quantize
        y[i] = 0.5 if integrator > 0 else -0.5
    
    return y

def demonstrate_noise_shaping():
    """Demonstrate noise shaping with sigma-delta quantization"""
    
    # Generate test signal
    fs = 8000
    t = np.linspace(0, 0.5, int(fs * 0.5), endpoint=False)
    
    # Create a low-frequency signal (speech-like)
    x = (0.8 * np.sin(2*np.pi*200*t) + 0.4 * np.sin(2*np.pi*500*t) + 
         0.2 * np.sin(2*np.pi*800*t))
    x = x / np.max(np.abs(x))
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Regular 1-bit quantization
    x_regular = np.where(x >= 0, 0.5, -0.5)
    
    # Sigma-delta quantization
    x_sigma_delta = sigma_delta_quantizer(x)
    
    # Time domain comparison
    t_show = t[:1000]  # Show first portion
    axes[0, 0].plot(t_show, x[:1000], 'k-', linewidth=2, label='Original')
    axes[0, 0].plot(t_show, x_regular[:1000], 'b-', alpha=0.7, label='Regular 1-bit')
    axes[0, 0].plot(t_show, x_sigma_delta[:1000], 'r-', alpha=0.7, label='Sigma-Delta')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].set_title('Time Domain Comparison')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Frequency domain analysis
    f_reg, Pxx_reg = signal.welch(x_regular, fs, nperseg=1024)
    f_sd, Pxx_sd = signal.welch(x_sigma_delta, fs, nperseg=1024)
    
    axes[0, 1].semilogy(f_reg, Pxx_reg, 'b-', label='Regular 1-bit')
    axes[0, 1].semilogy(f_sd, Pxx_sd, 'r-', label='Sigma-Delta')
    axes[0, 1].set_xlabel('Frequency (Hz)')
    axes[0, 1].set_ylabel('Power Spectral Density')
    axes[0, 1].set_title('Noise Shaping Effect')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_xlim(0, fs/2)
    
    # Design low-pass filter for reconstruction
    nyquist = fs / 2
    cutoff = 1000  # 1 kHz cutoff
    order = 8
    b, a = butter(order, cutoff/nyquist, btype='low')
    
    # Filter both quantized signals
    x_reg_filtered = filtfilt(b, a, x_regular)
    x_sd_filtered = filtfilt(b, a, x_sigma_delta)
    
    # Show filtered results
    axes[0, 2].plot(t_show, x[:1000], 'k-', linewidth=3, label='Original')
    axes[0, 2].plot(t_show, x_reg_filtered[:1000], 'b--', linewidth=2, label='Filtered Regular')
    axes[0, 2].plot(t_show, x_sd_filtered[:1000], 'r-', linewidth=2, label='Filtered Sigma-Delta')
    axes[0, 2].set_xlabel('Time (s)')
    axes[0, 2].set_ylabel('Amplitude')
    axes[0, 2].set_title('After Low-Pass Filtering')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)
    
    # Calculate MSE for quality comparison
    mse_regular = np.mean((x - x_reg_filtered)**2)
    mse_sigma_delta = np.mean((x - x_sd_filtered)**2)
    
    # SNR comparison
    snr_regular = 10 * np.log10(np.var(x) / mse_regular)
    snr_sigma_delta = 10 * np.log10(np.var(x) / mse_sigma_delta)
    
    # Bar plot for comparison
    methods = ['Regular 1-bit', 'Sigma-Delta']
    mse_values = [mse_regular, mse_sigma_delta]
    snr_values = [snr_regular, snr_sigma_delta]
    
    axes[1, 0].bar(methods, mse_values, color=['blue', 'red'], alpha=0.7)
    axes[1, 0].set_ylabel('Mean Square Error')
    axes[1, 0].set_title('Reconstruction Quality (MSE)')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].bar(methods, snr_values, color=['blue', 'red'], alpha=0.7)
    axes[1, 1].set_ylabel('SNR (dB)')
    axes[1, 1].set_title('Signal-to-Noise Ratio')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Noise spectrum comparison
    noise_reg = x_regular - x
    noise_sd = x_sigma_delta - x
    
    f_noise_reg, Pxx_noise_reg = signal.welch(noise_reg, fs, nperseg=1024)
    f_noise_sd, Pxx_noise_sd = signal.welch(noise_sd, fs, nperseg=1024)
    
    axes[1, 2].semilogy(f_noise_reg, Pxx_noise_reg, 'b-', label='Regular Quantization Noise')
    axes[1, 2].semilogy(f_noise_sd, Pxx_noise_sd, 'r-', label='Sigma-Delta Noise (Shaped)')
    axes[1, 2].axvline(cutoff, color='green', linestyle='--', label=f'Filter Cutoff ({cutoff} Hz)')
    axes[1, 2].set_xlabel('Frequency (Hz)')
    axes[1, 2].set_ylabel('Noise Power Spectral Density')
    axes[1, 2].set_title('Quantization Noise Spectrum')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].set_xlim(0, fs/2)
    
    plt.tight_layout()
    plt.show()
    
    print(f"Reconstruction Quality Comparison:")
    print(f"Regular 1-bit: MSE = {mse_regular:.6f}, SNR = {snr_regular:.2f} dB")
    print(f"Sigma-Delta: MSE = {mse_sigma_delta:.6f}, SNR = {snr_sigma_delta:.2f} dB")
    print(f"Improvement: {snr_sigma_delta - snr_regular:.2f} dB")
    
    return fig, axes

# Activity 17: Advantages and Applications Discussion
def print_advantages_applications():
    """Print discussion points for 1-bit quantization advantages and applications"""
    
    print("\n" + "="*60)
    print("ACTIVITY 17: ADVANTAGES AND APPLICATIONS OF 1-BIT QUANTIZATION")
    print("="*60)
    
    print("\n🔧 ADVANTAGES OF 1-BIT QUANTIZATION:")
    print("-" * 40)
    advantages = [
        "Minimal Storage Requirements: Only 1 bit per sample",
        "Simple Hardware Implementation: Basic comparators and digital logic",
        "High-Speed Operation: Fast conversion rates possible", 
        "Reduced Quantization Noise: Through noise shaping techniques",
        "Cost-Effective: Lower component count and complexity",
        "Digital Processing Friendly: Easy manipulation in DSP systems",
        "Improved Dynamic Range: With oversampling and noise shaping"
    ]
    
    for i, advantage in enumerate(advantages, 1):
        print(f"{i}. {advantage}")
    
    print("\n🎵 AUDIO INDUSTRY APPLICATIONS:")
    print("-" * 35)
    audio_apps = [
        "Super Audio CD (SACD): Uses 1-bit sigma-delta at 2.8224 MHz",
        "Digital Audio Workstations: For high-quality audio processing",
        "Professional Audio Equipment: Mixing consoles and effects processors",
        "Automotive Audio: Space and cost-efficient audio systems",
        "Mobile Devices: Power-efficient audio codecs"
    ]
    
    for app in audio_apps:
        print(f"• {app}")
    
    print("\n🏭 SCADA SYSTEM APPLICATIONS:")
    print("-" * 32)
    scada_apps = [
        "Temperature Monitoring: Simple on/off threshold detection",
        "Pressure Switches: Binary state indication (safe/alarm)",
        "Motor Status: Running/stopped state monitoring",
        "Valve Positions: Open/closed state feedback",
        "Alarm Systems: Binary fault indication",
        "Digital I/O Modules: Cost-effective field device interfaces"
    ]
    
    for app in scada_apps:
        print(f"• {app}")
    
    print("\n📊 TYPICAL SPECIFICATIONS:")
    print("-" * 25)
    
    specs = {
        "Audio Industry": {
            "Sampling Rates": "44.1 kHz, 48 kHz, 96 kHz, 192 kHz, 2.8224 MHz (DSD)",
            "Quantization": "16-bit, 24-bit PCM; 1-bit sigma-delta (DSD)",
            "SNR Range": "90-120 dB",
            "Applications": "CD, DVD, Blu-ray, streaming, professional recording"
        },
        "SCADA Systems": {
            "Sampling Rates": "1 Hz - 1 kHz (depending on process dynamics)",
            "Quantization": "1-bit (digital I/O), 8-16 bit (analog measurements)",
            "Update Rates": "100 ms - 10 seconds",
            "Applications": "Power generation, water treatment, manufacturing"
        }
    }
    
    for category, details in specs.items():
        print(f"\n{category}:")
        for param, value in details.items():
            print(f"  {param}: {value}")

# Main execution function
def run_all_activities():
    """Execute all sigma-delta related activities"""
    
    print("="*60)
    print("DIGITAL INSTRUMENTATION: 1-BIT QUANTIZATION ANALYSIS")
    print("="*60)
    
    print("\n🔬 ACTIVITY 12-13: OVERSAMPLING EFFECTS")
    fig1, axes1 = demonstrate_oversampling_effect()
    
    print("\n🔬 ACTIVITY 14-16: SIGMA-DELTA QUANTIZATION")
    fig2, axes2 = demonstrate_noise_shaping()
    
    print_advantages_applications()
    
    # Summary of key theoretical results
    print("\n" + "="*60)
    print("KEY THEORETICAL RESULTS SUMMARY")
    print("="*60)
    
    theory_points = [
        "Nyquist Sampling Theorem: fs ≥ 2fm for perfect reconstruction",
        "Quantization Noise Power: σ² = q²/12 for uniform quantization",
        "SQNR for N-bit quantization: SQNR = 6.02N + 1.76 dB",
        "Oversampling benefit: 3 dB SNR improvement per 2x OSR increase",
        "Noise shaping: Pushes quantization noise to higher frequencies",
        "Sigma-delta advantage: Better SNR in signal bandwidth"
    ]
    
    for i, point in enumerate(theory_points, 1):
        print(f"{i}. {point}")

# Execute the analysis
if __name__ == "__main__":
    run_all_activities()