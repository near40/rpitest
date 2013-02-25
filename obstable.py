import wiringpi
from time import sleep

wiringpi.wiringPiSetup()

obsA = 14
obsB = 7


wiringpi.pinMode(obsA, wiringpi.INPUT)
wiringpi.pinMode(obsB, wiringpi.INPUT)

while True:
	valueA = wiringpi.digitalRead(obsA)
	valueB = wiringpi.digitalRead(obsB)
	print valueA, valueB
	sleep(1)
