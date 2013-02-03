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
from evdev import InputDevice, list_devices, categorize, ecodes

direction = 'Pause'	# Forward, Pause, Right, Left, Backward, BackRight, BackLeft
mouse_click = False
stop_listen = False
enableA = 1
enableB = 6

h1 = 15
h2 = 16
h3 = 11
h4 = 10

obsA = 14
obsB = 7


class MouseListener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global direction
		global stop_listen
		global mouse_click

		dev = InputDevice('/dev/input/event1')
		print(dev)

		for event in dev.read_loop():
			#print event
			mouse_click = True

			if event.code == 272 and event.type == 1 and event.value == 0 :
				print 'Left press'
				if direction == 'Forward':
					direction = 'Left'
				elif direction == 'Right':
					direction = 'Forward'
			if event.code == 273 and event.type == 1 and event.value == 0 :
				print 'Right press'
				if direction == 'Forward':
					direction = 'Right'
				elif direction == 'Left':
					direction = 'Forward'
			if event.code == 274 and event.type == 1 and event.value == 0 :
				print 'Middle press'
				if direction == 'Forward' or direction == 'Right' or direction == 'left' or direction == 'Backward':
					direction = 'Pause'
				else:
					direction = 'Forward'
			if event.code == 8 and event.type == 2 and event.value == 1 :
				print 'scroll up'
				if direction == 'Pause':
					direction = 'Forward'
				elif direction == 'Backward':
					direction = 'Pause'
			if event.code == 8 and event.type == 2 and event.value == -1 :
				print 'scroll down'
				if direction == 'Pause':
					direction = 'Backward'
				elif direction == 'Forward':
					direction = 'Pause'

			if stop_listen == True:
				break


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

def backward():
	wiringpi.softPwmWrite(enableA, 200)
	wiringpi.digitalWrite(h1, 1)
	wiringpi.digitalWrite(h2, 0)
	wiringpi.softPwmWrite(enableB, 200)
	wiringpi.digitalWrite(h3, 1)
	wiringpi.digitalWrite(h4, 0)

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
wiringpi.pinMode(obsA, wiringpi.INPUT)
wiringpi.pinMode(obsB, wiringpi.INPUT)


mthread = startMouse()

while True:
	valueA = wiringpi.digitalRead(obsA)
	valueB = wiringpi.digitalRead(obsB)

	print 'obsA:', valueA, 'obsB:', valueB

	if valueA == 0 or valueB == 0:
		if direction == 'Pause':
			stop()
		else:
			turnLeft()
			sleep(1)
			forward()
			direction = 'Forward'
	else:
		if mouse_click == False:
			if direction != 'Pause' and direction != 'Backward' :
				ran = random.randint(1, 6)
				if ran == 1:
					if direction == 'Forward':
						direction = 'Left'
					elif direction == 'Right':
						direction = 'Forward'
				elif ran == 2:
					if direction == 'Forward':
						direction = 'Right'
					elif direction == 'Left':
						direction = 'Forward'
				else:
					direction = 'Forward'
		else:
			mouse_click = False

		if direction == 'Forward':
			forward()
		elif direction == 'Pause':
			stop()
		elif direction == 'Left':
			turnLeft()
		elif direction == 'Right':
			turnRight()
		elif direction == 'Backward':
			backward()

	try:
		sleep(1)
	except KeyboardInterrupt:
		stop_listen = True
		raise
