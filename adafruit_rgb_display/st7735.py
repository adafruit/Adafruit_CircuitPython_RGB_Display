from adafruit_rgb_display.rgb import DisplaySPI


_NOP=const(0x00)
_SWRESET=const(0x01)
_RDDID=const(0x04)
_RDDST=const(0x09)

_SLPIN=const(0x10)
_SLPOUT=const(0x11)
_PTLON=const(0x12)
_NORON=const(0x13)

_INVOFF=const(0x20)
_INVON=const(0x21)
_DISPOFF=const(0x28)
_DISPON=const(0x29)
_CASET=const(0x2A)
_RASET=const(0x2B)
_RAMWR=const(0x2C)
_RAMRD=const(0x2E)

_PTLAR=const(0x30)
_COLMOD=const(0x3A)
_MADCTL=const(0x36)

_FRMCTR1=const(0xB1)
_FRMCTR2=const(0xB2)
_FRMCTR3=const(0xB3)
_INVCTR=const(0xB4)
_DISSET5=const(0xB6)

_PWCTR1=const(0xC0)
_PWCTR2=const(0xC1)
_PWCTR3=const(0xC2)
_PWCTR4=const(0xC3)
_PWCTR5=const(0xC4)
_VMCTR1=const(0xC5)

_RDID1=const(0xDA)
_RDID2=const(0xDB)
_RDID3=const(0xDC)
_RDID4=const(0xDD)

_PWCTR6=const(0xFC)

_GMCTRP1=const(0xE0)
_GMCTRN1=const(0xE1)


class ST7735(DisplaySPI):
    """
    A simple driver for the ST7735-based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.st7735 as st7735
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = st7735.ST7735(spi, cs=digitalio.DigitalInOut(board.GPIO0), dc=digitalio.DigitalInOut(board.GPIO15), rst=digitalio.DigitalInOut(board.GPIO16))
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
        (_COLMOD, b'\x05'), # 16bit color
        # fastest refresh, 6 lines front porch, 3 line back porch
        (_FRMCTR1, b'\x00\x06\x03'),
        (_MADCTL, b'\x08'), # bottom to top refresh
        # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
        # fix on VTL
        (_DISSET5, b'\x15\x02'),
        (_INVCTR, b'0x00'), # line inversion
        (_PWCTR1, b'\x02\x70'), # GVDD = 4.7V, 1.0uA
        (_PWCTR2, b'\x05'), # VGH=14.7V, VGL=-7.35V
        (_PWCTR3, b'\x01\x02'), # Opamp current small, Boost frequency
        (_VMCTR1, b'\x3c\x38'), # VCOMH = 4V, VOML = -1.1V
        (_PWCTR6, b'\x11\x15'),
        (_GMCTRP1, b'\x09\x16\x09\x20\x21\x1b\x13\x19'
                   b'\x17\x15\x1e\x2b\x04\x05\x02\x0e'), # Gamma
        (_GMCTRN1, b'\x08\x14\x08\x1e\x22\x1d\x18\x1e'
                   b'\x18\x1a\x24\x2b\x06\x06\x02\x0f'),
        (_CASET, b'\x00\x02\x00\x81'), # XSTART = 2, XEND = 129
        (_RASET, b'\x00\x02\x00\x81'), # XSTART = 2, XEND = 129
        (_NORON, None),
        (_DISPON, None),
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"

    def __init__(self, spi, dc, cs, rst=None, width=128, height=128):
        super().__init__(spi, dc, cs, rst, width, height)
