clear all % clear all variables
close all % close all figure windows

% ---------------- PARAMETERS -------------------

% This creates a size_of_box by size_of_box pixel grid
size_of_box = 2000; % size of a side of the square box in mm

% set up range of displacements to look at
minm=-100; % set limits for m and n
maxm=100;
minn=-100;
maxn=100;
% set up window of image to correlate
minmwin=-800; % set limits for m and n
maxmwin=800;
minnwin=-800;
maxnwin=800;

% -------------- END PARAMETERS -----------------

% Read data
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

% Process data into x,y values
x = dist.*sin(deg2rad(theta))/1000;
y = dist.*cos(deg2rad(theta))/1000;
x_new = dist_new.*sin(deg2rad(shifted_theta))/1000;
y_new = dist_new.*cos(deg2rad(shifted_theta))/1000;

% Create matrix of OLD x,y values within a size_of_box square of origin
old_matrix = zeros(size_of_box); % Each index is a 1mm space
for i = 1:length(x)
    x_val = round(x(i),3); % Round to nearest mm
    y_val = round(y(i),3); % Round to nearest mm
    % If x,y value is within the size_of_box square meter
    if abs(x_val)*1000 < size_of_box/2 && abs(y_val)*1000 < size_of_box/2 && abs(x_val) > 0 && abs(y_val) > 0
        if x_val < 0 && y_val < 0 % If quadrant 4
            old_matrix((size_of_box/2)-abs(x_val)*1000,(size_of_box/2)-abs(y_val)*1000) = 1; % Assign 1 to that coordinate
        elseif x_val > 0 && y_val < 0 % If quadrant 3
            old_matrix((abs(x_val)*1000)+size_of_box/2,(size_of_box/2)-abs(y_val)*1000) = 1; % Assign 1 to that coordinate
        elseif x_val > 0 && y_val > 0 % If quadrant 2
            old_matrix((abs(x_val)*1000)+size_of_box/2,(abs(y_val)*1000)+size_of_box/2) = 1; % Assign 1 to that coordinate
        else % If quadrant 1
            old_matrix((size_of_box/2)-abs(x_val)*1000,(abs(y_val)*1000)+size_of_box/2) = 1; % Assign 1 to that coordinate
        end
    end
end
        
% Create matrix of NEW x,y values within a size_of_box square of origin
new_matrix = zeros(size_of_box); % Each index is a 1mm space
for i = 1:length(x)
    x_val = round(x_new(i),3); % Round to nearest mm
    y_val = round(y_new(i),3); % Round to nearest mm
    % If x,y value is within the size_of_box square meter
    if abs(x_val)*1000 < size_of_box/2 && abs(y_val)*1000 < size_of_box/2 && abs(x_val) > 0 && abs(y_val) > 0
        if x_val < 0 && y_val < 0 % If quadrant 4
            new_matrix((size_of_box/2)-abs(x_val)*1000,(size_of_box/2)-abs(y_val)*1000) = 1; % Assign 1 to that coordinate
        elseif x_val > 0 && y_val < 0 % If quadrant 3
            new_matrix((abs(x_val)*1000)+size_of_box/2,(size_of_box/2)-abs(y_val)*1000) = 1; % Assign 1 to that coordinate
        elseif x_val > 0 && y_val > 0 % If quadrant 2
            new_matrix((abs(x_val)*1000)+size_of_box/2,(abs(y_val)*1000)+size_of_box/2) = 1; % Assign 1 to that coordinate
        else % If quadrant 1
            new_matrix((size_of_box/2)-abs(x_val)*1000,(abs(y_val)*1000)+size_of_box/2) = 1; % Assign 1 to that coordinate
        end
    end
end

% Assign two matricies to be point correlated
x1d = double(old_matrix);
x2d = double(new_matrix);

% Test new matrix assignments
% [row,col] = find(new_matrix == 1);
% figure(6);
% plot((row/1000)-1,(col/1000)-1,'r.')
% xlim([-1 1])
% ylim([-1 1])
% title('New Matrix Assignments')
% grid on
% [row,col] = find(old_matrix == 1);
% figure(7);
% plot((row/1000)-1,(col/1000)-1,'b.')
% xlim([-1 1])
% ylim([-1 1])
% title('Old Matrix Assignments')
% grid on
        

% gui to select files
% [filename1, pathname1] = uigetfile('*.bmp','Choose file 1');
% [filename2, pathname2] = uigetfile('*.bmp','Choose file 2');
% 
% %load the images into variables
% [x1,map]=imread(fullfile(pathname1,filename1));
% [x2,map]=imread(fullfile(pathname2,filename2));
% 
% %convert uint8 variables to double precision variables so that
% %they can be used for calculations
% x1d=double(x1);
% x2d=double(x2);
%
% command to display the images
%figure(1)
%subplot(121),image(x1)
%colormap(gray(256))
%axis('equal')
%axis('off')
%hold on
%subplot(122),image(x2)
%colormap(gray(256))
%axis('equal')
%axis('off')

% -------------------------- FFT START ---------------------------

