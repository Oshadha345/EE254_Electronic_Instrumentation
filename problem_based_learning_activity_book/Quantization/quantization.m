clear all;
close all;
clc

[x,Fs] = audioread('danith.wav');

X=x(:,1);

N = 0;

L = 2^N;

Xmin = -1; Xmax=1;

q = (Xmax - Xmin)/L;

n = floor((X-Xmin)/q) - (L/2);

Xq = ((2*n+1)*q)/2;

qe = Xq - X;

plot(x,'b');
hold on;

stairs(Xq,'r');

