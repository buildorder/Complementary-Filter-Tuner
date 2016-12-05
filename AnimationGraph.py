import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
import serial
import math

# Open Serial Port
ser = serial.Serial()
ser.port = 'COM7'
ser.baudrate = 115200
ser.open()

# Graph Datas
xArr = []
yArr = []
XANGLE = 0
YANGLE = 0
prev_data = -1

#setup figure
fig = plt.figure()

# Create X Window
x_window = fig.add_subplot(2,1,2)
x_window.grid(True)
x_window.set_xlabel('X Axis')
x_window.set_ylim(-90, 90)

# Create Y Window
y_window = fig.add_subplot(2,1,1)
y_window.grid(True)
y_window.set_xlabel('Y Axis')
y_window.set_ylim(-90, 90)

# Plot X, Y graph
x_graph, = x_window.plot([], [], color=(0,0,1))
y_graph, = y_window.plot([], [], color=(0,0,1))

def printF(Buffer, n):
    global XANGLE
    global YANGLE

    gyroX = float(Buffer[3]) / 131.0
    gyroY = float(Buffer[4]) / 131.0

    accX = math.atan2(int(Buffer[0]), int(Buffer[2])) * 180 / math.pi
    accY = math.atan2(int(Buffer[1]), int(Buffer[2])) * 180 / math.pi

    XANGLE = ( float(Buffer[5]) * (XANGLE + ( gyroX * 0.001) ) + ( (1.0 - float(Buffer[5])) * accX ))
    YANGLE = ( float(Buffer[5]) * (YANGLE + ( gyroY * 0.001) ) + ( (1.0 - float(Buffer[5])) * accY ))

    xArr.append(XANGLE)
    yArr.append(YANGLE)

    print(Buffer[5])

def func(n):

    global prev_data

    if( prev_data != n ):
        while(True):
            ser.write(2)

            if(ser.inWaiting() > 0):
                break

        dataBytes = ser.readline()

        dataBuffer = dataBytes[:-2].decode()
        splitBuffer = dataBuffer.split("|")
        printF(splitBuffer, n)

        x_graph.set_xdata(np.arange(n+1))
        x_graph.set_ydata(xArr)
        x_window.set_xlim(n-50, n)

        y_graph.set_xdata(np.arange(n+1))
        y_graph.set_ydata(yArr)
        y_window.set_xlim(n-50, n)

    prev_data = n
    return x_graph, y_graph

ani = animation.FuncAnimation(fig, func, interval=1, blit=True)

plt.show()
