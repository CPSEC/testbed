import board
import busio
import digitalio
import time

CMD_ANGLE = bytearray([0xff,0xff])
CMD_AGC = bytearray([0x7f,0xfd])
CMD_MAG = bytearray([0x7f,0xfe])
CMD_CLAER = bytearray([0x42,0x01])
CMD_NOP = bytearray([0xc0,0x00])


class AS5048A:

    def __init__(self, poll_delay=0.000001):
        self.spi = busio.SPI(board.SCK, MISO=board.MISO)
        self.cs = digitalio.DigitalInOut(board.CE0)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=3000000, polarity=0, phase=1)
        self.spi.unlock()
        tmp = time.time_ns()
        self.readtime = [tmp, tmp, tmp, tmp, tmp]
        self.angle = [0, 1, 2, 3, 4]

        self.on = True
        self.poll_delay = poll_delay

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def pop_append(self, lst, data):
        lst.pop(0)
        lst.append(data)

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
            result = bytearray(2)
            self.spi_write_read(CMD_ANGLE)
            result = self.spi_write_read(CMD_NOP)
            result0 = result[0] & 0x3f
            angle = (result0 << 8) + result[1]  # 0-0x3fff

            self.pop_append(self.readtime, time.time_ns())
            self.pop_append(self.angle, angle)

            ### clear error flag
            if result[0] & 0x40 > 0:
                print('error flag clear')
                self.spi_write_read(CMD_CLAER)

        finally:
            self.spi.unlock()

    def poll(self):
        self.get_angle()

    def filter(self):
        def get_interval(lst):
            interval = []
            for i in range(len(lst)-1):
                interval.append(lst[i+1]-lst[i])
            return interval
        # get intervals
        angle_interval = get_interval(self.angle)
        time_interval = get_interval(self.readtime)
        # get majority
        positive_num = 0
        positive = False
        for x in angle_interval:
            if x > 0:
                positive_num += 1
        if positive_num>2:
            positive = True
        # save majority
        angles = 0
        times = 0
        for i in range(len(angle_interval)):
            if positive:
                if angle_interval[i]<0:
                    continue
            else:
                if angle_interval[i]>0:
                    continue
            angles += angle_interval[i]
            times += time_interval[i]
        return angles, times

    def run_threaded(self):
        angles, times = self.filter()
        r = angles/0x3fff
        s = times/1000000000
        return r/s

    def run(self):
        self.poll()
        angles, times = self.filter()
        r = angles / 0x3fff
        s = times / 1000000000
        return r/s

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    iter = 0
    p = AS5048A()
    while iter < 100:
        output = p.run()
        print(output)
        time.sleep(0.001)
        iter += 1
