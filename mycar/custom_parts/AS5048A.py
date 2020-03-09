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

    def __init__(self, poll_delay=0.0001):
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

    def poll(self):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=10000000, polarity=0, phase=1)
            self.cs.value = False
            result = bytearray(2)
            self.spi.write_readinto(CMD_ANGLE, result)
            self.cs.value = True
            time.sleep(350 / 1000000000)
            self.cs.value = False
            self.spi.write_readinto(CMD_NOP, result)
            self.cs.value = True
            result[0] = result[0] & 0x3f
            self.output = (result[0] << 8) + result[1]  # 0-0x3fff
        finally:
            self.spi.unlock()

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
