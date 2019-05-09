from time import sleep
from typing import List

import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

from bmp180_reader import BmpSensorProxy


class DisplayProxy(object):
    def __init__(self):
        # Raspberry Pi pin configuration:
        self.RST = 24

        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)

        # Initialize library.
        self.disp.begin()

    def clear_disp(self):
        # Clear display.
        self.disp.clear()
        self.disp.display()

    def display_any_image(self, image_path):
        self.clear_disp()
        image = Image.open(image_path).resize((self.disp.width, self.disp.height), Image.ANTIALIAS).convert('1')

        # Display image.
        self.disp.image(image)
        self.disp.display()

    def display_text_lines(self, lines: List[str]):
        # self.clear_disp()
        padding = 2
        top = padding
        x = padding
        image = Image.new('1', (self.disp.width, self.disp.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Load default font
        font = ImageFont.load_default()

        for n, line in enumerate(lines):
            draw.text((x, top + (n * 16)), line, font=font, fill=255)

        try:
            self.disp.image(image)
            self.disp.display()
        except OSError:
            sleep(5)
            self.disp.reset()
            self.disp.image(image)
            self.disp.display()


if __name__ == "__main__":
    display_proxy = DisplayProxy()
    display_proxy.display_any_image('db.jpg')
    sleep(1000)
    display_proxy.display_text_lines(['asdf'])
    sleep(2)
    display_proxy.clear_disp()
    bmp_sensor = BmpSensorProxy()
    while True:
        display_proxy.display_text_lines(bmp_sensor.read_all())
        sleep(1)

