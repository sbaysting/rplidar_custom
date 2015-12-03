% Read actual data

theta = csvread('lidar_data_theta.csv');
theta_new = csvread('lidar_data_theta_new.csv');
dist = csvread('lidar_data_dist.csv');
dist_new = csvread('lidar_data_dist_new.csv');
heading = csvread('heading_data.csv');
heading_new = csvread('heading_data_new.csv');

% Shift theta points using yaw

delta_heading = heading_new - heading;
avg_delta_heading = sum(delta_heading)/length(delta_heading);

shifted_theta = theta_new + avg_delta_heading; 

x = dist.*sin(deg2rad(theta))/1000;
y = dist.*cos(deg2rad(theta))/1000;
x_new = dist_new.*sin(deg2rad(shifted_theta))/1000;
y_new = dist_new.*cos(deg2rad(shifted_theta))/1000;

% Sort points into groups   
% Calculate euclidian distance, find smallest one to current points
% group_mat = [];
% for i = 1:length(x)
%     error = 0.2;
%     bool = 0;
%     smallest_index = 0;
%     for j = 1:length(x)
%         if i ~= j
%             dist = sqrt((x(j)-x(i)).^2 + (y(j)-y(i)).^2);
%             if dist < error
%                 error = dist;
%                 bool = 1;
%                 smallest_index = j;
%             end
%         end
%     end
%     % Continue here
% end

% If the distances between points in an old group and new group
% are similar (within an error margin), shift the new points to
% the old points

% Plot

figure(1);
plot(x,y,'b.')
hold on
plot(x_new,y_new,'r.')
title('Point Map - Yaw and Linear Shifted')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
grid on
legend('Baseline Points','Yaw-Shifted New Points')

figure(2);
plot(x,y,'b.')
title('Point Map - Original')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
xlim([-1 1])
ylim([-1 1])
grid on

figure(3);
plot(x_new,y_new,'r.')
title('Point Map - Shifted')
xlabel('X Distance (m)')
ylabel('Y Distance (m)')
xlim([-1 1])
ylim([-1 1])
grid on

