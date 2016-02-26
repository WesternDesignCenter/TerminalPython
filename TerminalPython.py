##Simple Python Script that will interface with WDC's W65C134SXB and W65C265SXB Boards.
##You can use this as a start to customize the interface for your needs.  
##NOTE:  Change Line 14 to have the proper COM port or it will not work!
##import serial lib
##import msvcrt
import serial
import io
import time

try: 
	from msvcrt import getch 
except ImportError: 
	''' we're not on Windows, so we try the Unix-like approach '''

	def getch( ): 
		import sys, tty, termios 
		fd = sys.stdin.fileno( ) 
		old_settings = termios.tcgetattr(fd) 
		try: 
			tty.setraw(fd) 
			ch = sys.stdin.read(1) 
		finally: 
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
			return ch

##open serial port
print ("Welcome to WDC's 65xx Serial Monitor in Python");
print ("Press the reset button on your board to start reading serial data from the board");
## For now the Serial Port Needs to be set manually.  Change the line below to your COMXX port
ser = serial.Serial("/dev/tty.usbserial-A703XC1I", 9600,timeout=1)
ser.flushInput()
ser.flushOutput()
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
readser = 1
#while loop to read in serial data
#line will autofeed if reset is not pushed at beginning
while readser == 1:
	hello = sio.readline()
	#testing
	#
	if hello:
		if "Copyright 1995" in hello: 
			hello = hello.replace("1995", "1995-2014");	##Just an example of replacing text. Not needed.
			print hello;
		elif hello.strip() == '>': 
			readser = 0
			print ("Enter a command.  For a list of commands press h");
			print hello;
			writedata = getch()
			ser.write(writedata)
			readser = 1
		elif "BB:AAAA" in hello: 
			readser = 0
			print hello;
			print ("Type in a 2 digit Bank Address - Press Enter");
			writedata = raw_input()
			if len(writedata) == 2:
				ser.write(writedata)
				readser = 1
			else:
				print ("Please re-enter the 2 digit hex Bank Address and press enter");
				writedata = raw_input()
				readser = 1
		elif hello.endswith(':'): 
			readser = 0
			print hello;
			print ("Type in a 4 digit Address - Press Enter");
			writedata = raw_input()
			if len(writedata) == 4:
				ser.write(writedata)
				readser = 1
			else:
				print ("Please re-enter the 4 digit hex address and press enter");
				writedata = raw_input()
				readser = 1	
		else:
			print hello;

##close serial connection
ser.close()
print ("Closing out!");
