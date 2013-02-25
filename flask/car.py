# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request
import datetime
from time import sleep
import wiringpi
import threading

app = Flask(__name__)

class CarLoopThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global direction
        while True:
            valueA = wiringpi.digitalRead(obsA)
            valueB = wiringpi.digitalRead(obsB)

            #print 'obsA:', valueA, 'obsB:', valueB

            if valueA == 0 or valueB == 0:
                if direction == 'Pause':
                    pass
                else:
                    doGoBackward()
                    sleep(0.5)
                    doTurnLeft()
                    sleep(0.5)
                    doGoForward()
                    direction = 'Forward'
            #else:
            #    if direction == 'Forward':
            #        doGoForward()
            #    elif direction == 'Pause':
            #        doStop()
            #    elif direction == 'Left':
            #        doTurnLeft()
            #        direction = 'Forward'
            #    elif direction == 'Right':
            #        doTurnRight()
            #        direction = 'Forward'
            #    elif direction == 'Backward':
            #        doGoBackward()

            if threadExit == True:
                break

            sleep(0.5)


def startCarLoop():
    thread = CarLoopThread()
    thread.start()
    return thread

direction = 'Pause' # Forward, Pause, Right, Left, Backward, BackRight, BackLeft
threadExit = False
enableA = 1
enableB = 6

h1 = 15
h2 = 16
h3 = 11
h4 = 10

obsA = 14
obsB = 7

def doGoForward():
    #wiringpi.softPwmWrite(enableA, 255)
    wiringpi.digitalWrite(h1, 0)
    wiringpi.digitalWrite(h2, 1)
    #wiringpi.softPwmWrite(enableB, 255)
    wiringpi.digitalWrite(h3, 0)
    wiringpi.digitalWrite(h4, 1)

def doGoBackward():
    #wiringpi.softPwmWrite(enableA, 255)
    wiringpi.digitalWrite(h1, 1)
    wiringpi.digitalWrite(h2, 0)
    #wiringpi.softPwmWrite(enableB, 255)
    wiringpi.digitalWrite(h3, 1)
    wiringpi.digitalWrite(h4, 0)

def doStop():
    #wiringpi.softPwmWrite(enableA, 0)
    #wiringpi.softPwmWrite(enableB, 0)
    wiringpi.digitalWrite(h1, 0)
    wiringpi.digitalWrite(h2, 0)
    wiringpi.digitalWrite(h3, 0)
    wiringpi.digitalWrite(h4, 0)


def doTurnRight():
    #wiringpi.softPwmWrite(enableA, 255)
    wiringpi.digitalWrite(h1, 0)
    wiringpi.digitalWrite(h2, 1)
    #wiringpi.softPwmWrite(enableB, 255)
    wiringpi.digitalWrite(h3, 1)
    wiringpi.digitalWrite(h4, 0)

def doTurnLeft():
    #wiringpi.softPwmWrite(enableA, 255)
    wiringpi.digitalWrite(h1, 1)
    wiringpi.digitalWrite(h2, 0)
    #wiringpi.softPwmWrite(enableB, 255)
    wiringpi.digitalWrite(h3, 0)
    wiringpi.digitalWrite(h4, 1)


wiringpi.wiringPiSetup()
wiringpi.pinMode(enableA, 1)
wiringpi.pinMode(h1, 1)
wiringpi.pinMode(h2, 1)
wiringpi.pinMode(enableB, 1)
wiringpi.pinMode(h3, 1)
wiringpi.pinMode(h4, 1)
#wiringpi.softPwmCreate(enableA, 0, 255)
#wiringpi.softPwmCreate(enableB, 0, 255)
wiringpi.digitalWrite(enableA, 1)
wiringpi.digitalWrite(enableB, 1)
wiringpi.pinMode(obsA, wiringpi.INPUT)
wiringpi.pinMode(obsB, wiringpi.INPUT)



@app.route('/forward')
def forward():
    """forward"""
    global direction
    print 'forward'
    if direction == 'Pause':
        direction = 'Forward'
    elif direction == 'Backward':
        direction = 'Pause'
    doGoForward()
    return ''

@app.route('/stop')
def stop():
    """stop"""
    global direction
    print 'stop'
    direction = 'Pause'
    doStop()
    return ''

@app.route('/reverse')
def reverse():
    """reverse"""
    global direction
    print 'reverse'
    if direction == 'Pause':
        direction = 'Backward'
    elif direction == 'Forward':
        direction = 'Pause'
    doGoBackward()
    return ''

@app.route('/left')
def left():
    """left"""
    global direction
    print 'left'
    if direction == 'Forward':
        direction = 'Left'
    elif direction == 'Right':
        direction = 'Forward'
    doTurnLeft()
    sleep(0.5)
    doGoForward()
    return ''

@app.route('/right')
def right():
    """right"""
    global direction
    print 'right'
    if direction == 'Forward':
        direction = 'Right'
    elif direction == 'Left':
        direction = 'Forward'
    doTurnRight()
    sleep(0.5)
    doGoForward()
    return ''

@app.route('/')
def index():
    print 'index'
    return render_template('index.html')


if __name__ == '__main__':
    startCarLoop()
    app.run(host='0.0.0.0', port=8090, debug=True)
