k = input('Number of Cycles = ');
a = input('Amplitude = ');
fm = input('Frequency = ');


%original signal
t = 0: 1/(fm*fm) : k/fm ;
y = a*cos(2*pi*fm*t);

figure;
subplot(2,2,1);
plot(t,y);
grid on;
xlabel('t'); ylabel('y');
title('The input signal');

%nyquist frequency
fn = 2*fm;

% undersampling
fu = 3/4*fn;
tu= 0: 1/fu: k/fm;
yu = a*cos(2*pi*fm*tu);

subplot(2,2,2);
stem(tu,yu);
hold on;
plot(tu,yu,'r');
xlabel('tu'); ylabel('y3u');
title('The under sampled  signal');


%nyquist sampling
tn= 0: 1/fn: k/fm;
yn = a*cos(2*pi*fm*tn);

subplot(2,2,3);
stem(tn,yn);
hold on;
plot(tn,yn,'g');
xlabel('tn'); ylabel('yn');
title('The signal sampled at nyquist frequency');

%over sampling
fo = 10*fn;
to= 0: 1/fo: k/fm;
yo = a*cos(2*pi*fm*to);

subplot(2,2,4);
stem(to,yo);
hold on;
plot(to,yo,'r');
xlabel('to'); ylabel('yo');
title('The over sampled  signal');



