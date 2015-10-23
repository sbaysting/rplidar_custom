from reader import rplidar
from reader import ins
import time
import collections

# Global variables
lidar_cbuffer = collections.deque(maxlen=720)
lidar_cbuffer = collections.deque(maxlen=720)
heading_cbuffer = collections.deque(maxlen=720)

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

# Hampel Filter (Removal of Outliers)
def HampelFilter(wk,K,FilterParms):
    None # Could be difficult
    
# Moving Average Filter (Smoothing out Data)
def moving_average_filter():
    None # Shouldn't be too bad
    
# Point correlation to determine if it's similar
def point_correlate():
    None
    
# Direction Vector Calculate
def dir_vector(xold,yold,xnew,ynew):
    return [(xnew-xold),(ynew-yold)]

# Gather 
    
# Main

rplidar = rplidar(device='/dev/ttyUSB0')
ins = ins(device='/dev/ttyACM0')

connect(rplidar,ins)


    