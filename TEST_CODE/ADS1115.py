import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create ADC object
ads = ADS.ADS1015(i2c)

POWER_CHANNEL_MOTOR = ADS.P3 # A3 on board
POWER_CHANNEL_PI    = ADS.P2 # A2 on board

chan_motor = AnalogIn(ads, POWER_CHANNEL_MOTOR)
chan_pi    = AnalogIn(ads, POWER_CHANNEL_PI)

try:
    while True:
        print("Motor: {:>5}\t{:>5.3f}".format(chan_motor.value, chan_motor.voltage))
        print("Pi:    {:>5}\t{:>5.3f}".format(chan_pi.value, chan_pi.voltage))
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exit")
