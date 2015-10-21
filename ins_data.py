import os
import serial
import sys
import threading
import time
from reader import ins

# Main
reader = ins()
reader.connect()
if reader.isClosed() == False:
    read_thread = threading.Thread(target=reader.dump)
    read_thread.start()
    read_thread.join()
else:
    print "Could not connect!"