import board
import busio
import digitalio
import time

CMD_ANGLE = bytearray([0xff, 0xff])
CMD_AGC = bytearray([0x7f, 0xfd])
CMD_MAG = bytearray([0x7f, 0xfe])
CMD_CLAER = bytearray([0x42, 0x01])
CMD_NOP = bytearray([0xc0, 0x00])


class AS5048A:

    def __init__(self, poll_delay=0.0001):
        self.spi = busio.SPI(board.SCK, MISO=board.MISO)
        self.cs = digitalio.DigitalInOut(board.CE0)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=3000000, polarity=0, phase=1)
        self.spi.unlock()

        # data
        self.angle = 0
        self.sampletime = 0
        self.last_angle = 0
        self.last_sampletime = 0
        self.sum_angle = 0
        self.sum_time = 0

        self.on = True
        self.poll_delay = poll_delay

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def spi_write_read(self, cmd):
        result = bytearray(2)
        self.cs.value = False
        self.spi.write_readinto(cmd, result)
        self.cs.value = True
        time.sleep(350 / 1000000000)
        return result

    def get_angle(self):
        while not self.spi.try_lock():
            pass
        try:
            self.spi_write_read(CMD_ANGLE)
            result = self.spi_write_read(CMD_NOP)
            result0 = result[0] & 0x3f
            result1 = result[1] & 0xf0  # ignore the last four value
            self.angle = (result0 << 8) + result1  # 0-0x3fff
            self.sampletime = time.time_ns()
            # clear error flag
            if result[0] & 0x40 > 0:
                print('error flag clear')
                self.spi_write_read(CMD_CLAER)
        finally:
            self.spi.unlock()

    def poll(self):
        self.last_angle = self.angle
        self.last_sampletime = self.sampletime
        self.get_angle()
        if self.angle == 0:
            # did not get value, pass this poll
            self.angle = self.last_angle
            self.sampletime = self.last_sampletime
        else:
            theta_angle = self.last_angle - self.angle
            # go through zero  (0x3fff=16383)
            if theta_angle < -10467:
                theta_angle += 0x3fff
            if theta_angle > 10467:
                theta_angle -= 0x3fff
            self.sum_angle += theta_angle
            theta_time = self.sampletime - self.last_sampletime
            self.sum_time += theta_time

    def run_threaded(self):
        r = self.sum_angle / 0x3fff
        s = self.sum_time / 1000000000
        if s == 0:
            s = 0.01  # impossible, just in case
        self.sum_angle = 0
        self.sum_time = 0
        return r / s

    def run(self):
        # do not expect use threaded=False
        pass

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    itr = 0
    lst = []
    as5048a = AS5048A()
    while itr < 5000:
        itr += 1
        as5048a.poll()
        time.sleep(0.001)
        if itr % 20 == 0:
            speed = as5048a.run_threaded()
            lst.append(speed)
    print(lst)
    # while itr < 500:
    #     as5048a.run()
    #     print(as5048a.angle)
    #     itr += 1
