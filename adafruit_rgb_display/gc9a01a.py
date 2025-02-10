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

# Constants for MADCTL
_MADCTL_MY = const(0x80)  # Bottom to top
_MADCTL_MX = const(0x40)  # Right to left
_MADCTL_MV = const(0x20)  # Reverse Mode
_MADCTL_ML = const(0x10)  # LCD refresh Bottom to top
_MADCTL_RGB = const(0x00) # Red-Green-Blue pixel order
_MADCTL_BGR = const(0x08) # Blue-Green-Red pixel order
_MADCTL_MH = const(0x04)  # LCD refresh right to left
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
        (0xFE, b"\x00"),  # Inter Register Enable1
        (0xEF, b"\x00"),  # Inter Register Enable2
        (0xB6, b"\x00\x00"),  # Display Function Control [S1→S360 source, G1→G32 gate]
        (_MADCTL, b"\x48"),  # Memory Access Control [Invert Row order, invert vertical scan order]
        (_COLMOD, b"\x05"),  # COLMOD: Pixel Format Set [16 bits/pixel]
        (_PWCTR1, b"\x13"),  # Power Control 2 [VREG1A = 5.06, VREG1B = 0.68]
        (_PWCTR2, b"\x13"),  # Power Control 3 [VREG2A = -3.7, VREG2B = 0.68]
        (_PWCTR3, b"\x22"),  # Power Control 4
        (_GMCTRP1, b"\x45\x09\x08\x08\x26\x2a"),  # SET_GAMMA1
        (_GMCTRN1, b"\x43\x70\x72\x36\x37\x6f"),  # SET_GAMMA2
        (_GMCTRP2, b"\x45\x09\x08\x08\x26\x2a"),  # SET_GAMMA3
        (_GMCTRN2, b"\x43\x70\x72\x36\x37\x6f"),  # SET_GAMMA4
        (0x66, b"\x3c\x00\xcd\x67\x45\x45\x10\x00\x00\x00"),
        (0x67, b"\x00\x3c\x00\x00\x00\x01\x54\x10\x32\x98"),
        (0x74, b"\x10\x85\x80\x00\x00\x4e\x00"),
        (0x98, b"\x3e\x07"),
        (_TEON, b"\x00"),  # Tearing Effect Line ON [both V-blanking and H-blanking]
        (_INVON, b"\x00"),  # Display Inversion ON
        (_SLPOUT, None),  # Sleep Out Mode (with 120ms delay)
        (_DISPON, None),  # Display ON (with 20ms delay)
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
        # Account for offsets in the column and row addressing
        cols = struct.pack(">HH", self._X_START, self.width + self._X_START - 1)
        rows = struct.pack(">HH", self._Y_START, self.height + self._Y_START - 1)
        
    def init(self) -> None:
        """Initialize the display"""
        super().init()
        
        # Initialize display
        self.write(_SWRESET)
        time.sleep(0.150)  # 150ms delay after reset
        
        # Set addressing mode and color format
        self.write(_MADCTL, bytes([_MADCTL_MX | _MADCTL_BGR]))
        
        # Set addressing windows
        self.write(_CASET, b"\x00\x00\x00\xef")  # Column Address Set [0-239]
        self.write(_RASET, b"\x00\x00\x00\xef")  # Row Address Set [0-239]
        
        time.sleep(0.150)  # 150ms delay before turning on display