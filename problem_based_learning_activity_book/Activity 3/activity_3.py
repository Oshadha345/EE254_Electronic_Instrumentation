import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

def generate_experimental_data():
    """Generate MSE data for Activity 3 experiment"""
    
    # Signal parameters
    f0 = 25  # Base frequency (Hz)
    fm1 = 2 * f0    # fm = 2f0 = 50 Hz
    fm2 = 2.2 * f0  # fm = 2.2f0 = 55 Hz
    
    # Sampling parameters
    steps = np.arange(28, 36)  # Steps 28 to 35
    fs_values = steps.astype(float)  # Sampling frequencies
    
    # Time parameters for high-resolution reference
    t_duration = 2.0  # seconds
    fs_ref = 1000    # High sampling rate for reference
    t_ref = np.linspace(0, t_duration, int(fs_ref * t_duration), endpoint=False)
    
    # Generate reference signals
    x1_ref = np.sin(2 * np.pi * fm1 * t_ref)  # 50 Hz reference
    x2_ref = np.sin(2 * np.pi * fm2 * t_ref)  # 55 Hz reference
    
    # Arrays to store results
    mse_fm1 = []
    mse_fm2 = []
    
    print("Generating experimental data...")
    print("Step | fs (Hz)   | MSE fm=2f0    | MSE fm=2.2f0  ")
    print("-" * 55)
    
    # Calculate MSE for each sampling frequency
    for i, fs in enumerate(fs_values):
        # Create sampling time vector
        dt = 1.0 / fs
        t_sample = np.arange(0, t_duration, dt)
        
        # Sample the signals
        x1_sampled = np.sin(2 * np.pi * fm1 * t_sample)
        x2_sampled = np.sin(2 * np.pi * fm2 * t_sample)
        
        # Reconstruct signals using linear interpolation
        x1_reconstructed = np.interp(t_ref, t_sample, x1_sampled)
        x2_reconstructed = np.interp(t_ref, t_sample, x2_sampled)
        
        # Calculate MSE
        mse1 = np.mean((x1_ref - x1_reconstructed)**2)
        mse2 = np.mean((x2_ref - x2_reconstructed)**2)
        
        mse_fm1.append(mse1)
        mse_fm2.append(mse2)
        
        # Print data for table with adjusted widths to prevent overlap
        print(f"{steps[i]:4d} | {fs:10.1f} | {mse1:13.5f} | {mse2:13.5f}")
    
    return steps, fs_values, np.array(mse_fm1), np.array(mse_fm2)
    
    # Sampling parameters
    steps = np.arange(28, 36)  # Steps 28 to 35
    fs_values = steps.astype(float)  # Sampling frequencies
    
    # Time parameters for high-resolution reference
    t_duration = 2.0  # seconds
    fs_ref = 1000    # High sampling rate for reference
    t_ref = np.linspace(0, t_duration, int(fs_ref * t_duration), endpoint=False)
    
    # Generate reference signals
    x1_ref = np.sin(2 * np.pi * fm1 * t_ref)  # 50 Hz reference
    x2_ref = np.sin(2 * np.pi * fm2 * t_ref)  # 55 Hz reference
    
    # Arrays to store results
    mse_fm1 = []
    mse_fm2 = []
    
    print("Generating experimental data...")
    print("Step | fs (Hz) | MSE fm=2f0 | MSE fm=2.2f0")
    print("-" * 45)
    
    # Calculate MSE for each sampling frequency
    for i, fs in enumerate(fs_values):
        # Create sampling time vector
        dt = 1.0 / fs
        t_sample = np.arange(0, t_duration, dt)
        
        # Sample the signals
        x1_sampled = np.sin(2 * np.pi * fm1 * t_sample)
        x2_sampled = np.sin(2 * np.pi * fm2 * t_sample)
        
        # Reconstruct signals using linear interpolation
        x1_reconstructed = np.interp(t_ref, t_sample, x1_sampled)
        x2_reconstructed = np.interp(t_ref, t_sample, x2_sampled)
        
        # Calculate MSE
        mse1 = np.mean((x1_ref - x1_reconstructed)**2)
        mse2 = np.mean((x2_ref - x2_reconstructed)**2)
        
        mse_fm1.append(mse1)
        mse_fm2.append(mse2)
        
        # Print data for table
        print(f"{steps[i]:4d} | {fs:7.1f} | {mse1:10.5f} | {mse2:12.5f}")
    
    return steps, fs_values, np.array(mse_fm1), np.array(mse_fm2)

