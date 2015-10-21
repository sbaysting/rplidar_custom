timespan = 10;
a = csvread('accel_x_data.csv');
%for i = 1:length(a)
%    if a(i) < 1
%        if a(i) > -1
%            a(i) = 0;
%        end
%    end
%end

% Moving average filter (interval = 30)
a = smooth(a,25,'moving');

time = [0+timespan/length(a):timespan/length(a):timespan];
pos_array = zeros(1,length(a));
vel_array = zeros(1,length(a));
previous_time = 0;
previous_pos = 0;
previous_vel = 0;
for i = 1:length(a)
    pos_func = @(t) a(i)*t^2 + previous_vel*t + previous_pos;
    vel_func = @(t) 2*a(i)*t + previous_vel;
    previous_vel = vel_func(time(i)-previous_time);
    previous_pos = pos_func(time(i)-previous_time);
    previous_time = time(i);
    pos_array(i) = previous_pos;
    vel_array(i) = previous_vel;
end

figure(1);
plot(time,a)
hold on
xlabel('Time (s)')
ylabel('Acceleration (m/s^2)')
title('Acceleration vs. Time')
grid on
legend('Raw Data','Filtered Data (Moving Average)')

figure(2);
plot(time,pos_array)
hold on
xlabel('Time (s)')
ylabel('Position (m)')
title('Position vs. Time')
grid on
legend('Raw Data','Filtered Data (Moving Average)')

figure(3);
plot(time,vel_array)
hold on
xlabel('Time (s)')
ylabel('Velocity (m/s)')
title('Velocity vs. Time')
grid on
legend('Raw Data','Filtered Data (Moving Average)')
    