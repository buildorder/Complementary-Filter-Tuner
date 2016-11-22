import serial
import math

ser = serial.Serial()
ser.port = 'COM7'
ser.baudrate = 57600
ser.open()

XANGLE = 0;
YANGLE = 0;

def ComplementaryFilter(Buffer):

    global XANGLE
    global YANGLE

    gyroX = float(Buffer[3]) / 131.0
    gyroY = float(Buffer[4]) / 131.0

    accX = math.atan2(int(Buffer[0]), int(Buffer[2])) * 180 / math.pi
    accY = math.atan2(int(Buffer[1]), int(Buffer[2])) * 180 / math.pi

    XANGLE = ( 0.98 * (XANGLE + ( gyroX * 0.001) ) + (0.02 * accX ) )
    YANGLE = ( 0.98 * (YANGLE + ( gyroY * 0.001) ) + (0.02 * accY ) )

    print("XANGLE : {0}   YANGLE : {1}".format("%0.4f" % XANGLE, "%0.4f" % YANGLE) )

while(True):

    if(ser.inWaiting() > 0):
        dataBytes = ser.readline()

        dataBuffer = dataBytes[:-2].decode()
        splitBuffer  =dataBuffer.split("|")

        ComplementaryFilter(splitBuffer)
