""" Base class for all RGB Display devices """
import time
from micropython import const
try:
    import struct
except ImportError:
    import ustruct as struct

import adafruit_bus_device.spi_device as spi_device

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

# This is the size of the buffer to be used for fill operations, in 16-bit
# units. We use 256, which is 512 bytes — size of the DMA buffer on SAMD21.
_BUFFER_SIZE = const(256)


def color565(r, g, b):
    """Format color code for device"""
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


class DummyPin:
    """A fake gpio pin for when you want to skip pins."""
    def init(self, *args, **kwargs):
        """Dummy Pin init"""
        pass

    def low(self):
        """Dummy low Pin method"""
        pass

    def high(self):
        """Dummy high Pin method"""
        pass


class Display: #pylint: disable-msg=no-member
    """Base class for all RGB display devices"""
    _PAGE_SET = None
    _COLUMN_SET = None
    _RAM_WRITE = None
    _RAM_READ = None
    _INIT = ()
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init()

    def init(self):
        """Run the initialization commands."""
        for command, data in self._INIT:
            self.write(command, data)

    #pylint: disable-msg=invalid-name,too-many-arguments
    def _block(self, x0, y0, x1, y1, data=None):
        """Read or write a block of data."""
        self.write(self._COLUMN_SET, self._encode_pos(x0, x1))
        self.write(self._PAGE_SET, self._encode_pos(y0, y1))
        if data is None:
            size = struct.calcsize(self._DECODE_PIXEL)
            return self.read(self._RAM_READ,
                             (x1 - x0 + 1) * (y1 - y0 + 1) * size)
        self.write(self._RAM_WRITE, data)
        return None
    #pylint: enable-msg=invalid-name,too-many-arguments

    def _encode_pos(self, x, y):
        """Encode a postion into bytes."""
        return struct.pack(self._ENCODE_POS, x, y)

    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return struct.pack(self._ENCODE_PIXEL, color)

    def _decode_pixel(self, data):
        """Decode bytes into a pixel color."""
        return color565(*struct.unpack(self._DECODE_PIXEL, data))

    def pixel(self, x, y, color=None):
        """Read or write a pixel."""
        if color is None:
            return self._decode_pixel(self._block(x, y, x, y))

        if 0 <= x < self.width and 0 <= y < self.height:
            self._block(x, y, x, y, self._encode_pixel(color))
        return None

    #pylint: disable-msg=too-many-arguments
    def fill_rectangle(self, x, y, width, height, color):
        """Draw a filled rectangle."""
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        width = min(self.width - x, max(1, width))
        height = min(self.height - y, max(1, height))
        self._block(x, y, x + width - 1, y + height - 1, b'')
        chunks, rest = divmod(width * height, _BUFFER_SIZE)
        pixel = self._encode_pixel(color)
        if chunks:
            data = pixel * _BUFFER_SIZE
            for _ in range(chunks):
                self.write(None, data)
        self.write(None, pixel * rest)
    #pylint: enable-msg=too-many-arguments

    def fill(self, color=0):
        """Fill whole screen."""
        self.fill_rectangle(0, 0, self.width, self.height, color)

    def hline(self, x, y, width, color):
        """Draw a horizontal line."""
        self.fill_rectangle(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line."""
        self.fill_rectangle(x, y, 1, height, color)


class DisplaySPI(Display):
    """Base class for SPI type devices"""
    #pylint: disable-msg=too-many-arguments
    def __init__(self, spi, dc, cs, rst=None, width=1, height=1, baudrate=1000000,
                 polarity=0, phase=0):
        self.spi_device = spi_device.SPIDevice(spi, cs, baudrate=baudrate,
                                               polarity=polarity, phase=phase)
        self.dc_pin = dc
        self.rst = rst
        self.dc_pin.switch_to_output(value=0)
        if self.rst:
            self.rst.switch_to_output(value=0)
            self.reset()
        super().__init__(width, height)
    #pylint: enable-msg=too-many-arguments

    def reset(self):
        """Reset the device"""
        self.rst.value = 0
        time.sleep(0.050)  # 50 milliseconds
        self.rst.value = 1
        time.sleep(0.050)  # 50 milliseconds

    def write(self, command=None, data=None):
        """SPI write to the device: commands and data"""
        if command is not None:
            self.dc_pin.value = 0
            with self.spi_device as spi:
                spi.write(bytearray([command]))
        if data is not None:
            self.dc_pin.value = 1
            with self.spi_device as spi:
                spi.write(data)

    def read(self, command=None, count=0):
        """SPI read from device with optional command"""
        data = bytearray(count)
        self.dc_pin.value = 0
        with self.spi_device as spi:
            if command is not None:
                spi.write(bytearray([command]))
            if count:
                spi.readinto(data)
        return data
