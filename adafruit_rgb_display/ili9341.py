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
`adafruit_rgb_display.ili9341`
====================================================

A simple driver for the ILI9341/ILI9340-based displays.

* Author(s): Radomir Dopieralski, Michael McWethy
"""

try:
    import struct
except ImportError:
    import ustruct as struct

from adafruit_rgb_display.rgb import DisplaySPI

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"


class ILI9341(DisplaySPI):
    """
    A simple driver for the ILI9341/ILI9340-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.ili9341 as ili9341
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = ili9341.ILI9341(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15))
    >>> display.fill(color565(0xff, 0x11, 0x22))
    >>> display.pixel(120, 160, 0)
    """

    _COLUMN_SET = 0x2A
    _PAGE_SET = 0x2B
    _RAM_WRITE = 0x2C
    _RAM_READ = 0x2E
    _INIT = (
        (0xEF, b"\x03\x80\x02"),
        (0xCF, b"\x00\xc1\x30"),
        (0xED, b"\x64\x03\x12\x81"),
        (0xE8, b"\x85\x00\x78"),
        (0xCB, b"\x39\x2c\x00\x34\x02"),
        (0xF7, b"\x20"),
        (0xEA, b"\x00\x00"),
        (0xC0, b"\x23"),  # Power Control 1, VRH[5:0]
        (0xC1, b"\x10"),  # Power Control 2, SAP[2:0], BT[3:0]
        (0xC5, b"\x3e\x28"),  # VCM Control 1
        (0xC7, b"\x86"),  # VCM Control 2
        (0x36, b"\x48"),  # Memory Access Control
        (0x3A, b"\x55"),  # Pixel Format
        (0xB1, b"\x00\x18"),  # FRMCTR1
        (0xB6, b"\x08\x82\x27"),  # Display Function Control
        (0xF2, b"\x00"),  # 3Gamma Function Disable
        (0x26, b"\x01"),  # Gamma Curve Selected
        (
            0xE0,  # Set Gamma
            b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00",
        ),
        (
            0xE1,  # Set Gamma
            b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f",
        ),
        (0x11, None),
        (0x29, None),
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    # pylint: disable-msg=too-many-arguments
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
        rotation=0,
    ):
        super().__init__(
            spi,
            dc,
            cs,
            rst=rst,
            width=width,
            height=height,
            baudrate=baudrate,
            polarity=polarity,
            phase=phase,
            rotation=rotation,
        )
        self._scroll = 0

    # pylint: enable-msg=too-many-arguments

    def scroll(self, dy=None):  # pylint: disable-msg=invalid-name
        """Scroll the display by delta y"""
        if dy is None:
            return self._scroll
        self._scroll = (self._scroll + dy) % self.height
        self.write(0x37, struct.pack(">H", self._scroll))
        return None
