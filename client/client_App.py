#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import socket as sock      # Import necessary modules
import sys
from optparse import OptionParser

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

# Handle options
parser = OptionParser()
parser.add_option("-s", "--server", dest="serverIP", help="server IP")
(options, args) = parser.parse_args()
if not options.serverIP:
	print('The server IP must be provided')
	sys.exit(1)

topWindow = tk.Tk()   # Create a top window
topWindow.title('Sunfounder Raspberry Pi Smart Video Car')

HOST = options.serverIP    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server

# =============================================================================
# The function is to send the command forward to the server, so as to make the 
# car move forward.
# =============================================================================
def sendCmd(cmd):
	print('send command:', cmd)
	tcpCliSock.send(cmd.encode())


def forward_fun(event):
	sendCmd('forward')

def backward_fun(event):
	sendCmd('backward')

def left_fun(event):
	sendCmd('left')

def right_fun(event):
	sendCmd('right')

def stop_fun(event):
	sendCmd('stop')

def home_fun(event):
	sendCmd('center')

def x_increase(event):
	sendCmd('x+')

def x_decrease(event):
	sendCmd('x-')

def y_increase(event):
	sendCmd('y+')

def y_decrease(event):
	sendCmd('y-')

def xy_home(event):
	sendCmd('xy_home')

# =============================================================================
# Exit the GUI program and close the network connection between the client 
# and server.
# =============================================================================
def quit_fun(event):
	topWindow.quit()
	tcpCliSock.send('stop'.encode())
	tcpCliSock.close()

# =============================================================================
# Create buttons
# =============================================================================
BtnFwd = tk.Button(topWindow, width=5, text='Forward')
BtnBwd = tk.Button(topWindow, width=5, text='Backward')
BtnLeft = tk.Button(topWindow, width=5, text='Left')
BtnRight = tk.Button(topWindow, width=5, text='Right')
BtnQuit = tk.Button(topWindow, width=5, text='Quit')
BtnCenter = tk.Button(topWindow, width=5, height=2, text='Center')

# =============================================================================
# Buttons layout
# =============================================================================
BtnFwd.grid(row=0, column=1)
BtnBwd.grid(row=2, column=1)
BtnLeft.grid(row=1, column=0)
BtnRight.grid(row=1, column=2)
BtnQuit.grid(row=3, column=2)
BtnCenter.grid(row=1, column=1)

# =============================================================================
# Bind the buttons for the car movements
# =============================================================================
BtnFwd.bind('<ButtonPress-1>', forward_fun)  # When button0 is pressed down, call the function forward_fun().
BtnFwd.bind('<ButtonRelease-1>', stop_fun)   # When button0 is released, call the function stop_fun().
BtnBwd.bind('<ButtonPress-1>', backward_fun)
BtnBwd.bind('<ButtonRelease-1>', stop_fun)
BtnLeft.bind('<ButtonPress-1>', left_fun)
BtnLeft.bind('<ButtonRelease-1>', stop_fun)
BtnRight.bind('<ButtonPress-1>', right_fun)
BtnRight.bind('<ButtonRelease-1>', stop_fun)
BtnQuit.bind('<ButtonRelease-1>', quit_fun)
BtnCenter.bind('<ButtonRelease-1>', home_fun)

# =============================================================================
# Create buttons for the camera movements
# =============================================================================
BtnXPlus = tk.Button(topWindow, width=5, text='X+', bg='red')
BtnXMinus = tk.Button(topWindow, width=5, text='X-', bg='red')
BtnYMinus = tk.Button(topWindow, width=5, text='Y-', bg='red')
BtnYPlus = tk.Button(topWindow, width=5, text='Y+', bg='red')
BtnHome = tk.Button(topWindow, width=5, height=2, text='HOME', bg='red')

# =============================================================================
# Buttons layout
# =============================================================================
BtnXPlus.grid(row=1, column=5)
BtnXMinus.grid(row=1, column=3)
BtnYMinus.grid(row=2, column=4)
BtnYPlus.grid(row=0, column=4)
BtnHome.grid(row=1, column=4)

# =============================================================================
# Bind button events
# =============================================================================
BtnXPlus.bind('<ButtonPress-1>', x_increase)
BtnXMinus.bind('<ButtonPress-1>', x_decrease)
BtnYMinus.bind('<ButtonPress-1>', y_decrease)
BtnYPlus.bind('<ButtonPress-1>', y_increase)
BtnHome.bind('<ButtonPress-1>', xy_home)
#Btn07.bind('<ButtonRelease-1>', home_fun)
#Btn08.bind('<ButtonRelease-1>', home_fun)
#Btn09.bind('<ButtonRelease-1>', home_fun)
#Btn10.bind('<ButtonRelease-1>', home_fun)
#Btn11.bind('<ButtonRelease-1>', home_fun)

# =============================================================================
# Bind buttons on the keyboard with the corresponding callback function to 
# control the car remotely with the keyboard.
# =============================================================================
topWindow.bind('<KeyPress-a>', left_fun)   # Press down key 'A' on the keyboard and the car will turn left.
topWindow.bind('<KeyPress-d>', right_fun)
topWindow.bind('<KeyPress-s>', backward_fun)
topWindow.bind('<KeyPress-w>', forward_fun)
topWindow.bind('<KeyPress-h>', home_fun)
topWindow.bind('<KeyRelease-a>', home_fun) # Release key 'A' and the car will turn back.
topWindow.bind('<KeyRelease-d>', home_fun)
topWindow.bind('<KeyRelease-s>', stop_fun)
topWindow.bind('<KeyRelease-w>', stop_fun)

spd = 50

def changeSpeed(ev=None):
	tmp = 'speed'
	global spd
	spd = speed.get()
	data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'. 
	print('sendData = %s' % data)
	tcpCliSock.send(data.encode())  # Send the speed data to the server(Raspberry Pi)


label = tk.Label(topWindow, text='Speed:', fg='red')  # Create a label
label.grid(row=6, column=0)                  # Label layout

speed = tk.Scale(topWindow, from_=0, to=100, orient=tk.HORIZONTAL, command=changeSpeed)  # Create a scale
speed.set(50)
speed.grid(row=6, column=1)

def main():
	topWindow.mainloop()

if __name__ == '__main__':
	main()

