import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115:

    def __init__(self, coeff_m=1, coeff_p=1,coeff_r=1, poll_delay=2.5):
        # create I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # create ADC object
        ads = ADS.ADS1015(i2c)

        POWER_CHANNEL_MOTOR = ADS.P0  # A0 on board
        POWER_CHANNEL_PI = ADS.P1  # A1 on board
        POWER_CHANNEL_RG = ADS.P2 #A2 on board

        self.chan_motor = AnalogIn(ads, POWER_CHANNEL_MOTOR)
        self.chan_pi = AnalogIn(ads, POWER_CHANNEL_PI)
        self.chan_rg = AnalogIn(ads, POWER_CHANNEL_RG)
        self.poll_delay = poll_delay
        self.coeff_m = coeff_m
        self.coeff_p = coeff_p
        self.coeff_r = coeff_r
        self.on = True
        self.vm = 0
        self.vp = 0
        self.vr = 0
    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def poll(self):
        self.vm = self.chan_motor.value * self.coeff_m
        self.vp = self.chan_pi.value * self.coeff_p
        self.vr = self.chan_rg.value * self.coeff_r
    def run_threaded(self):
        return self.vm, self.vp, self.vr

    def run(self):
        self.poll()
        return self.vm, self.vp, self.vr

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    iter = 0
    p = ADS1115()
    while True:
        print("{:>5}\t{:>5.3f}".format(p.chan_motor.value,p.chan_motor.voltage))
        time.sleep(0.5)
        print("{:>5}\t{:>5.3f}".format(p.chan_pi.value,p.chan_pi.voltage))
        time.sleep(0.5)
        print("{:>5}\t{:>5.3f}".format(p.chan_rg.value,p.chan_rg.voltage))
        time.sleep(0.5)
