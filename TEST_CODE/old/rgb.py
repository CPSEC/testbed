from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 200
pca.channels[0].duty_cycle = 0xffff
pca.channels[1].duty_cycle = 0x0000
pca.channels[2].duty_cycle = 0xffff


try:
    while(True):
        time.sleep(2)

except KeyboardInterrupt:
    pca.channels[0].duty_cycle = 0x0000
    pca.channels[1].duty_cycle = 0x0000
    pca.channels[2].duty_cycle = 0x0000
