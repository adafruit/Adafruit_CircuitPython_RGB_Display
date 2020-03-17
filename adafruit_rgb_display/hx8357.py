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
`adafruit_rgb_display.hx8357`
====================================================

A simple driver for the HX8357-based displays.

* Author(s): Melissa LeBlanc-Williams
"""
from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

_SWRESET = const(0x01)
_SLPOUT = const(0x11)
_NORON = const(0x13)
_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_PASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)
_TEON = const(0x35)
_MADCTL = const(0x36)
_COLMOD = const(0x3A)
_TEARLINE = const(0x44)
_SETOSC = const(0xB0)
_SETPWR1 = const(0xB1)
_SETRGB = const(0xB3)
_SETCYC = const(0xB4)
_SETCOM = const(0xB6)
_SETC = const(0xB9)
_SETSTBA = const(0xC0)
_SETPANEL = const(0xCC)
_SETGAMMA = const(0xE0)


class HX8357(DisplaySPI):
    """
    A simple driver for the HX8357-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.hx8357 as hx8357
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = hx8357.HX8357(spi, cs=digitalio.DigitalInOut(board.GPIO0),
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
        (_SETC, b"\xFF\x83\x57"),
        (_SETRGB, b"\x80\x00\x06\x06"),  # 0x80 enables SDO pin (0x00 disables)
        (_SETCOM, b"\x25"),  # -1.52V
        (_SETOSC, b"\x68"),  # Normal mode 70Hz, Idle mode 55 Hz
        (_SETPANEL, b"\x05"),  # BGR, Gate direction swapped
        (_SETPWR1, b"\x00\x15\x1C\x1C\x83\xAA"),  # Not deep standby BT VSPR VSNR AP
        (_SETSTBA, b"\x50\x50\x01\x3C\x1E\x08"),  # OPON normal OPON idle STBA GEN
        (
            _SETCYC,
            b"\x02\x40\x00\x2A\x2A\x0D\x78",
        ),  # NW 0x02 RTN DIV DUM DUM GDON GDOFF
        (
            _SETGAMMA,
            b"\x02\x0A\x11\x1d\x23\x35\x41\x4b\x4b\x42\x3A\x27\x1B\x08\x09\x03\x02"
            b"\x0A\x11\x1d\x23\x35\x41\x4b\x4b\x42\x3A\x27\x1B\x08\x09\x03\x00\x01",
        ),
        (_COLMOD, b"\x55"),  # 16 bit
        (_MADCTL, b"\xc0"),
        (_TEON, b"\x00"),
        (_TEARLINE, b"\x00\x02"),  # TW off
        (_SLPOUT, None),
        (_MADCTL, b"\xa0"),
        (_DISPON, None),
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"

    # pylint: disable-msg=useless-super-delegation, too-many-arguments
    def __init__(
        self,
        spi,
        dc,
        cs,
        rst=None,
        width=480,
        height=320,
        baudrate=16000000,
        polarity=0,
        phase=0,
        rotation=0,
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
            rotation=rotation,
        )
