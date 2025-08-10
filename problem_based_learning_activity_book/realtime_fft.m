clear all; close all; clc;

% Read audio
[y, Fs] = audioread('danith.wav');
y = y(:,1); % take first channel if stereo
L = length(y);

% Prepare plots
figure(1);

subplot(2,1,1);
time_plot = plot(NaN, NaN);
xlabel('Time (s)');
ylabel('Audio Signal');
ylim([-1 1]);
xlim([0 0.05]); % 50 ms window

subplot(2,1,2);
freq_plot = plot(NaN, NaN);
xlabel('Frequency (Hz)');
ylabel('|P1(f)|');
xlim([0 Fs/2]);
ylim([0 1]);

% Play audio once
sound(y, Fs);

% Parameters
win_size = 2048; % samples per FFT window
hop_size = 512;  % samples to advance per update
update_rate = hop_size / Fs; % seconds per update

% Start timer
start_time = tic;

fprintf('Press any key to stop...\n');

% Real-time loop
while true
    % Check if key pressed -> exit
    if kbhit()
        disp('Stopping...');
        break;
    end

    % Find current playback position
    elapsed = toc(start_time);
    current_sample = round(elapsed * Fs) + 1;

    if current_sample + win_size - 1 > L
        break; % reached end of audio
    end

    % Extract chunk
    chunk = y(current_sample : current_sample + win_size - 1);

    % Update time-domain plot
    t = (0:win_size-1) / Fs;
    set(time_plot, 'XData', t, 'YData', chunk);

    % Update frequency-domain plot
    Y_chunk = fft(chunk);
    P2 = abs(Y_chunk / win_size);
    P1 = P2(1:floor(win_size/2)+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs * (0:floor(win_size/2)) / win_size;

    set(freq_plot, 'XData', f, 'YData', P1);

    drawnow;
    pause(update_rate);
end

