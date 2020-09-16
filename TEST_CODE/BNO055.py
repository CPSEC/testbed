# wiring
# SCL  ----  SCL6   GPIO23
# SDA  ----  SDA6   GPIO22

# add 2 rows into /boot/config.txt
# # Additional overlays and parameters are documented /boot/overlays/README
# dtoverlay=i2c6

# pip3 install adafruit-extended-bus
# pip3 install adafruit-circuitpython-bno055

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055

# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected
i2c = I2C(6)  # Device is /dev/i2c-1
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    print("Temperature: {} degrees C".format(sensor.temperature))
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(1)