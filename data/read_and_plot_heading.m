timespan = 10;
a = csvread('heading_data.csv');

% Moving average filter (interval = 30)
b = hampel(a,1);
b = smooth(b,20);
c = smooth(a,20);
d = smooth(a,30);
e = smooth(a,40);
f = smooth(a,50);

time = [0+timespan/length(a):timespan/length(a):timespan];

figure(1);
plot(time,b)
xlabel('Time (s)')
ylabel('Heading (degrees)')
title('Heading vs. Time')
grid on
legend('Hampel + Moving Average Data')

    