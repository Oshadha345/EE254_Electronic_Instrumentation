% Activity 10: SQNR Analysis - Octave Compatible Code
% Signal to Quantization Noise Ratio verification

% Signal parameters
x_max = 1;
x_min = -1; % range of the signal

% Generate input signal in the range x_min to x_max
% Using uniform random distribution
x = (x_max - x_min) * rand(10000, 1) + x_min;

% Initialize arrays to store results
QE_c = []; % array to store Calculated SQNR
QE_m = []; % array to store Measured SQNR

% Display header
fprintf('SQNR Analysis for Different Bit Depths\n');
fprintf('=====================================\n');
fprintf('N (bits) | Measured SQNR | Calculated SQNR | Difference\n');
fprintf('---------+---------------+-----------------+-----------\n');

% Loop through different bit depths
for N = 1:16
    % Calculate quantization step size
    q = (x_max - x_min) / (2^N);

    % Mid-riser quantization
    xq = q * (floor(x/q) + 0.5);

    % Calculate quantization error
    qe = x - xq;

    % Calculate measured SQNR
    sqnr_measured = 20 * log10(std(x) / std(qe));
    QE_m = [QE_m sqnr_measured];

    % Calculate theoretical SQNR (for sinusoidal signals)
    sqnr_calculated = 6.02 * N + 1.76;
    QE_c = [QE_c sqnr_calculated];

    % Display results for each N
    fprintf('%8d | %13.2f | %15.2f | %9.2f\n', N, sqnr_measured, sqnr_calculated, abs(sqnr_measured - sqnr_calculated));
end

% Create the plot
figure;
plot(1:16, QE_m, 'k', 'LineWidth', 2);
hold on;
plot(1:16, QE_c, 'b', 'LineWidth', 2);

% Add plot formatting
grid on;
xlabel('Number of Bits (N)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('SQNR (dB)', 'FontSize', 12, 'FontWeight', 'bold');
title('Calculated and Measured SQNR vs Number of Bits', 'FontSize', 14, 'FontWeight', 'bold');

% Add legend
legend('Measured SQNR', 'Theoretical SQNR (6.02N + 1.76)', 'Location', 'northwest');

% Set axis limits for better visualization
xlim([1 16]);
ylim([0 max(max(QE_m), max(QE_c)) + 5]);

% Add grid styling
set(gca, 'GridAlpha', 0.3);
set(gca, 'FontSize', 11);

% Display summary statistics
fprintf('\n=== SUMMARY STATISTICS ===\n');
fprintf('Signal type: Uniform random distribution\n');
fprintf('Signal range: [%.1f, %.1f]\n', x_min, x_max);
fprintf('Number of samples: %d\n', length(x));
fprintf('Signal standard deviation: %.4f\n', std(x));
fprintf('Signal variance: %.4f\n', var(x));

% Calculate differences between measured and theoretical
differences = abs(QE_m - QE_c);
fprintf('\nSQNR Comparison:\n');
fprintf('Average difference: %.2f dB\n', mean(differences));
fprintf('Maximum difference: %.2f dB (at N=%d bits)\n', max(differences), find(differences == max(differences)));
fprintf('Minimum difference: %.2f dB (at N=%d bits)\n', min(differences), find(differences == min(differences)));

% Additional analysis plot
figure;
subplot(2, 2, 1);
plot(1:16, differences, 'r-o', 'LineWidth', 2, 'MarkerSize', 6);
grid on;
xlabel('Number of Bits (N)');
ylabel('|Measured - Theoretical| SQNR (dB)');
title('Difference Between Measured and Theoretical SQNR');

% Show quantization levels for different N values
subplot(2, 2, 2);
N_demo = [2, 4, 8];
colors = {'r', 'g', 'b'};
x_demo = linspace(-1, 1, 1000);

for i = 1:length(N_demo)
    N = N_demo(i);
    q = (x_max - x_min) / (2^N);
    xq_demo = q * (floor(x_demo/q) + 0.5);
    plot(x_demo, xq_demo, colors{i}, 'LineWidth', 2);
    hold on;
end
plot(x_demo, x_demo, 'k--', 'LineWidth', 1);
grid on;
xlabel('Input Signal');
ylabel('Quantized Output');
title('Quantization Characteristics');
legend('N=2', 'N=4', 'N=8', 'Ideal', 'Location', 'northwest');

% Histogram of quantization error for N=8
subplot(2, 2, 3);
N = 8;
q = (x_max - x_min) / (2^N);
xq = q * (floor(x/q) + 0.5);
qe = x - xq;
hist(qe, 50);
grid on;
xlabel('Quantization Error');
ylabel('Frequency');
title(sprintf('Quantization Error Distribution (N=%d)', N));

% SNR improvement with bit depth
subplot(2, 2, 4);
snr_improvement = QE_m - QE_m(1); % Relative to 1-bit
theoretical_improvement = QE_c - QE_c(1);
plot(1:16, snr_improvement, 'k-o', 'LineWidth', 2);
hold on;
plot(1:16, theoretical_improvement, 'b--s', 'LineWidth', 2);
grid on;
xlabel('Number of Bits (N)');
ylabel('SQNR Improvement (dB)');
title('SQNR Improvement vs 1-bit Quantization');
legend('Measured', 'Theoretical', 'Location', 'northwest');

% Print important theoretical notes
fprintf('\n=== THEORETICAL NOTES ===\n');
fprintf('1. SQNR formula (6.02N + 1.76) applies to sinusoidal signals\n');
fprintf('2. For uniform random signals, actual SQNR may differ slightly\n');
fprintf('3. Each additional bit provides ~6 dB improvement in SQNR\n');
fprintf('4. The constant 1.76 dB accounts for peak-to-RMS ratio of sine waves\n');
fprintf('5. Quantization noise is approximately uniformly distributed\n');

% Save the workspace for further analysis
save('sqnr_analysis_results.mat', 'QE_m', 'QE_c', 'x', 'N');

fprintf('\n✅ Analysis complete! Results saved to sqnr_analysis_results.mat\n');
