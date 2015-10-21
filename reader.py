from threading import Thread
import sys
import subprocess
import os
import serial
import threading
import time

class rplidar:
    
    location = 'bin/Debug/./rplidar_custom ' # Path to the RPLIDAR Program
    device = '/dev/ttyUSB0' # Path to serial device
    subproc = None # Contains the subprocess associated with the RPLIDAR Program
    
    def __init__(self, location = 'bin/Debug/./rplidar_custom ', device = '/dev/ttyUSB0'):
        self.location = location
        self.device = device
        
    def connect(self):
        self.subproc = subprocess.Popen(self.location+self.device,shell=True,stdout=subprocess.PIPE)
        if self.isClosed() == False:
            return True
        return False
        
    def disconnect(self):
        self.subproc.kill() 
        if self.isClosed() == True:
            return True
        self.subproc = None #Force kill
        return False #Show that the force kill took place
    
    def readline(self):
        if self.isClosed() == False:
            return self.subproc.stdout.readline()
        return None
        
    def getProcess(self):
        return self.subproc
        
    def isClosed(self):
        return self.subproc.stdout.closed 
    
    def dump(self):
        while self.isClosed() == False:
            print self.subproc.stdout.readline()
    
    
class ins:
    
    device = '/dev/ttyACM0' # Path to the serial port
    conn = None # Contains the connection associated with the serial port
    
    def __init__(self, device = '/dev/ttyACM0'):
        self.device = device
        
    def __out(self,msg):
        print(msg)
        sys.stdout.flush()
        
    def connect(self):
        fd = os.open(self.device,os.O_RDONLY)
        serial_port = os.ttyname(fd)
    
        time.sleep(1)

        #self.__out("Connecting to serial {}".format(serial_port))
        self.conn = serial.Serial(serial_port, timeout=0,baudrate=115200)
        self.conn.nonblocking()
        if self.conn == None:
            #self.__out("Failed to connect!")
            return False
        #self.__out("Connected! Performing software reset...")
        self.conn.write("reset")
        self.conn.flushInput()
        #self.__out("Ready to read!")
        
        return True;
        
    def disconnect(self):
        self.conn.close() 
        if self.isClosed():
            return True
        self.conn = None #Force kill
        return False #Show that the force kill took place
    
    def readline(self):
        if self.isReadable():
            return self.conn.readline()
        return None
        
    def getConnection(self):
        return self.conn
        
    def isClosed(self):
        return (self.conn.isOpen() == False)
    
    def isReadable(self):
        return self.conn.readable()
    
    def dump(self):
        while self.conn.readable():
            output = self.conn.readline() # Try and read line
            while '\n' not in output: # If line not read correctly/buffered
                output = output + self.conn.read(0x4) # Read byte by byte until full line is present
            self.__out("{}".format(output).strip())
        