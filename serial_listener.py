import os
import serial
import sys
import threading
import time

def out(msg):
    print(msg)
    sys.stdout.flush()

# child process
def serial_read():
    time.sleep(1)

    out("Connecting to serial {}".format(serial_name))
    conn = serial.Serial(serial_name, timeout=0,baudrate=115200)
    conn.nonblocking()
    out("Connected! Reading data...")

    while conn.readable():
        output = conn.readline() # Try and read line
        while '\n' not in output: # If line not read correctly/buffered
            output = output + conn.read(0x4) # Read byte by byte until full line is present
        out("{}".format(output).strip())
        #time.sleep(1)

# Main thread

fd = os.open("/dev/ttyACM0",os.O_RDONLY)
serial_name = os.ttyname(fd)

child_thread = threading.Thread(target=serial_read)
child_thread.start()

child_thread.join()