#scratchcomm.py
#connect to scratch and receive the value of "green" sensor
#if "green" value is 0, turn of LED connected to GPIO 4
#else turn on the LED
#Date:		2013-1-26
#Author:	JimmyWang
#Email:		JimmyWang.tj@gmail.com


import scratch
import RPi.GPIO as GPIO
import time

GreenPin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(GreenPin, GPIO.OUT)

def start_blink():
	GPIO.output(GreenPin, GPIO.HIGH)

def stop_blink():
	GPIO.output(GreenPin, GPIO.LOW)


#s = scratch.Scratch(host='0.0.0.0')
s = scratch.Scratch()

def listen():
	while True:
		try:
			yield s.receive()
		except scratch.ScratchError:
			raise StopIteration

for msg in listen():
	if msg[0] == 'boradcast':
		print(msg)
	elif msg[0] == 'sensor-update':
		print(msg)
		sensor = msg[1]
		if sensor.has_key('green'):
			if sensor['green'] == 0:
				stop_blink()
			else:
				start_blink()

exit()