% % calculate the correlation by direct multiplication
% phidm=zeros(maxm-minm+1,maxn-minn+1); % create matrix of proper size
% [mmesh,nmesh]=meshgrid(minm:maxm,minn:maxn); % set up matrix of grid locations
% corrtime=cputime; % record start time
% for m=minm:maxm
% for n=minn:maxn
% phidm(m-minm+1,n-minn+1)=sum(sum(x1d(128+minmwin:128+maxmwin,128+minnwin:128+maxnwin)...
% .*x2d(128+minmwin+m:128+maxmwin+m,128+minnwin+n:128+maxnwin+n)));
% end
% end
% sprintf('Correlation CPU time: %10.5f sec',cputime-corrtime) % record stop time
% figure(2)
% mesh(mmesh',nmesh',phidm) % plot results
% axis([minm maxm minn maxn min(min(phidm)) max(max(phidm))])
% title('Correlation')
% xlabel('m offset')
% ylabel('n offset')
% % find correlation peak locations
% [mpeakint,npeakint]=find(max(max(phidm))==phidm);
% mpeaksub=(log(phidm(mpeakint+1,npeakint))-log(phidm(mpeakint-1,npeakint)))...
% /(-2*log(phidm(mpeakint-1,npeakint))+4*log(phidm(mpeakint-0,npeakint))...
% -2*log(phidm(mpeakint+1,npeakint)))+mpeakint+minm-1
% npeaksub=(log(phidm(mpeakint,npeakint+1))-log(phidm(mpeakint,npeakint-1)))...
% /(-2*log(phidm(mpeakint,npeakint-1))+4*log(phidm(mpeakint,npeakint-0))...
% -2*log(phidm(mpeakint,npeakint+1)))+npeakint+minn-1
% FFT Correlation tracking routine
corrtime=cputime; % record start time
g1=ones(128,128)*mean(mean((x1d(128+minmwin:128+maxmwin,128+minnwin:128+maxnwin))));
g1(32:95,32:95)=x1d(128+minmwin:128+maxmwin,128+minnwin:128+maxnwin);
g2=x2d(128-64:128+63,128-64:128+63);
phifft=real(fftshift(ifft2(fft2(g1).*conj(fft2(g2)))));
sprintf('FFT Correlation tracking CPU time: %10.5f sec',cputime-corrtime)
% record stop time
% find phifft peak locations
[mpeakint,npeakint]=find(max(max(phifft))==phifft);
mpeak=(log(phifft(mpeakint+1,npeakint))-log(phifft(mpeakint-1,npeakint)))...
/(-2*log(phifft(mpeakint-1,npeakint))+4*log(phifft(mpeakint-0,npeakint))...
-2*log(phifft(mpeakint+1,npeakint)))+mpeakint-64
npeak=(log(phifft(mpeakint,npeakint+1))-log(phifft(mpeakint,npeakint-1)))...
/(-2*log(phifft(mpeakint,npeakint-1))+4*log(phifft(mpeakint,npeakint-0))...
-2*log(phifft(mpeakint,npeakint+1)))+npeakint-64
% Calculate image peak location using various image shifts clf
% fig=figure(3);
 iminshift=-32;
 imaxshift=32;
% set(fig,'DoubleBuffer','on');
% set(gca,'xlim',[1 64],'ylim',[1 64],...
% 'NextPlot','replace','Visible','off')
for ishift=iminshift:imaxshift
jshift=2*ishift;
corrtime=cputime; % record start time
g1=x1d(128+minmwin:128+maxmwin,128+minnwin:128+maxnwin);
g2=x2d(128+minmwin+ishift:128+maxmwin+ishift,128+minnwin+jshift:128+maxnwin+jshift);
phifft=real(fftshift(ifft2(fft2(g1).*conj(fft2(g2)))));
% find phifft peak locations
[mpeakint,npeakint]=find(max(max(phifft))==phifft);
% check if peak location is in bounds enough to do subpixel fit
if mpeakint>1&&npeakint>1&&mpeakint<maxmwin-minmwin+1&&npeakint<maxnwin-minnwin+1
mpeak(ishift-iminshift+1)=(log(phifft(mpeakint+1,npeakint))-log(phifft(mpeakint-1,npeakint)))...
/(-2*log(phifft(mpeakint-1,npeakint))+4*log(phifft(mpeakint-0,npeakint))...
-2*log(phifft(mpeakint+1,npeakint)))+mpeakint+minmwin-1-ishift;
npeak(ishift-iminshift+1)=(log(phifft(mpeakint,npeakint+1))-log(phifft(mpeakint,npeakint-1)))...
/(-2*log(phifft(mpeakint,npeakint-1))+4*log(phifft(mpeakint,npeakint-0))...
-2*log(phifft(mpeakint,npeakint+1)))+npeakint+minnwin-1-jshift;
else
% if not, then just use the integer value
mpeak(ishift-iminshift+1)=mpeakint+minmwin-1-ishift;
npeak(ishift-iminshift+1)=npeakint+minnwin-1-jshift;
end
% mesh plot of the correlation function as the windows are shifted
% mesh(phifft);
% hidden on
% axis([1 64 1 64 3.5e7 4.0e7])
% caxis([3.5e7 4.0e7])
% colorbar
 end
% figure(4)
% subplot(121),plot(iminshift:imaxshift,mpeak+10.3,'r.',iminshift:imaxshift,npeak+5.2,'k*')
% xlabel('shift (pix)')
% ylabel('displacement error (pix)')
% subplot(122),plot(iminshift:imaxshift,mpeak+10.3,'r.',iminshift:imaxshift,npeak+5.2,'k*')
% axis([-40 40 -0.2 0.2])
% xlabel('shift (pix)')
% ylabel('displacement error (pix)')
