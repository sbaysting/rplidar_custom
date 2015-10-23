from reader import rplidar
from reader import ins
from threading import Thread
import time
import sys

points = 720 # Points to collect
filename_theta = 'data/lidar_data_theta_new.csv' # File to write to
filename_dist = 'data/lidar_data_dist_new.csv' # File to write to
filename_heading = 'data/heading_data_new.csv'

buffer_theta = [0]*points
buffer_dist = [0]*points
buffer_heading = [0]*points
ft = open(filename_theta,'w')
fd = open(filename_dist,'w')
fh = open(filename_heading,'w')
def write_file():
    def read_lidar():
        start_time = time.time()
        count = 0
        while(count < points):
            buffertd = lidar.readline().split(" ")
            buffer_theta[count] = buffertd[0]
            buffer_dist[count] = buffertd[1]
            count = count + 1
        print "LIDAR collection time: "+str(time.time() - start_time)
        return
    def read_ins():
        start_time = time.time()
        count = 0
        while(count < points):
            buffer_heading[count] = ins.readline()
            count = count + 1
        print "INS collection time: "+str(time.time() - start_time)
        return
    try:
        t1 = Thread(target=read_lidar)
        t2 = Thread(target=read_ins)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        for number in buffer_theta:
            ft.write(str(number)+",")
        for number in buffer_dist:
            fd.write(str(number)+",")
        for number in buffer_heading:
            fh.write(str(number)+",")
        return
    except:
        return
lidar = rplidar(device="/dev/ttyUSB8")
lidar.connect()
ins = ins()
ins.connect()
write_file()
ft.close()
fd.close()
fh.close()
exit(0)