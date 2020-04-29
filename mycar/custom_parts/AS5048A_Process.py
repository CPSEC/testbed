import time
import multiprocessing
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
    def __init__(self):
        self.spi = busio.SPI(board.SCK, MISO=board.MISO)
        self.cs = digitalio.DigitalInOut(board.CE0)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=3000000, polarity=0, phase=1)
        self.spi.unlock()
        self.angle = 0
        self.sampletime = time.time_ns()

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


def feed_position(b1p, b1t, b2p, b2t, b1n, b2n, cbn):
    bp = b1p
    bt = b1t
    bn = b1n
    as5048a = AS5048A()
    idx = 0
    lb = -1
    while True:
        time.sleep(0.001)

        if cbn.value != lb:
            # switch buffer
            idx = 0
            if cbn.value == 1:
                bp = b1p
                bt = b1t
                bn = b1n
            else:
                bp = b2p
                bt = b2t
                bn = b2n
        lb = cbn.value

        # avoid overflow
        if idx > 49:
            continue

        as5048a.get_angle()
        bp[idx] = as5048a.angle
        bt[idx] = as5048a.sampletime
        print('current_buff=', cbn.value, '  idx=', bn.value, ' angle=', bp[idx])
        idx += 1
        bn.value = idx


class speed:

    def __init__(self, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay

        # create shared memory
        self.buff1_position = multiprocessing.Array('i', 50)
        self.buff1_time = multiprocessing.Array('i', 50)
        self.buff1_num = multiprocessing.Value('i')
        self.buff2_position = multiprocessing.Array('i', 50)
        self.buff2_time = multiprocessing.Array('i', 50)
        self.buff2_num = multiprocessing.Value('i')
        self.current_buff = multiprocessing.Value('i')
        self.current_buff.value = 1

        # create process
        p = multiprocessing.Process(target=feed_position, args=(self.buff1_position, self.buff1_time,
                                                                self.buff2_position, self.buff2_time,
                                                                self.buff1_num, self.buff2_num, self.current_buff))
        p.start()

    def run(self):
        # inform the subprocess change buffer
        last_buff = self.current_buff.value
        if last_buff == 1:
            self.current_buff.value = 2
            bp = self.buff1_position
            bt = self.buff1_time
            bn = self.buff1_num.value
        else:
            self.current_buff.value = 1
            bp = self.buff2_position
            bt = self.buff2_time
            bn = self.buff2_num.value

        print(bp[:bn])
        return 0
        theta_p = [bp[idx] - bp[idx + 1] for idx in range(bn - 1)]

        def filter(theta_angle):
            if theta_angle < -10467:
                theta_angle += 0x3fff
            if theta_angle > 10467:
                theta_angle -= 0x3fff

        theta_p = [filter(p) for p in theta_p]
        print('num=', bn, '  theta_p=', theta_p)

        theta_t = [bt[idx + 1] - bt[idx] for idx in range(bn - 1)]
        result = (sum(theta_p) / 0x3fff) / ((sum(theta_t)+1) / 1000000000)

        return result

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        # Call once before stop the part

    def update(self):
        pass

    def run_threaded(self, in1, in2):
        pass

    def poll(self):
        pass
        # your actual function of the thread


# test
if __name__ == "__main__":
    iter = 0
    t = speed()
    time.sleep(1)
    while iter < 10:
        time.sleep(0.01)
        data = t.run()
        print('data=', data)
        iter += 1
