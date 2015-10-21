from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from threading import Thread
import sys
import subprocess

class lidar_plot:
    
    plot_points = 0
    x = []
    y = []
    s1 = None
    thread = None
    
    # Parameters:
    # plot_points - the number of points to store
    # frame_rate - the plot GUI update rate in ms
    # title - the plot and window title
    def __init__(self, plot_points, frame_rate, title = 'RPLIDAR Data Plot'):
        self.thread = Thread(target=self.__start,args=[plot_points,frame_rate,title])
        self.thread.start()
        
    def __start(self, plot_points, frame_rate, title = 'RPLIDAR Data Plot'):
        self.x = [0]*plot_points # x value data generated from dist*sin(theta)
        self.y = [0]*plot_points # y value data generated from dist*cos(theta)
        self.plot_points = plot_points
        # Create GUI Graphics and Window; Set up parameters
        app = QtGui.QApplication([])
        mw = QtGui.QMainWindow()
        mw.resize(800,800)
        view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        mw.setCentralWidget(view)
        mw.show() # Show the created GUI
        mw.setWindowTitle(title)
        # Create plot and set plot parameters
        w1 = view.addPlot() # Returns a PlotItem object
        w1.showGrid(x=True,y=True)
        w1.setMenuEnabled()
        w1.getViewBox().setXRange(min=-0.8,max=0.8)
        w1.getViewBox().setYRange(min=-1.0,max=1.0)
        w1.setLabel(axis='left',text='Y Distance',units='m')
        w1.setLabel(axis='bottom',text='X Distance',units='m')
        w1.setTitle(title=title)
        # Create scatter plot
        s1 = pg.ScatterPlotItem(size=3, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120))
        s1.addPoints(self.x,self.y)
        # Add scatter plot to the window
        w1.addItem(s1)
        self.s1 = s1
        # Create plot GUI update timer
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.__update_plot)
        timer.start(frame_rate)
        # Load plot
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
        
    # Update the plot as the data comes in
    def __update_plot(self):
        self.s1.clear()
        self.s1.addPoints(self.x,self.y)
