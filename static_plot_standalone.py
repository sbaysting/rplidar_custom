import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys

def live_plot(x, y):
    plt.clf()
    plt.plot(x, y, 'ro')
    plt.show()
    
if __name__ == "__main__":
    counter = 0
    #while True:
    try:
        rotations = 10
        if len(sys.argv) > 1:
            rotations = int(sys.argv[1])
        # New thread to open rplidar program and pipe input into python
        proc = subprocess.Popen('bin/Debug/./rplidar_custom '+str(rotations),shell=True,stdout=subprocess.PIPE)
        tmp = proc.communicate()[0]
        
        # Process data
        data = np.array(tmp.strip().split(), dtype=np.double)
        theta = []
        dist = []
        for i in range(0,len(data),2):
            theta.append(data[i])
        for i in range(1,len(data),2):
            dist.append(data[i])
        if len(dist) != len(theta):
            if len(dist)>len(theta):
                dist.pop()
            else:
                theta.pop()
        x = []
        y = []
        for i in range(0,len(theta)):
            x.append(dist[i]*np.sin(np.radians(theta[i])))
            y.append(dist[i]*np.cos(np.radians(theta[i])))
            
        # Plot data
        live_plot(x, y)
        counter += 1
    except EOFError:
        print "Input has terminated! Exiting"
        exit()
    except ValueError:
        print "Invalid input, skipping.  Input was: %s"%tmp
        #continue