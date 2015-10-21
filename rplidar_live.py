############################################################################
#
# RPLIDAR Live Plot Program
#
# Written by Samuel Baysting, Rutgers University
#
# Language: Python (Plotting) and C++ (RPLIDAR Executable)
# Required Libraries: PyQtGraph, PyOpenGL, PyQt, NumPy
#
############################################################################

############################    PARAMETERS    ##############################

frame_rate = 10 # Frame update rate in milliseconds
plot_points = 720 # Number of data points to show on the graph at any given time

############################################################################

# Start program
import numpy as np
from threading import Thread
from reader import rplidar
from lidar_plot import lidar_plot

# Read from RPLIDAR C++ executable stdout, write into variables and process them
def read_data(subproc,plot):
    count = 0 # Count value to reuse x and y array storage spots
    while subproc.stdout.closed is False:
        # tmp[0] will be the theta value; tmp[1] will be the distance value
        tmp = np.array(subproc.stdout.readline().strip().split(), dtype=np.double)
        if len(tmp) == 2:
            plot.x[count] = (tmp[1]*np.sin(np.radians(tmp[0])))/1000
            plot.y[count] = (tmp[1]*np.cos(np.radians(tmp[0])))/1000
            count = count + 1
        if count >= plot.plot_points: # This creates a circular array storage system for x and y values
            count = 0

# Main function
if __name__ == "__main__":
    print("Creating plot...")
    plot = lidar_plot(plot_points, frame_rate)
    print("Plot created!")
    print("Booting RPLIDAR process...")
    rplidar = rplidar(device = '/dev/ttyUSB1')
    if rplidar.connect():
        data_read_thread = Thread(target=read_data,args=[rplidar.getProcess(),plot])
        data_read_thread.start()
        print("RPLIDAR process now live!")
    else:
        print("RPLIDAR process could not be opened!")
        exit(1)
        
        