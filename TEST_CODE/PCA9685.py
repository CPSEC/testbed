# wiring
# SCL  ----  SCL1
# SDA  ----  SDA1
# ch3  ----  HC-SR04
# ch7  ----  Motor
# ch11 ----  Servo

# pip install adafruit-circuitpython-pca9685
# pip install adafruit-circuitpython-motor

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50

servo3 = servo.Servo(pca.channels[3])


for i in range(180):
    servo3.angle = i
for i in range(180):
    servo3.angle = 180 - i

servo3.angle = 90
pca.deinit()
