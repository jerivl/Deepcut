# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import numpy as np
import sys

import Adafruit_PCA9685

if __name__ == "__main__":
    dur = float(sys.argv[1])
    bpm = int(sys.argv[2])
    # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

    # Alternatively specify a different address and/or bus:
    #pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096
    servo_h = 375

    # Set frequency to 60hz, good for servos.
    pwm_freq = 60
    pwm.set_pwm_freq(pwm_freq)

    dt = 8 / pwm_freq
    t = np.arange(0,dur,dt)

    rng = (servo_max - servo_min) / 2
    zero_pt = (servo_max + servo_min) / 2
    motor1 = list(np.floor(rng*np.sin(np.pi * t * bpm/120 )+zero_pt).astype(int))
    motor2 = list(np.floor(rng*np.cos(np.pi * t * bpm/120 )+zero_pt).astype(int))
    print(type(motor1), type(motor2))
    print(type(motor1[0]), type(motor2[0]))
    print('Moving servo on channel 5 & 8, press Ctrl-C to quit...')

    #import time
    #time.sleep(1.15)
    for m1,m2 in zip(motor1, motor2):
        pwm.set_pwm(11, 11, m1)
        pwm.set_pwm(12, 12, m2)
        time.sleep(dt)
        
    pwm.set_pwm(11, 11, int(np.floor(servo_min)))
    pwm.set_pwm(12, 12, int(np.floor(servo_max)))
