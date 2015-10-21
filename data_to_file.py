from reader import ins
from threading import Thread

time_to_run = 10 # Time to run in seconds
filename = 'accel_x_data.csv' # File to write to

f = open(filename, 'w')
def write_file():
    try:
        while(1):
            f.write(ins.readline())
    except:
        return
ins = ins()
ins.connect()
t = Thread(target=write_file)
t.start()
t.join(time_to_run)
f.close()
exit(0)
    