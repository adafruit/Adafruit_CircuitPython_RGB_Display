# SPDX-FileCopyrightText: 2025 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_rgb_display.gc9a01a`
====================================================
A simple driver for the GC9A01A-based displays.

* Author(s): Liz Clark

Implementation Notes
--------------------
Adapted from the CircuitPython GC9A01A driver for use with the RGB Display library.
"""
import struct
import busio
import digitalio
from micropython import const
from adafruit_rgb_display.rgb import DisplaySPI

try:
    from typing import Optional
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

# Command constants
_NOP = const(0x00)
_SWRESET = const(0x01)
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
_MADCTL = const(0x36)
_COLMOD = const(0x3A)
_TEON = const(0x35)

# Extended command constants
_PWCTR1 = const(0xC3)
_PWCTR2 = const(0xC4)
_PWCTR3 = const(0xC9)
_GMCTRP1 = const(0xF0)
_GMCTRN1 = const(0xF1)
_GMCTRP2 = const(0xF2)
_GMCTRN2 = const(0xF3)

class GC9A01A(DisplaySPI):
    """
    A simple driver for the GC9A01A-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.gc9a01a as gc9a01a
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = gc9a01a.GC9A01A(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15), rst=digitalio.DigitalInOut(board.GPIO16))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)
    """
    # pylint: disable=too-few-public-methods

    COLUMN_SET = _CASET
    PAGE_SET = _RASET
    RAM_WRITE = _RAMWR
    RAM_READ = _RAMRD

    _INIT = (
        (_SWRESET, None),
        (0xFE, None),  # Inter Register Enable1
        (0xEF, None),  # Inter Register Enable2
        (0xB6, b"\x00\x00"),  # Display Function Control
        (_MADCTL, b"\x48"),  # Memory Access Control
        (_COLMOD, b"\x05"),  # Interface Pixel Format (16 bits/pixel)
        (_PWCTR1, b"\x13"),  # Power Control 2
        (_PWCTR2, b"\x13"),  # Power Control 3
        (_PWCTR3, b"\x22"),  # Power Control 4
        (_GMCTRP1, b"\x45\x09\x08\x08\x26\x2a"),  # Set Gamma 1
        (_GMCTRN1, b"\x43\x70\x72\x36\x37\x6f"),  # Set Gamma 2
        (_GMCTRP2, b"\x45\x09\x08\x08\x26\x2a"),  # Set Gamma 3
        (_GMCTRN2, b"\x43\x70\x72\x36\x37\x6f"),  # Set Gamma 4
        (0x66, b"\x3c\x00\xcd\x67\x45\x45\x10\x00\x00\x00"),
        (0x67, b"\x00\x3c\x00\x00\x00\x01\x54\x10\x32\x98"),
        (0x74, b"\x10\x85\x80\x00\x00\x4e\x00"),
        (0x98, b"\x3e\x07"),
        (_TEON, None),  # Tearing Effect Line ON
        (_INVON, None),  # Display Inversion ON
        (_SLPOUT, None),  # Exit Sleep Mode
        (_NORON, None),  # Normal Display Mode ON
        (_DISPON, None),  # Display ON
    )

    def __init__(
        self,
        spi: busio.SPI,
        dc: digitalio.DigitalInOut,
        cs: digitalio.DigitalInOut,
        rst: Optional[digitalio.DigitalInOut] = None,
        width: int = 240,
        height: int = 240,
        baudrate: int = 16000000,
        polarity: int = 0,
        phase: int = 0,
        *,
        x_offset: int = 0,
        y_offset: int = 0,
        rotation: int = 0
    ) -> None:
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

    def init(self) -> None:
        super().init()
        cols = struct.pack(">HH", 0, self.width - 1)
        rows = struct.pack(">HH", 0, self.height - 1)
        
        for command, data in (
            (_CASET, cols),
            (_RASET, rows),
            (_MADCTL, b"\xc0"),  # Set rotation to 0 and use RGB
        ):
            self.write(command, data)
