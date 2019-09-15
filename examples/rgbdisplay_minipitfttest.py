import time
import random
import digitalio
import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins for Raspberry Pi
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000   # The pi can be very fast!
# Create the ST7789 display:
display = st7789.ST7789(board.SPI(), cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                        width=135, height=240, x_offset=53, y_offset=40)

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Main loop:
while True:
    if not buttonA.value: # button A pressed
        display.fill(color565(255, 0, 0))  # red
    elif not buttonB.value: # button B pressed
        display.fill(color565(0, 0, 255))  # blue
    else:
        display.fill(color565(0, 255, 0))    # green

