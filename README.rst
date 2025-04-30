Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-rgb_display/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/rgb_display/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/actions/
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

Port of display drivers from https://github.com/adafruit/micropython-adafruit-rgb-display to Adafruit CircuitPython for use on Adafruit's SAMD21-based and other CircuitPython boards.

.. note:: This driver currently won't work on micropython.org firmware, instead you want the micropython-adafruit-rgb-display driver linked above!

This CircuitPython driver currently supports displays that use the following display-driver chips: HX8353, HX8357, ILI9341, S6D02A1, ST7789, SSD1331, SSD1351, and ST7735 (including variants ST7735R and ST7735S).

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

For the Pillow Examples, you will need to be running CPython. This means using a Single Board Computer
such as a Raspberry Pi or using a chip such as an FT232H on Linux, Window, or Mac. CircuitPython does
not support PIL/pillow (python imaging library)!

For improved performance consider installing NumPy.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-rgb-display/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-rgb-display

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-rgb-display

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-rgb-display

Usage Example
=============

2.2", 2.4", 2.8", 3.2" TFT
---------------------------

.. code-block:: python

  import time
  import busio
  import digitalio
  from board import SCK, MOSI, MISO, D2, D3

  from adafruit_rgb_display import color565
  import adafruit_rgb_display.ili9341 as ili9341


  # Configuration for CS and DC pins:
  CS_PIN = D2
  DC_PIN = D3

  # Setup SPI bus using hardware SPI:
  spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

  # Create the ILI9341 display:
  display = ili9341.ILI9341(spi, cs=digitalio.DigitalInOut(CS_PIN),
                            dc=digitalio.DigitalInOut(DC_PIN))

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


1.14" TFT with Raspbery Pi 4
-----------------------------

With 1.14" `wiring <https://learn.adafruit.com/adafruit-1-14-240x135-color-tft-breakout/python-wiring-and-setup>`_, here is the working code:

.. code-block:: python

  import time
  import busio
  import digitalio
  from board import SCK, MOSI, MISO, CE0, D24, D25

  from adafruit_rgb_display import color565
  from adafruit_rgb_display.st7789 import ST7789


  # Configuration for CS and DC pins:
  CS_PIN = CE0
  DC_PIN = D25
  RESET_PIN = D24
  BAUDRATE = 24000000

  # Setup SPI bus using hardware SPI:
  spi = busio.SPI(clock=SCK, MOSI=MOSI, MISO=MISO)

  # Create the ST7789 display:
  display = ST7789(
      spi,
      rotation=90,
      width=135,
      height=240,
      x_offset=53,
      y_offset=40,
      baudrate=BAUDRATE,
      cs=digitalio.DigitalInOut(CS_PIN),
      dc=digitalio.DigitalInOut(DC_PIN),
      rst=digitalio.DigitalInOut(RESET_PIN))

  # Main loop: same as above
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


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/rgb_display/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
