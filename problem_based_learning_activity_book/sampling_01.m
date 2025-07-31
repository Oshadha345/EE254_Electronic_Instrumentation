pkg load audio

[x, Fs] = audioread('danith.wav');

%dimensions of audio file

print('Size of the audio array  : ',size(x));
print('Length of the audio array: ',length(x));


%creating new audio samples with different sampling rates

y = resample(x, 1, 10);
Fs_y = Fs/10;

z = resample(x, 1, 40);
Fs_z = Fs/40;

 %plotting the graphs of three samples

subplot(3,1,1);
hold on;
plot(x,'r-','o','MarkSize',5);

subplot(3,1,2);
hold on;
plot(y,'g-','o','MarkSize',5);

subplot(3,1,3);
hold on;
plot(x,'b-','o','MarkSize',5);
