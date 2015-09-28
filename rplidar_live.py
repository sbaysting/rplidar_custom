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

frame_rate = 15 # Frame update rate in milliseconds
plot_points = 720 # Number of data points to show on the graph at any given time

############################################################################

# Start program
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from threading import Thread
import sys
import subprocess

# Global variables
x = [0]*plot_points # x value data generated from dist*sin(theta)
y = [0]*plot_points # y value data generated from dist*cos(theta)

# Create GUI Graphics and Window; Set up parameters
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show() # Show the created GUI
mw.setWindowTitle('RPLIDAR Live Data Plot')
w1 = view.addPlot()
# Create scatter plot
s1 = pg.ScatterPlotItem(size=3, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120))
s1.addPoints(x,y)
w1.addItem(s1)
# Create subprocess that starts the RPLIDAR C++ executable
p = subprocess.Popen('bin/Debug/./rplidar_custom ',shell=True,stdout=subprocess.PIPE)

# Read from RPLIDAR C++ executable stdout, write into variables and process them
def read_data():
    count = 0 # Count value to reuse x and y array storage spots
    while p.stdout.closed is False:
        # tmp[0] will be the theta value; tmp[1] will be the distance value
        tmp = np.array(p.stdout.readline().strip().split(), dtype=np.double)
        if len(tmp) == 2:
            x[count] = tmp[1]*np.sin(np.radians(tmp[0]))
            y[count] = tmp[1]*np.cos(np.radians(tmp[0]))
            count = count + 1
        if count >= plot_points: # This creates a circular array storage system for x and y values
            count = 0
    
# Update the plot as the data comes in
def update_plot():
    s1.clear()
    s1.addPoints(x,y)
    
# Create plot GUI update timer
timer = pg.QtCore.QTimer()
timer.timeout.connect(update_plot)
timer.start(frame_rate)

# Main function
if __name__ == "__main__":
    print("Starting data read and process stream...")
    data_read_thread = Thread(target=read_data)
    data_read_thread.start()
    print("Read stream active!")
    print("Data streams are now live! Loading plot...")
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        
        