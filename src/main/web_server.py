#!/usr/bin/env python3

import logging
import time
from RPi import GPIO
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Set log level
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('pos')
def program_pos(msx, msy):
    logging.info("pos %d,%d", msx, msy)

@socketio.on('light')
def program_light(flag):
    logging.info("light flag %d", flag)

@socketio.on('cam')
def program_cam(flag):
    logging.info("cam flag %d", flag)

@socketio.on('power')
def program_power(flag):
    logging.info("power flag %d", flag)

@socketio.on('disconnect')
def program_disconnect():
    logging.info("disconnect")


class Motor:
    """ An interface for motor control."""

    def __init__(self, channelA, channelB):
        self._channelA = channelA
        self._channelB = channelB
        GPIO.setup(channelA, GPIO.OUT)
        GPIO.setup(channelB, GPIO.OUT)
        self._pwmA = GPIO.PWM(channelA, 100)    # frequency : 100 Hz
        self._pwmB = GPIO.PWM(channelB, 100)    # frequency : 100 Hz
        self._pwmA.start(0)
        self._pwmB.start(0)

    def close(self):
        self._pwmA.stop()
        self._pwmB.stop()
        GPIO.cleanup(self._channelA)
        GPIO.cleanup(self._channelB)

    def set_speed(self, speed):  # Speed range (-100 ~ 100)
        if (speed >= 0):
            self._pwmA.ChangeDutyCycle(0)
            self._pwmB.ChangeDutyCycle(speed)
        else:
            self._pwmA.ChangeDutyCycle(-speed)
            self._pwmB.ChangeDutyCycle(0)


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    # Assign Motor
    motor_up_left  = Motor(0, 5)
    motor_up_right = Motor(6, 13)
    motor_dn_left  = Motor(25, 8)
    motor_dn_right = Motor(1, 12)
    motor_waist    = Motor(16, 20)

    while True:
        motor_up_left.set_speed(20)
        motor_up_right.set_speed(80)
        motor_dn_left.set_speed(30)
        motor_dn_right.set_speed(70)
        motor_waist.set_speed(50)
        time.sleep(5)

        motor_up_left.set_speed(-20)
        motor_up_right.set_speed(-80)
        motor_dn_left.set_speed(-30)
        motor_dn_right.set_speed(-70)
        motor_waist.set_speed(-50)
        time.sleep(5)


    socketio.run(app, host='0.0.0.0', port=8080, debug=False, use_reloader=False)
