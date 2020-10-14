import time
import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class BNO055:
    def __init__(self, p1, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # optional, parameter p1
        i2c = I2C(6)  # Device is /dev/i2c-1
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

        self.heading = self.roll = self.pitch = self.sys = self.gyro = self.accel = self.mag = \
            self.ori_x = self.ori_y = self.ori_z = self.ori_w = self.temp_c = self.mag_x = self.mag_y = \
            self.mag_z = self.gyr_x = self.gyr_y = self.gyr_z = self.acc_x = self.acc_y = self.acc_z = \
            self.lacc_x = self.lacc_y = self.lacc_z = self.gra_x = self.gra_y = self.gra_z = 0

    def run(self):
        self.poll()
        return self.heading, self.roll, self.pitch, self.sys, self.gyro, self.accel, self.mag, \
               self.ori_x, self.ori_y, self.ori_z, self.ori_w, self.temp_c, self.mag_x, self.mag_y, \
               self.mag_z, self.gyr_x, self.gyr_y, self.gyr_z, self.acc_x, self.acc_y, self.acc_z, \
               self.lacc_x, self.lacc_y, self.lacc_z, self.gra_x, self.gra_y, self.gra_z

        # Call in the control loop
        # Works when threaded=False
        # Input is parameters, Return your output

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        # Call once before stop the part

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)
        # your thread
        # Works when threaded=True

    def run_threaded(self, in1, in2):
        return self.tdata1, self.tdata2
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self):
        self.temp_c = self.sensor.temperature
        self.acc_x, self.acc_y, self.acc_z = self.sensor.acceleration
        self.mag_x, self.mag_y, self.mag_z = self.sensor.magnetic
        self.gra_x, self.gra_y, self.gyr_z = self.sensor.gyro
        self.heading, self.roll, self.pitch = self.sensor.euler
        self.ori_x, self.ori_y, self.ori_z, self.ori_w = self.sensor.quaternion
        self.lacc_x, self.lacc_y, self.lacc_z = self.sensor.linear_acceleration
        self.gyr_x, self.gyr_y, self.gyr_z = self.sensor.gravity


# test
if __name__ == "__main__":
    iter = 0
    t = template()
    while iter < 3:
        tdata1, tdata2 = t.run()
        print(tdata1, tdata2)
        iter += 1
        time.sleep(0.5)
