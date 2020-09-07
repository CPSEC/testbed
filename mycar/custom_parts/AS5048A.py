# requirements:
# spi-dev
import spidev

CMD_READ = 0x4000
CMD_ANGLE = 0x3FFF
CMD_READ_MAG = 0x3FFE
CMD_READ_DIAG = 0x3FFD
CMD_NOP = 0x0000
CMD_CLEAR_ERROR = 0x0001
CMD_ProgramControl = 0x0003
CMD_OTPHigh = 0x0016
CMD_OTPLow = 0x0017


class AS5048A:
    """
    class for sensor AS5048A (SPI protocol)
    default /dev/spidev0.0
      signal      physical pin
     SPI0_MOSI         19
     SPI0_MISO         21
     SPI0_SCLK         23
     SPI0_CE0          24

    :param bus: spi bus number
    :param device: spi chip-select pin to use
    :param speed: spi bus speed in Hz - Max 10MHz
    """

    def __init__(self, bus=0, device=0, speed=7800000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)  # default /dev/spidev0.0
        self.spi.max_speed_hz = speed  # Max 10MHz
        self.spi.mode = 1  # polarity=0, phase=1

    @staticmethod
    def calc_parity(v):
        """
        Args:
            v: data - int 16bit
        Returns: 1 (odd) or 0 (even)
        """
        if v == 0:
            return 0
        v ^= v >> 8
        v ^= v >> 4
        v ^= v >> 2
        v ^= v >> 1
        return v & 1

    def read_reg(self, cmd, debug=True):
        """
        Args:
            cmd: AS5048A command
        Returns: data or -1 (error)
        """
        if debug:
            print("cmd:", hex(cmd))
        command = CMD_READ | cmd
        command |= (self.calc_parity(command) << 15)
        cmd_lst = [(command >> 8) & 0xff, command & 0xff]
        self.spi.xfer(cmd_lst)
        if debug:
            print('sent:', [hex(value) for value in cmd_lst])

        command = CMD_READ | CMD_NOP
        command |= (self.calc_parity(command) << 15)
        cmd_lst = [(command >> 8) & 0xff, command & 0xff]
        res = self.spi.xfer(cmd_lst)
        if debug:
            print('sent:', [hex(value) for value in cmd_lst])
            print('received:', [hex(value) for value in res])

        error_flag = 1
        data = 0
        if res[0] & (1 << 6):
            data = (res[0] & 0x3f) << 8 + res[1]
            error_flag = self.calc_parity(data) ^ (res[0] >> 7)
            if error_flag & debug:
                print("AS5048A: Parity bit check failed.")
        else:  # error
            if debug:
                print("AS5048A: There exists a transmission error in a previous host transmission.")
            command = CMD_READ | CMD_CLEAR_ERROR
            command |= (self.calc_parity(command) << 15)
            cmd_lst = [(command >> 8) & 0xff, command & 0xff]
            self.spi.xfer(cmd_lst)
            if debug:
                print('sent', [hex(value) for value in cmd_lst])

        if error_flag:
            return -1
        return data

    def get_angle(self, debug=True):
        return self.read_reg(CMD_ANGLE, debug=debug)

    def close(self):
        self.spi.close()


if __name__ == "__main__":
    as5048a = AS5048A()
    for i in range(10):
        print(hex(as5048a.get_angle()))



