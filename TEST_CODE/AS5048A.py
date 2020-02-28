import board
import busio
import digitalio
import time

spi = busio.SPI(board.SCK,  MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CE0)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

CMD_ANGLE = bytearray([0xff,0xff])
CMD_AGC = bytearray([0x7f,0xfd])
CMD_MAG = bytearray([0x7f,0xfe])
CMD_CLAER = bytearray([0x42,0x01])
CMD_NOP = bytearray([0xc0,0x00])

while not spi.try_lock():
    pass
try:
    try:
        while(True):
            spi.configure(baudrate=10000000, polarity=0, phase=1)
            cs.value = False
            result = bytearray(2)
            spi.write_readinto(CMD_ANGLE, result)
            cs.value = True
            time.sleep(350/1000000000)
            cs.value = False
            spi.write_readinto(CMD_NOP, result)
            cs.value = True
            result[0] = result[0]&0x3f
            output = (result[0]<<8)+result[1]
            angle = output / 0x3fff * 360
            print('output={:0>14b}'.format(output))
            print('angle={:.3f}'.format(angle))
            time.sleep(0.5)
    finally:
        spi.unlock()
finally:
    pass
