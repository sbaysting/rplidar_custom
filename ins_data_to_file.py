from reader import ins
from threading import Thread

time_to_run = 10 # Time to run in seconds
filename = 'data/heading_data.csv' # File to write to

stop = False
f = open(filename, 'w')
def write_file():
    try:
        while(1 and not stop):
            f.write(ins.readline())
    except:
        return
ins = ins()
ins.connect()
t = Thread(target=write_file)
t.start()
t.join(time_to_run)
stop = True
f.close()
exit(0)
    