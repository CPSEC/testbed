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

    def __init__(self, poll_delay=0.00000035):
        self.spi = busio.SPI(board.SCK, MISO=board.MISO)
        self.cs = digitalio.DigitalInOut(board.CE0)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True

        self.output = 0
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
            self.spi.configure(baudrate=3000000, polarity=0, phase=1)
            # self.cs.value = False
            result = bytearray(2)
            # self.spi.write_readinto(CMD_ANGLE, result)
            # self.cs.value = True
            # time.sleep(350 / 1000000000)
            self.spi_write_read(CMD_ANGLE)
            result = self.spi_write_read(CMD_NOP)

            # self.cs.value = False
            # self.spi.write_readinto(CMD_NOP, result)
            # self.cs.value = True
            result0 = result[0] & 0x3f
            angle = (result0 << 8) + result[1]  # 0-0x3fff

            ### clear error flag

        finally:
            self.spi.unlock()
        return angle

    def poll(self):
        self.output = self.get_angle()

    def run_threaded(self):
        return self.output

    def run(self):
        self.poll()
        return self.output

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    iter = 0
    p = AS5048A()
    while iter < 100:
        output = p.run()
        print(output)
        time.sleep(0.01)
        iter += 1
