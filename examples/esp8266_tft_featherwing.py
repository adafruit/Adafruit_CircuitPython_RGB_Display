# Quick test of TFT FeatherWing (ILI9341) with ESP8266 Adafruit MicroPython.
# Will fill the TFT black and put a red pixel in the center, wait 2 seconds,
# then fill the screen blue (with no pixel), wait 2 seconds, and repeat.
import time

import busio
import digitalio
from board import SCK, MOSI, MISO, GPIO0, GPIO15

from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341


# Configuratoin for CS and DC pins (these are FeatherWing defaults on ESP8266):
CS_PIN = GPIO0
DC_PIN = GPIO15
# Config for display baudrate (default is 32mhz, about as fast as the ESP supports):
BAUDRATE = 32000000


# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

# Create the ILI9341 display:
display = ili9341.ILI9341(spi, cs=digitalio.DigitalInOut(CS_PIN),
                          dc=digitalio.DigitalInOut(DC_PIN), baudrate=BAUDRATE)

# Main loop:
while True:
    # Clear the display
    display.fill(0)
    # Draw a red pixel in the center.
    display.pixel(120, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)
    # Clear the screen blue.
    display.fill(color565(0, 0, 255))
    # Pause 2 seconds.
    time.sleep(2)
