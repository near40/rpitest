#car.py
#Drive L298N
#Date:		2013-2-2
#Author:	JimmyWang
#Email:		JimmyWang.tj@gmail.com

from time import sleep
import wiringpi
import threading
import time
import sys
import random

direction = 'Forward'	# Forward, Pause, Right, Left
mouse_click = False
stop_listen = False
enableA = 1
enableB = 6

h1 = 15
h2 = 16
h3 = 10
h4 = 11

class MouseListener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.fd = open('/dev/input/mouse0', 'r')

	def run(self):
		global direction
		global stop_listen
		global mouse_click
		while 1:
			if stop_listen == True:
				break

			buttons, dx, dy = map(ord, self.fd.read(3))
			mouse_click = True

			if buttons == 0x9 and dx == 0 and dy == 0:
				print 'left pressed'
				if direction == 'Forward':
					direction = 'Left'
				elif direction == 'Right':
					direction = 'Forward'
			elif buttons == 0xa and dx == 0 and dy == 0:
				print 'right pressed'
				if direction == 'Forward':
					direction = 'Right'
				elif direction == 'Left':
					direction = 'Forward'
			elif buttons == 0xc and dx == 0 and dy == 0:
				print 'middle pressed'
				if direction == 'Forward' or direction == 'Right' or direction == 'left':
					direction = 'Pause'
				else:
					direction = 'Forward'


def startMouse():
	thread = MouseListener()
	thread.start()
	return thread

def forward():
	wiringpi.softPwmWrite(enableA, 200)
	wiringpi.digitalWrite(h1, 0)
	wiringpi.digitalWrite(h2, 1)
	wiringpi.softPwmWrite(enableB, 200)
	wiringpi.digitalWrite(h3, 0)
	wiringpi.digitalWrite(h4, 1)

def stop():
	wiringpi.softPwmWrite(enableA, 0)
	wiringpi.softPwmWrite(enableB, 0)


def turnRight():
	wiringpi.softPwmWrite(enableA, 200)
	wiringpi.digitalWrite(h1, 1)
	wiringpi.digitalWrite(h2, 0)
	wiringpi.softPwmWrite(enableB, 200)
	wiringpi.digitalWrite(h3, 0)
	wiringpi.digitalWrite(h4, 1)

def turnLeft():
	wiringpi.softPwmWrite(enableA, 200)
	wiringpi.digitalWrite(h1, 0)
	wiringpi.digitalWrite(h2, 1)
	wiringpi.softPwmWrite(enableB, 200)
	wiringpi.digitalWrite(h3, 1)
	wiringpi.digitalWrite(h4, 0)


wiringpi.wiringPiSetup()
wiringpi.pinMode(enableA, 1)
wiringpi.pinMode(h1, 1)
wiringpi.pinMode(h2, 1)
wiringpi.pinMode(enableB, 1)
wiringpi.pinMode(h3, 1)
wiringpi.pinMode(h4, 1)
wiringpi.softPwmCreate(enableA, 0, 255)
wiringpi.softPwmCreate(enableB, 0, 255)


mthread = startMouse()

while True:
	if mouse_click == True:
		mouse_click = False
		if direction == 'Forward':
			forward()
		elif direction == 'Pause':
			stop()
		elif direction == 'Left':
			turnLeft()
		elif direction == 'Right':
			turnRight()
	else:
		if direction != 'Pause' :
			ran = random.randint(1, 6)
			if ran == 1:
				if direction == 'Forward':
					direction = 'Left'
					turnLeft()
				elif direction == 'Right':
					direction = 'Forward'
					forward()
			elif ran == 2:
				if direction == 'Forward':
					direction = 'Right'
					turnRight()
				elif direction == 'Left':
					direction = 'Forward'
					forward()
			else:
				direction = 'Forward'
				forward()

	try:
		sleep(1)
	except KeyboardInterrupt:
		stop_listen = True
		raise
