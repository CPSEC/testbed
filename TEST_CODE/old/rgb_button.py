import RPi.GPIO as GPIO
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 200
pca.channels[0].duty_cycle = 0xffff
pca.channels[2].duty_cycle = 0xffff

channels = [0, 1, 2]
counter = 0

def callback(channel):
    global counter
    i = counter % 3
    pca.channels[channels[i]].duty_cycle = 0xffff
    for j in [x for x in channels if x != i]:
        pca.channels[j].duty_cycle = 0x0000
    counter += 1

GPIO.add_event_detect(4, GPIO.RISING, callback=callback, bouncetime=500)

try:
    while(True):
        time.sleep(2)

except KeyboardInterrupt:
    pca.channels[0].duty_cycle = 0x0000
    pca.channels[1].duty_cycle = 0x0000
    pca.channels[2].duty_cycle = 0x0000
    GPIO.cleanup()
