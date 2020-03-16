# The MIT License (MIT)
#
# Copyright (c) 2017 Radomir Dopieralski and Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_rgb_display.hx8353`
====================================================

A simple driver for the HX8353-based displays.

* Author(s): Radomir Dopieralski, Michael McWethy
"""
from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

_SWRESET = const(0x01)
_NORON = const(0x13)
_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_PASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)
_MADCTL = const(0x36)
_COLMOD = const(0x3A)


class HX8353(DisplaySPI):
    """
    A simple driver for the HX8353-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.hx8353 as hx8353
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = hx8353.HX8383(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)
    """

    _COLUMN_SET = _CASET
    _PAGE_SET = _PASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (_SWRESET, None),
        (_DISPON, None),
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"

    # pylint: disable-msg=useless-super-delegation, too-many-arguments
    def __init__(self, spi, dc, cs, rst=None, width=128, height=128, rotation=0):
        super().__init__(spi, dc, cs, rst, width, height, rotation)
