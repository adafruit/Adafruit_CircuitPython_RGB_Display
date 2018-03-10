Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-rgb_display/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/Adafruit_CircuitPython_RGB_Display.svg?branch=master
    :target: https://travis-ci.org/adafruit/Adafruit_CircuitPython_RGB_Display
    :alt: Build Status

Port of display drivers from https://github.com/adafruit/micropython-adafruit-rgb-display to Adafruit CircuitPython for use on Adafruit's SAMD21-based and other CircuitPython boards.

.. note:: This driver currently won't work on micropython.org firmware, instead you want the micropython-adafruit-rgb-display driver linked above!

This CircuitPython driver currently supports displays that use the following display-driver chips: HX8353, ILI9341, S6D02A1, SSD1331, SSD1351, and ST7735.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. code-block:: python

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

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-rgb_display --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.