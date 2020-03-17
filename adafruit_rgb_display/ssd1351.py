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
`adafruit_rgb_display.ssd1351`
====================================================

A simple driver for the SSD1351-based displays.

* Author(s): Radomir Dopieralski, Michael McWethy
"""
from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

_SETCOLUMN = const(0x15)
_SETROW = const(0x75)
_WRITERAM = const(0x5C)
_READRAM = const(0x5D)
_SETREMAP = const(0xA0)
_STARTLINE = const(0xA1)
_DISPLAYOFFSET = const(0xA2)
_DISPLAYALLOFF = const(0xA4)
_DISPLAYALLON = const(0xA5)
_NORMALDISPLAY = const(0xA6)
_INVERTDISPLAY = const(0xA7)
_FUNCTIONSELECT = const(0xAB)
_DISPLAYOFF = const(0xAE)
_DISPLAYON = const(0xAF)
_PRECHARGE = const(0xB1)
_DISPLAYENHANCE = const(0xB2)
_CLOCKDIV = const(0xB3)
_SETVSL = const(0xB4)
_SETGPIO = const(0xB5)
_PRECHARGE2 = const(0xB6)
_SETGRAY = const(0xB8)
_USELUT = const(0xB9)
_PRECHARGELEVEL = const(0xBB)
_VCOMH = const(0xBE)
_CONTRASTABC = const(0xC1)
_CONTRASTMASTER = const(0xC7)
_MUXRATIO = const(0xCA)
_COMMANDLOCK = const(0xFD)
_HORIZSCROLL = const(0x96)
_STOPSCROLL = const(0x9E)
_STARTSCROLL = const(0x9F)


class SSD1351(DisplaySPI):
    """
    A simple driver for the SSD1351-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.ssd1351 as ssd1351
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = ssd1351.SSD1351(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15), rst=digitalio.DigitalInOut(board.GPIO16))
    >>> display.fill(0x7521)
    >>> display.pixel(32, 32, 0)
    """

    _COLUMN_SET = _SETCOLUMN
    _PAGE_SET = _SETROW
    _RAM_WRITE = _WRITERAM
    _RAM_READ = _READRAM
    _INIT = (
        (_COMMANDLOCK, b"\x12"),
        (_COMMANDLOCK, b"\xb1"),
        (_DISPLAYOFF, b""),
        (_DISPLAYENHANCE, b"\xa4\x00\x00"),
        # 7:4 = Oscillator Frequency,
        # 3:0 = CLK Div Ratio (A[3:0]+1 = 1..16)
        (_CLOCKDIV, b"\xf0"),
        (_MUXRATIO, b"\x7f"),  # 127
        (_SETREMAP, b"\x74"),
        (_STARTLINE, b"\x00"),
        (_DISPLAYOFFSET, b"\x00"),
        (_SETGPIO, b"\x00"),
        (_FUNCTIONSELECT, b"\x01"),
        (_PRECHARGE, b"\x32"),
        (_PRECHARGELEVEL, b"\x1f"),
        (_VCOMH, b"\x05"),
        (_NORMALDISPLAY, b""),
        (_CONTRASTABC, b"\xc8\x80\xc8"),
        (_CONTRASTMASTER, b"\x0a"),
        (_SETVSL, b"\xa0\xb5\x55"),
        (_PRECHARGE2, b"\x01"),
        (_DISPLAYON, b""),
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">BB"

    # pylint: disable-msg=useless-super-delegation, too-many-arguments
    def __init__(
        self,
        spi,
        dc,
        cs,
        rst=None,
        width=128,
        height=128,
        baudrate=16000000,
        polarity=0,
        phase=0,
        *,
        x_offset=0,
        y_offset=0,
        rotation=0
    ):
        if baudrate > 16000000:  # Limit to Display Max Baudrate
            baudrate = 16000000
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
