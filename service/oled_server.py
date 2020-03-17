from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
import pickle
import sys
import traceback


class OLED:
    def __init__(self):
        # Create the I2C interface.
        i2c = busio.I2C(SCL, SDA)

        # Create the SSD1306 OLED class.
        # The first two parameters are the pixel width and pixel height.  Change these
        # to the right size for your display!
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        # Clear display.
        self.disp.fill(0)
        self.disp.show()

        # Set font
        self.font = {'text': ImageFont.load_default(),
                     'icon': ImageFont.truetype('/home/pi/testbed/service/fa-solid-900.ttf', 16, encoding='unic')}

        # Content
        self.content = {'icons': {'pi_bat': 0, 'car_bat': 0, 'relay': 0, 'power': 0},
                        'text': []}

        # Icons
        self.icons = {'pi_bat': {0: chr(0xf244), 1: chr(0xf243), 2: chr(0xf242), 3: chr(0xf241), 4: chr(0xf240)},
                      'car_bat': {0: chr(0xf1e6), 1: chr(0xf5df)},
                      'relay': {0: chr(0xf023), 1: chr(0xf09c)},
                      'power': {0: chr(0xf058), 1: chr(0xf011), 2: chr(0xf2f9)}}

    def display(self):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = self.disp.width
        height = self.disp.height
        image = Image.new('1', (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw Icons
        draw.text((108, 0), self.icons['pi_bat'][self.content['icons']['pi_bat']], font=self.font['icon'], fill=255)
        draw.text((88, 0), self.icons['car_bat'][self.content['icons']['car_bat']], font=self.font['icon'], fill=255)
        draw.text((68, 0), self.icons['relay'][self.content['icons']['relay']], font=self.font['icon'], fill=255)
        draw.text((0, 0), self.icons['power'][self.content['icons']['power']], font=self.font['icon'], fill=255)

        # Draw Texts
        offset = 0
        for text in self.content['text']:
            x = 1
            y = 39 + offset
            draw.text((x, y), text, font=self.font['text'], fill=255)
            offset += 8

        # Display image.
        self.disp.image(image)
        self.disp.show()

    def icon_update(self, status):
        for s in status:
            if s in self.content['icons']:
                self.content['icons'][s] = status[s]

    def text_append(self, texts):
        for text in texts:
            if len(text) > 21:
                text = text[:21]
            if len(self.content['text']) == 3:
                self.content['text'].pop(0)
            self.content['text'].append(text)


if __name__ == '__main__':
    oled = OLED()

    from multiprocessing.connection import Listener

    address = ('localhost', 13202)
    listener = Listener(address, authkey=bytes('7jogUVtgh5v@h^', 'ascii'))

    while True:
        try:
            conn = listener.accept()
            data_str = conn.recv()
            data = pickle.loads(data_str)
            # print(data)
            if 'icons' in data:
                # icons = {'power': 2, 'car_bat':1}
                oled.icon_update(data['icons'])
            if 'texts' in data and bool(data['texts']):
                # texts = ['1234567890123456789012345','Hello','     World!']
                oled.text_append(data['texts'])
            oled.display()
            conn.close()
        except Exception as e:
            listener.close()
            traceback.print_exc()
            sys.exit(0)


