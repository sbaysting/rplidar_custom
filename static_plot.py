import numpy as np
import matplotlib.pyplot as plt

def live_plot(x, y):
    plt.clf()
    plt.plot(x, y, 'ro')
    plt.show()
    
if __name__ == "__main__":
    counter = 0
    #while True:
    try:
        tmp = raw_input().strip().split()
        data = np.array(tmp, dtype=np.double)
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
        print "Data: "+str(len(data))
        print "Theta: "+str(len(theta))
        print "Dist: "+str(len(dist))
        x = []
        y = []
        for i in range(0,len(theta)):
            x.append(dist[i]*np.sin(np.radians(theta[i])))
            y.append(dist[i]*np.cos(np.radians(theta[i])))
        print "x: "+str(len(x))
        print "y: "+str(len(y))
        print "Plotting plot number %d"%counter
        live_plot(x, y)
        counter += 1
    except EOFError:
        print "Input has terminated! Exiting"
        exit()
    except ValueError:
        print "Invalid input, skipping.  Input was: %s"%tmp
        #continue