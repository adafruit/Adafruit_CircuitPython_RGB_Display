from adafruit_rgb_display.rgb import DisplaySPI

_SWRESET = const(0x01)
_NORON = const(0x13)
_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2a)
_PASET = const(0x2b)
_RAMWR = const(0x2c)
_RAMRD = const(0x2e)
_MADCTL = const(0x36)
_COLMOD = const(0x3a)

class HX8353(DisplaySPI):
    """
    A simple driver for the ST7735-based displays.

    >>> import nativeio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.hx8353 as hx8353
    >>> spi = nativeio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = hx8353.HX8383(spi, cs=nativeio.DigitalInOut(board.GPIO0), dc=nativeio.DigitalInOut(board.GPIO15))
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

    def __init__(self, spi, dc, cs, rst=None, width=128, height=128):
        super().__init__(spi, dc, cs, rst, width, height)
