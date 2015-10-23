theta = csvread('lidar_data_theta.csv');
theta_new = csvread('lidar_data_theta_new.csv');
dist = csvread('lidar_data_dist.csv');
dist_new = csvread('lidar_data_dist_new.csv');
heading = csvread('heading_data.csv');
heading_new = csvread('heading_data_new.csv');

delta_heading = heading_new - heading;
avg_delta_heading = sum(delta_heading)/length(delta_heading)

shifted_theta = theta_new + avg_delta_heading;

figure(1);
x = dist.*sin(deg2rad(theta))/1000;
y = dist.*cos(deg2rad(theta))/1000;
plot(x,y,'b.')
title('Point Map - Baseline')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
grid on

figure(2);
x = dist_new.*sin(deg2rad(theta_new))/1000;
y = dist_new.*cos(deg2rad(theta_new))/1000;
plot(x,y,'r.')
title('Point Map - With LIDAR Rotated (New Points)')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
grid on

figure(3);
x = dist.*sin(deg2rad(theta))/1000;
y = dist.*cos(deg2rad(theta))/1000;
x1 = dist_new.*sin(deg2rad(shifted_theta))/1000;
y1 = dist_new.*cos(deg2rad(shifted_theta))/1000;
plot(x,y,'b.')
hold on
plot(x1,y1,'r.')
title('Point Map - Yaw Shifted')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
grid on
legend('Baseline Points','Yaw-Shifted New Points')

