
% Read the whole audio file
[y, Fs] = audioread('danith.wav');
L = length(y);

% Parameters for chunk processing
chunk_size = 1024; % number of samples per update
num_chunks = ceil(L / chunk_size);

% Prepare plots
figure(1);
subplot(2,1,1);
time_plot = plot(NaN, NaN);
xlabel('Time (s)');
ylabel('Audio Signal');
xlim([0 chunk_size/Fs]);
ylim([-1 1]);


subplot(2,1,2);
freq_plot = plot(NaN, NaN);
xlabel('Frequency (Hz)');
ylabel('|P1(f)|');
xlim([0 Fs/2]);
ylim([0 1]);

% Play audio in chunks and update plots
for k = 1:num_chunks
    start_idx = (k-1)*chunk_size + 1;
    end_idx = min(k*chunk_size, L);
    chunk = y(start_idx:end_idx);

    % Update time plot
    t = (0:length(chunk)-1) / Fs;
    set(time_plot, 'XData', t, 'YData', chunk);

    % FFT for frequency domain
    NFFT = length(chunk);
    Y_chunk = fft(chunk);
    P2 = abs(Y_chunk/NFFT);
    P1 = P2(1:floor(NFFT/2)+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs*(0:floor(NFFT/2))/NFFT;

    % Update frequency plot
    set(freq_plot, 'XData', f, 'YData', P1);

    drawnow; % refresh the figure

    % Play the chunk
    sound(chunk, Fs);

    % Wait for chunk duration
    pause(length(chunk)/Fs);
end