def create_activity3_plot(steps, fs_values, mse_fm1, mse_fm2):
    """Create the required plot for Activity 3"""
    
    # Set up the plot with professional formatting
    plt.figure(figsize=(12, 8))
    
    # Create the main plot
    plt.plot(fs_values, mse_fm1, 'bo-', linewidth=2.5, markersize=8, 
             label='fm = 2f₀ (50 Hz)', markerfacecolor='lightblue', markeredgecolor='blue')
    plt.plot(fs_values, mse_fm2, 'rs-', linewidth=2.5, markersize=8, 
             label='fm = 2.2f₀ (55 Hz)', markerfacecolor='lightcoral', markeredgecolor='red')
    
    # Add reference lines for Nyquist frequencies
    plt.axvline(50, color='blue', linestyle='--', alpha=0.6, 
                label='fm = 50 Hz (signal frequency)')
    plt.axvline(55, color='red', linestyle='--', alpha=0.6, 
                label='fm = 55 Hz (signal frequency)')
    
    # Formatting
    plt.xlabel('Sampling Frequency fs (Hz)', fontsize=14, fontweight='bold')
    plt.ylabel('Mean Square Error (MSE)', fontsize=14, fontweight='bold')
    plt.title('MSE vs Sampling Frequency\nActivity 3: Effect of Sampling Frequency on Reconstructed Signal', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Grid and styling
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    plt.legend(fontsize=12, loc='upper right')
    
    # Set axis limits with some padding
    plt.xlim(27.5, 35.5)
    plt.ylim(0, max(max(mse_fm1), max(mse_fm2)) * 1.1)
    
    # Add data point annotations for key points
    for i, (fs, mse1, mse2) in enumerate(zip(fs_values, mse_fm1, mse_fm2)):
        if i % 2 == 0:  # Annotate every other point to avoid crowding
            plt.annotate(f'{mse1:.3f}', (fs, mse1), 
                        textcoords="offset points", xytext=(0,10), 
                        ha='center', fontsize=9, color='blue', alpha=0.8)
            plt.annotate(f'{mse2:.3f}', (fs, mse2), 
                        textcoords="offset points", xytext=(0,-15), 
                        ha='center', fontsize=9, color='red', alpha=0.8)
    
    # Add text box with key information
    textstr = '\n'.join((
        f'Signal 1: fm = 2f₀ = 50 Hz',
        f'Signal 2: fm = 2.2f₀ = 55 Hz',
        f'All fs < Nyquist rates (100 & 110 Hz)',
        f'Aliasing present in all cases'
    ))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.show()

def create_data_table(steps, fs_values, mse_fm1, mse_fm2):
    """Create a formatted data table"""
    
    # Create DataFrame for easy formatting
    df = pd.DataFrame({
        'step': steps,
        'fs (Hz)': fs_values,
        'MSE fm = 2f₀': [f"{mse:.5f}" for mse in mse_fm1],
        'MSE fm = 2.2f₀': [f"{mse:.5f}" for mse in mse_fm2]
    })
    
    print("\n" + "="*60)
    print("TABLE 2: MSE VALUES FOR DIFFERENT SAMPLING FREQUENCIES")
    print("="*60)
    print(df.to_string(index=False, justify='center'))
    print("="*60)
    
    return df

def analyze_results(steps, fs_values, mse_fm1, mse_fm2):
    """Analyze and explain the experimental results"""
    
    print("\n" + "🔬 EXPERIMENTAL ANALYSIS")
    print("-" * 30)
    
    # Basic statistics
    print(f"Signal Parameters:")
    print(f"  • fm1 = 2f₀ = 50 Hz (Nyquist rate = 100 Hz)")
    print(f"  • fm2 = 2.2f₀ = 55 Hz (Nyquist rate = 110 Hz)")
    print(f"  • Sampling range: {fs_values[0]:.0f} - {fs_values[-1]:.0f} Hz")
    
    # MSE analysis
    mse1_reduction = ((mse_fm1[0] - mse_fm1[-1]) / mse_fm1[0]) * 100
    mse2_reduction = ((mse_fm2[0] - mse_fm2[-1]) / mse_fm2[0]) * 100
    
    print(f"\nMSE Trends:")
    print(f"  • 50 Hz signal: {mse_fm1[0]:.5f} → {mse_fm1[-1]:.5f} ({mse1_reduction:.1f}% reduction)")
    print(f"  • 55 Hz signal: {mse_fm2[0]:.5f} → {mse_fm2[-1]:.5f} ({mse2_reduction:.1f}% reduction)")
    
    # Aliasing analysis
    print(f"\nAliasing Effects:")
    print(f"  • All sampling frequencies are below Nyquist rates")
    print(f"  • 55 Hz signal shows consistently higher MSE due to more severe aliasing")
    print(f"  • MSE decreases as fs approaches (but remains below) signal frequency")
    
    # Critical observations
    print(f"\nKey Observations:")
    print(f"  • When fs < fm: Severe aliasing occurs")
    print(f"  • When fs ≈ fm: MSE is still significant due to undersampling")
    print(f"  • Higher frequency signals are more sensitive to undersampling")
    print(f"  • To eliminate aliasing: fs ≥ 2fm (Nyquist criterion)")
    
    # Practical implications
    print(f"\nPractical Implications:")
    print(f"  • Anti-aliasing filters required when fs < 2fm")
    print(f"  • Oversampling (fs >> 2fm) provides better reconstruction")
    print(f"  • Trade-off between sampling rate and reconstruction quality")

def demonstrate_aliasing_effect(fs_values, mse_fm1, mse_fm2):
    """Demonstrate the aliasing effect visually"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Time domain demonstration
    t_show = np.linspace(0, 0.2, 1000)  # Show 0.2 seconds
    fm1, fm2 = 50, 55
    
    # Original signals
    x1_orig = np.sin(2 * np.pi * fm1 * t_show)
    x2_orig = np.sin(2 * np.pi * fm2 * t_show)
    
    # Demonstrate with two different sampling rates
    fs_demo = [30, 34]  # From our experimental range
    
    for i, fs in enumerate(fs_demo):
        # Sample and reconstruct
        t_sample = np.arange(0, 0.2, 1/fs)
        x1_sample = np.sin(2 * np.pi * fm1 * t_sample)
        x2_sample = np.sin(2 * np.pi * fm2 * t_sample)
        
        x1_recon = np.interp(t_show, t_sample, x1_sample)
        x2_recon = np.interp(t_show, t_sample, x2_sample)
        
        # Plot 50 Hz signal
        axes[0, i].plot(t_show, x1_orig, 'b-', linewidth=2, label='Original 50 Hz')
        axes[0, i].plot(t_show, x1_recon, 'b--', linewidth=2, alpha=0.8, label='Reconstructed')
        axes[0, i].plot(t_sample, x1_sample, 'bo', markersize=6, label='Samples')
        axes[0, i].set_title(f'50 Hz Signal @ fs = {fs} Hz\nMSE = {mse_fm1[fs_values.tolist().index(fs)]:.4f}')
        axes[0, i].set_xlabel('Time (s)')
        axes[0, i].set_ylabel('Amplitude')
        axes[0, i].legend()
        axes[0, i].grid(True, alpha=0.3)
        
        # Plot 55 Hz signal  
        axes[1, i].plot(t_show, x2_orig, 'r-', linewidth=2, label='Original 55 Hz')
        axes[1, i].plot(t_show, x2_recon, 'r--', linewidth=2, alpha=0.8, label='Reconstructed')
        axes[1, i].plot(t_sample, x2_sample, 'rs', markersize=6, label='Samples')
        axes[1, i].set_title(f'55 Hz Signal @ fs = {fs} Hz\nMSE = {mse_fm2[fs_values.tolist().index(fs)]:.4f}')
        axes[1, i].set_xlabel('Time (s)')
        axes[1, i].set_ylabel('Amplitude')
        axes[1, i].legend()
        axes[1, i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Main execution
def run_activity3_experiment():
    """Run the complete Activity 3 experiment"""
    
    print("🧪 ACTIVITY 3: SAMPLING FREQUENCY ANALYSIS EXPERIMENT")
    print("="*60)
    
    # Generate experimental data
    steps, fs_values, mse_fm1, mse_fm2 = generate_experimental_data()
    
    # Create the required plot
    print("\n📊 Creating MSE vs Sampling Frequency plot...")
    create_activity3_plot(steps, fs_values, mse_fm1, mse_fm2)
    
    # Create formatted data table
    df = create_data_table(steps, fs_values, mse_fm1, mse_fm2)
    
    # Analyze results
    analyze_results(steps, fs_values, mse_fm1, mse_fm2)
    
    # Demonstrate aliasing effect
    print("\n📈 Creating aliasing demonstration plots...")
    demonstrate_aliasing_effect(fs_values, mse_fm1, mse_fm2)
    
    print("\n✅ Activity 3 experiment completed!")
    print("   📋 Table 2 data generated and displayed")
    print("   📊 MSE vs fs graph created") 
    print("   🔍 Aliasing effects demonstrated")
    
    return df

# Run the experiment
if __name__ == "__main__":
    results_df = run_activity3_experiment()