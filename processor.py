from reader import rplidar
from reader import ins
import time

# Global variables
x_old = 0 # Old x position for the LIDAR
y_old = 0 # Old y position for the LIDAR
x_new = 0 # New x position for the LIDAR
y_new = 0 # New y position for the LIDAR

# Connect RPLIDAR and INS Devices
def connect(rplidar, ins):
    print "Connecting to RPLIDAR at "+rplidar.device+"..."
    if rplidar.connect() == False:
        print "RPLIDAR failed to connect!"
        exit(1)
    print "Connected to RPLIDAR!"
    print "Connecting to INS at "+ins.device+"..."
    if ins.connect() == False:
        print "INS failed to connect!"
        exit(1)
    print "Connected to INS!"

# Kalman Filter
def kalman_filter():
    None
    
# Moving Average Filter
def moving_average_filter():
    None
    
# Direction Vector Calculate
def dir_vector(xold,yold,xnew,ynew):
    return [(xnew-xold),(ynew-yold)]
    
# Main

rplidar = rplidar(device='/dev/ttyUSB1')
ins = ins(device='/dev/ttyACM0')

connect(rplidar,ins)

ins.dump()
time.sleep(1)
rplidar.dump()
    