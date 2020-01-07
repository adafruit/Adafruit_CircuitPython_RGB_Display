"""
Example to extract the frames and other parameters from an animated gif
and then run the animation on the display.

Usage:
python3 rgb_display_pillow_animated_gif.py

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""
import os
import time
import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789        # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357        # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735        # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351      # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331      # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

def init_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input()
    button.pull = digitalio.Pull.UP
    return button

# pylint: disable=too-few-public-methods
class Frame:
    def __init__(self, duration=0):
        self.duration = duration
        self.image = None
# pylint: enable=too-few-public-methods

class AnimatedGif:
    def __init__(self, display, width=None, height=None, folder=None):
        self._frame_count = 0
        self._loop = 0
        self._index = 0
        self._duration = 0
        self._gif_files = []
        self._frames = []

        if width is not None:
            self._width = width
        else:
            self._width = disp.width
        if height is not None:
            self._height = height
        else:
            self._height = disp.height
        self.display = display
        self.advance_button = init_button(board.D17)
        self.back_button = init_button(board.D22)
        if folder is not None:
            self.load_files(folder)
            self.run()

    def advance(self, loop=False):
        if self._index < len(self._gif_files) - 1:
            self._index += 1
        elif loop and self._index == len(self._gif_files) - 1:
            self._index = 0

    def back(self, loop=False):
        if self._index > 0:
            self._index -= 1
        elif loop and self._index == 0:
            self._index = len(self._gif_files) - 1

    def load_files(self, folder):
        self._gif_files = [f for f in os.listdir(folder) if f[-4:] == '.gif']
        print("Found", self._gif_files)
        if not self._gif_files:
            print("No Gif files found in current folder")
            exit()

    def preload(self):
        image = Image.open(self._gif_files[self._index])
        print("Loading {}...".format(self._gif_files[self._index]))
        if "duration" in image.info:
            self._duration = image.info['duration']
        else:
            self._duration = 0
        if "loop" in image.info:
            self._loop = image.info['loop']
        else:
            self._loop = 1
        self._frame_count = image.n_frames
        screen_ratio = self._width / self._height
        image_ratio = image.width / image.height
        if screen_ratio > image_ratio:
            scaled_width = image.width * self._height // image.height
            scaled_height = self._height
        else:
            scaled_width = self._width
            scaled_height = image.height * self._width // image.width

        self._frames.clear()
        for frame in range(self._frame_count):
            image.seek(frame)
            # Create blank image for drawing.
            # Make sure to create image with mode 'RGB' for full color.
            frame_object = Frame(duration=self._duration)
            if "duration" in image.info:
                frame_object.duration = image.info['duration']
            frame_object.image = Image.new('RGB', (self._width, self._height))

            # Get drawing object to draw on image.
            draw = ImageDraw.Draw(frame_object.image)
            draw.rectangle((0, 0, self._width, self._height), outline=0, fill=(0, 0, 0))

            frame_image = image.copy()
            frame_image = frame_image.resize((scaled_width, scaled_height), Image.BICUBIC)
            x = scaled_width // 2 - self._width // 2
            y = scaled_height // 2 - self._height // 2
            frame_image = frame_image.crop((x, y, x + self._width, y + self._height))
            frame_object.image.paste(frame_image)
            self._frames.append(frame_object)

    def play(self):
        self.preload()

        # Check if we have loaded any files first
        if not self._gif_files:
            print("There are no Gif Images to Play")

        for frame_object in self._frames:
            self.display.image(frame_object.image)
            if not self.advance_button.value:
                self.advance()
            elif not self.back_button.value:
                self.back()
            time.sleep(frame_object.duration / 1000)

        if self._loop == 1:
            return
        if self._loop > 0:
            self._loop -= 1

    def run(self):
        while True:
            self.play()
            self.advance(True)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
#disp = st7789.ST7789(spi, rotation=90                             # 2.0" ST7789
#disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=90    # 1.3", 1.54" ST7789
#disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
#disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
#disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
#disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
#disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
#disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
#disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
#disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = ili9341.ILI9341(spi, rotation=90,                           # 2.2", 2.4", 2.8", 3.2" ILI9341
                       cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
# pylint: enable=line-too-long

if disp.rotation % 180 == 90:
    disp_height = disp.width   # we swap height/width to rotate it to landscape!
    disp_width = disp.height
else:
    disp_width = disp.width   # we swap height/width to rotate it to landscape!
    disp_height = disp.height

gif_player = AnimatedGif(disp, width=disp_width, height=disp_height, folder=".")
