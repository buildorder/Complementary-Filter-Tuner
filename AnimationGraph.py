import serial
import math
import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np

from multiprocessing import Process

ser = serial.Serial()
ser.port = 'COM7'
ser.baudrate = 57600
ser.open()

XANGLE = 0;
YANGLE = 0;

def complementaryFilter(Buffer):
    global XANGLE
    global YANGLE

    # Convert Gyro Data / LSB is 131.0
    gyroX = float(Buffer[3]) / 131.0
    gyroY = float(Buffer[4]) / 131.0

    # Convert Accel Data /
    accX = math.atan2(int(Buffer[0]), int(Buffer[2])) * 180 / math.pi
    accY = math.atan2(int(Buffer[1]), int(Buffer[2])) * 180 / math.pi

    # ComplementaryFilter
    XANGLE = ( 0.98 * (XANGLE + ( gyroX * 0.001) ) + (0.02 * accX ) )
    YANGLE = ( 0.98 * (YANGLE + ( gyroY * 0.001) ) + (0.02 * accY ) )

def getIMUData():
    ser.write(2)

    if(ser.inWaiting() > 0):
        dataBytes = ser.readline()

        dataBuffer=dataBytes[:-2].decode()
        splitBuffer=dataBuffer.split("|")

        ComplementaryFilter(splitBuffer)

def drawGraph(number) :
    getIMUData_process = Process(target = getIMUData)
    getIMUData_process.start()

    graph_one.set_xdata(np.arange(number))
    graph_one.set_ydata(XANGLE)
    graph_window_one.set_xlim(number - 10, number)

    getIMUData_process.join()
    return graph_one

if __name__=='__main__':
    # Create Main Window & Graph Window
    main_window = plt.figure();
    graph_window_one = main_window.add_subplot(1, 1, 1)

    # Set Y Axis Scale
    graph_window_one.set_ylim(-90, 90)

    graph_one, = graph_window_one.plot([])

    ani = animation.FuncAnimation(main_window, drawGraph, interval=1)
    plt.show()
