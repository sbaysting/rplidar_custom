# -*- coding: utf-8 -*-
"""
Example demonstrating a variety of scatter plot features.
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import time
import threading

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')

## create four areas to add plots
w1 = view.addPlot()
print("Generating data, this takes a few seconds...")

## There are a few different ways we can draw scatter plots; each is optimized for different types of data:


## 1) All spots identical and transform-invariant (top-left plot). 
## In this case we can get a huge performance boost by pre-rendering the spot 
## image and just drawing that image repeatedly.

n = 500
s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
pos = np.random.normal(size=(2,n), scale=1e-5)
spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
s1.addPoints(spots)

w1.addItem(s1)

## Make all plots clickable
lastClicked = []
def clicked(plot, points):
    global lastClicked
    for p in lastClicked:
        p.resetPen()
    print("clicked points", points)
    for p in points:
        p.setPen('b', width=2)
    lastClicked = points
s1.sigClicked.connect(clicked)

timer = pg.QtCore.QTimer()
#pw = pg.plot()
def update_points():
    time.sleep(5)
    pos = np.random.normal(size=(2,n), scale=1e-5)
    spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
    
def update():
    s1.clear()
    pos = np.random.normal(size=(2,n), scale=1e-5)
    spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
    s1.addPoints(spots)
#s1.sigPlotChanged.connect(update)
    #pw.plot(x, y, clear=True)
timer.timeout.connect(update)
timer.start(2000)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    #t = threading.Thread(target=update_points)
    #t.start()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

        