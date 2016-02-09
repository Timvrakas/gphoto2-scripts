#! /usr/bin/env python

# adapted from https://forum.pjrc.com/threads/25295-Automatically-find-a-Teensy-Board-with-Python-and-PySerial


import io, re, serial, sys
from serial.tools import list_ports

# grab the mLine-th line
mLine = 2

# Arduino board values  (use command to gather info, if needed):
# python -m serial.tools.list_ports -v
VENDOR_ID = "2341"
PRODUCT_ID = "8036"

# find the Arduino board's serial port.  based on example found at:
# https://forum.pjrc.com/threads/25295-Automatically-find-a-Teensy-Board-with-Python-and-PySerial
def getIMUPort():
    for port in list(list_ports.comports()):
        matchString = "USB VID:PID=%s:%s"%(VENDOR_ID, PRODUCT_ID)
        matchObj = re.match( matchString, port[2], re.M|re.I )
        if matchObj:
            return port[0]

def setIMUPort(thePort, ser):
     ser.baudrate = 9600
     ser.port = IMUPort
     ser.timeout = 1
#     print ser

# simple line reader.  based on snippet found at:
# http://stackoverflow.com/questions/10222788/line-buffered-serial-input
def readLine(ser):
    str = ""
    while 1:
        ch = ser.read()
        if(ch == '\m' or ch == '' or ch == '\n' or ch == '\r'):  
            break
        str += ch
    return str

if __name__ == "__main__":

	IMUPort = getIMUPort()

# if the board is there, open a serial connection
	if IMUPort:
	    print "IMU found on port %s"%IMUPort
            ser = serial.Serial()
            setIMUPort(IMUPort, ser)
            ser.open()

# to allow for incomplete line fill, output the 2nd non-blank line
            icount = 0
            while True:
                line = readLine(ser)
                if len(line) != 0:
                    icount = icount + 1
                if icount == mLine:
                    print line
                    break

# close port
            ser.close()

# parse the line (first 7 fields are separated by ';', but the 7th switches to
# space delimited...split these and grab just the calibration flags and add
# to the end of the FIELDS array
            fields = line.split(';')
            group2 =  fields[6].split()
            fields[6] = group2[0]
            flagStr = group2[2:6]
            for flag in flagStr:
                flagVal = flag.split('=')[1]
                fields.append(flagVal)
# values are already "formatted" in the FIELDS list (comma trick is probably
# broken in python 3)
            for val in fields:
                 print val,

	else:
	    print "No compatible Arduino board found. Aborting."
	    sys.exit(1)
