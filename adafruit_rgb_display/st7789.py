# The MIT License (MIT)
#
# Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries
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
`adafruit_rgb_display.st7789`
====================================================

A simple driver for the ST7789-based displays.

* Author(s): Melissa LeBlanc-Williams
"""

try:
    import struct
except ImportError:
    import ustruct as struct
from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)

_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)

_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)

_PTLAR = const(0x30)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)

_FRMCTR1 = const(0xB1)
_FRMCTR2 = const(0xB2)
_FRMCTR3 = const(0xB3)
_INVCTR = const(0xB4)
_DISSET5 = const(0xB6)

_PWCTR1 = const(0xC0)
_PWCTR2 = const(0xC1)
_PWCTR3 = const(0xC2)
_PWCTR4 = const(0xC3)
_PWCTR5 = const(0xC4)
_VMCTR1 = const(0xC5)

_RDID1 = const(0xDA)
_RDID2 = const(0xDB)
_RDID3 = const(0xDC)
_RDID4 = const(0xDD)

_PWCTR6 = const(0xFC)

_GMCTRP1 = const(0xE0)
_GMCTRN1 = const(0xE1)


class ST7789(DisplaySPI):
    """
    A simple driver for the ST7789-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.st7789 as st7789
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = st7789.ST7789(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15), rst=digitalio.DigitalInOut(board.GPIO16))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)
    """

    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (_SWRESET, None),
        (_SLPOUT, None),
        (_COLMOD, b"\x55"),  # 16bit color
        (_MADCTL, b"\x08"),
    )

    # pylint: disable-msg=useless-super-delegation, too-many-arguments
    def __init__(
        self,
        spi,
        dc,
        cs,
        rst=None,
        width=240,
        height=320,
        baudrate=16000000,
        polarity=0,
        phase=0,
        *,
        x_offset=0,
        y_offset=0,
        rotation=0
    ):
        super().__init__(
            spi,
            dc,
            cs,
            rst,
            width,
            height,
            baudrate=baudrate,
            polarity=polarity,
            phase=phase,
            x_offset=x_offset,
            y_offset=y_offset,
            rotation=rotation,
        )

    def init(self):

        super().init()
        cols = struct.pack(">HH", self._X_START, self.width + self._X_START)
        rows = struct.pack(">HH", self._Y_START, self.height + self._Y_START)
        for command, data in (
            (_CASET, cols),
            (_RASET, rows),
            (_INVON, None),
            (_NORON, None),
            (_DISPON, None),
            (_MADCTL, b"\xc0"),  # Set rotation to 0 and use RGB
        ):
            self.write(command, data)
