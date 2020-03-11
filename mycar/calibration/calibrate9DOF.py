import os
import json
import time
from Adafruit_BNO055 import BNO055

bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=21)

if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')
# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

# LOAD json
CALIBRATION_FILE = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'calibration.json')
with open(CALIBRATION_FILE, 'r') as cal_file:
    data = json.load(cal_file)
    bno.set_calibration(data)

try:
    while True:
        sys, gyro, accel, mag = bno.get_calibration_status()
        print('sys=', sys, '  gyro=', gyro, '  accel=', accel, '  mag=', mag, end='\r', flush=True)
        time.sleep(0.2)
except KeyboardInterrupt:
    print('\nQuit...')