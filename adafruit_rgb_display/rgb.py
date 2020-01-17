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
`adafruit_rgb_display.rgb`
====================================================

Base class for all RGB Display devices

* Author(s): Radomir Dopieralski, Michael McWethy, Jonah Yolles-Murphy
"""

import time
import gc

try:
    import numpy
except ImportError:
    numpy = None
try:
    import struct
except ImportError:
    import ustruct as struct

import adafruit_bus_device.spi_device as spi_device

try:
    from terminalio import FONT as _FONT
    #from fonts.default import font as _FONT
except:
    _FONT = None

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display.git"

# This is the size of the buffer to be used for fill operations, in 16-bit
# units.
_BUFFER_SIZE = 256
try:
    import platform
    if "CPython" in platform.python_implementation():
        _BUFFER_SIZE = 320 * 240 # blit the whole thing
except ImportError:
    pass

def color565(r, g=0, b=0):
    """Convert red, green and blue values (0-255) into a 16-bit 565 encoding.  As
    a convenience this is also available in the parent adafruit_rgb_display
    package namespace."""
    try:
        r, g, b = r  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

def image_to_data(image):
    """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
    #NumPy is much faster at doing this. NumPy code provided by:
    #Keith (https://www.blogger.com/profile/02555547344016007163)
    data = numpy.array(image.convert('RGB')).astype('uint16')
    color = ((data[:, :, 0] & 0xF8) << 8) | ((data[:, :, 1] & 0xFC) << 3) | (data[:, :, 2] >> 3)
    return numpy.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()

class DummyPin:
    """Can be used in place of a ``DigitalInOut()`` when you don't want to skip it."""
    def deinit(self):
        """Dummy DigitalInOut deinit"""
        pass

    def switch_to_output(self, *args, **kwargs):
        """Dummy switch_to_output method"""
        pass

    def switch_to_input(self, *args, **kwargs):
        """Dummy switch_to_input method"""
        pass

    @property
    def value(self):
        """Dummy value DigitalInOut property"""
        pass

    @value.setter
    def value(self, val):
        pass

    @property
    def direction(self):
        """Dummy direction DigitalInOut property"""
        pass

    @direction.setter
    def direction(self, val):
        pass

    @property
    def pull(self):
        """Dummy pull DigitalInOut property"""
        pass

    @pull.setter
    def pull(self, val):
        pass

class Display: #pylint: disable-msg=no-member
    """Base class for all RGB display devices
        :param width: number of pixels wide
        :param height: number of pixels high
        :param rotation: the rotation of the display in degrees
    """
    _PAGE_SET = None
    _COLUMN_SET = None
    _RAM_WRITE = None
    _RAM_READ = None
    _X_START = 0 # pylint: disable=invalid-name
    _Y_START = 0 # pylint: disable=invalid-name
    _INIT = ()
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    def __init__(self, width, height, rotation, default_text_size = 1, default_font = _FONT, fast_text = True, DEBUG = False):
        self.width = width
        self.height = height
        if rotation not in (0, 90, 180, 270):
            raise ValueError('Rotation must be 0/90/180/270')
        self._rotation = rotation
        self.default_font = default_font
        self.default_text_size = default_text_size
        self._font_glyph_coord_caches = {}
        self.fast_text = fast_text

        self._last_calcualted_string_specs = ([None], -1, -1)

        self.DEBUG = DEBUG

        self.init()

    def _dbgout(self, *args, **kwargs):
        if self.DEBUG:
            print(args, kwargs)

    def init(self):
        """Run the initialization commands."""
        for command, data in self._INIT:
            self.write(command, data)

    #pylint: disable-msg=invalid-name,too-many-arguments
    def _block(self, x0, y0, x1, y1, data=None, scale=1):
        """Read or write a block of data."""
        if data is None:
            #write destination to display
            self.write(self._COLUMN_SET, self._encode_pos(x0 + self._X_START, x1 + self._X_START))
            self.write(self._PAGE_SET, self._encode_pos(y0 + self._Y_START, y1 + self._Y_START))

            size = struct.calcsize(self._DECODE_PIXEL)
            return self.read(self._RAM_READ, (x1 - x0 + 1) * (y1 - y0 + 1) * size)
        else:
            #make a larger bytearray if > 1
            if scale > 1:
                ##self._dbgout(x0, y0, x1, y1)
                ##self._dbgout(x1 - x0 + 1, y1 - y0 + 1)
                source_width = (x1 - x0 + 1)
                source_height = (y1 - y0 + 1)
                source = data

                data_width = source_width * scale
                data_height = source_height * scale
                data = bytearray(source_width * 2  * source_height * scale**2)

                #magic :-)
                for y in range(0, source_height*2, 2): # evey pixel in the source (bytearray adressed)
                    for x in range(0, source_width*2, 2):
                        high_byte = source[x + source_width*y]
                        low_byte =  source[x + source_width*y + 1]
                        x_base = x * scale #left most pos of pixel
                        y_base = y * scale * data_width  #the top most pos of the pixe
                        for line in range(0, scale*2* data_width , 2*data_width ):
                            for pixel in range(0, scale*2, 2):
                                data[x_base + pixel + (y_base) + line ] = high_byte
                                data[x_base + pixel + (y_base) + line + 1] = low_byte

                #adjust x1 to match new size
                x1 = x0 + data_width -1
                y1 = y0 + data_height -1

                del source, source_width, source_height
                del data_width, data_height
                del x, y, high_byte, low_byte, x_base, y_base
                del line, pixel

            # write destination  to display
            self.write(self._COLUMN_SET, self._encode_pos(x0 + self._X_START, x1 + self._X_START))
            self.write(self._PAGE_SET, self._encode_pos(y0 + self._Y_START, y1 + self._Y_START))

            # write data to display
            self.write(self._RAM_WRITE, data)
            del data, x0, x1, y0, y1
            gc.collect()
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
        """Read or write a pixel at a given position."""
        if color is None:
            return self._decode_pixel(self._block(x, y, x, y))

        if 0 <= x < self.width and 0 <= y < self.height:
            self._block(x, y, x, y, self._encode_pixel(color))
        return None

    def image(self, img, rotation=None, x=0, y=0):
        """Set buffer to value of Python Imaging Library image. The image should
        be in 1 bit mode and a size not exceeding the display size when drawn at
        the supplied origin."""
        if rotation is None:
            rotation = self.rotation
        if not img.mode in ('RGB', 'RGBA'):
            raise ValueError('Image must be in mode RGB or RGBA')
        if rotation not in (0, 90, 180, 270):
            raise ValueError('Rotation must be 0/90/180/270')
        if rotation != 0:
            img = img.rotate(rotation, expand=True)
        imwidth, imheight = img.size
        if x + imwidth > self.width or y + imheight > self.height:
            raise ValueError('Image must not exceed dimensions of display ({0}x{1}).' \
                .format(self.width, self.height))
        if numpy:
            pixels = list(image_to_data(img))
        else:
            # Slower but doesn't require numpy
            pixels = bytearray(imwidth * imheight * 2)
            for i in range(imwidth):
                for j in range(imheight):
                    pix = color565(img.getpixel((i, j)))
                    pixels[2*(j * imwidth + i)] = pix >> 8
                    pixels[2*(j * imwidth + i) + 1] = pix & 0xFF
        self._block(x, y, x + imwidth - 1, y + imheight - 1, pixels)

    #pylint: disable-msg=too-many-arguments
    def fill_rectangle(self, x, y, width, height, color):
        """Draw a rectangle at specified position with specified width and
        height, and fill it with the specified color."""
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
        """Fill the whole display with the specified color."""
        self.fill_rectangle(0, 0, self.width, self.height, color)

    def hline(self, x, y, width, color):
        """Draw a horizontal line."""
        self.fill_rectangle(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line."""
        self.fill_rectangle(x, y, 1, height, color)

    def text(self, x, y, string, size=0, color=0xffff, background=0x00, font=None, fast=None, estimate = False, center = False):
        """draws text on the display of specififed color and background,
            returns the width and hieght of the text placed
            :param int x: the horizontal position of the left side of the text
            :param int y: the vertical position of the top of the text
            :param str string: the text to be displayed on the screen
            :param int size: the scaling factor of the text, must be a whole number, defaults to display.default_text_size
            :param int color: the color filling the characters, in rgb565 format, defaults to white
            :param int backgound: is the color surrounding the characters, in rgb565 format, defaults to black
            :param BuiltinFont font: the font to be used for the characters, defaults to display.default_font
            :param bool fast: specifies to prioritize speed or memory usage.
            :param bool estimate: does not place text, just retuns the (width, height) tuple
            :param bool center: centers the text around the x,y coordinates specified
        """
        # later addin: backgound = None for transparent, but needs lower level tie-ins

        #check input types and defaults
        if (type(size) != int) or (size <=0):
            raise ValueError("size must be a whole number of type 'int'")
        if (type(color) != int) or (type(background) != int):
            raise ValueError("color and background must be a whole number of type 'int'")

        if font == None: # set to default font
            if self.default_font == None:
                raise ValueError("No font or .default_font specified")
            else:
                font = self.default_font

        if size <= 0:
            size = self.default_text_size

        if fast == None:
            fast = self.fast_text

        lines = [line.strip() for line in string.split('\n')]

        if center: # if centered find the toal size
            #note calculations are stored in self._last_calcualted_string_specs
            width, height = self.text(x, y, string, size=size,
                                        color=color, background=background,
                                        font=font, estimate = True,
                                        fast = True, center = False)
            domain_lines, buffer_width, buffer_height = self._last_calcualted_string_specs
            x -= width //2
            y -= height //2
            #del width, height


        if (fast == False) and (estimate == False):
            max_width = 0
            total_height = 0
            for line_index in range(len(lines)): # intentional
                line = lines[line_index]
                if center:
                    #domain_lines, buffer_width, buffer_height = self._last_calcualted_string_specs
                    print(x , (buffer_width - domain_lines[line_index][-1]) // 2, x + (buffer_width - domain_lines[line_index][-1]) // 2)
                    x_adj = x + (buffer_width/size - domain_lines[line_index][-1]) // 2
                else:
                    x_adj = x
                new_width, new_height = self.text(x_adj, y+total_height, line, size=size,
                                                    color=color, background=background,
                                                    font=font, fast=True, center = False) #, center = center)
                max_width = max(max_width, new_width)
                total_height += new_height
            del x_adj
            return max_width, total_height


        #calculate color bytes ahead of time
        color_high = (color & 0xff00) >> 8
        color_low  = (color & 0x00ff) >> 0
        background_high = (background & 0xff00) >> 8
        background_low  = (background & 0x00ff) >> 0

        #fetch the font_glyph_cache of letter locations and dimensions
        #the cache is identified by it's python object id
        fontmap = font.bitmap
        font_id = id(fontmap)
        font_caches = self._font_glyph_coord_caches
        if font_id in font_caches:
            #self._dbgout('found desired font cached! id:', font_id)
            font_cache = font_caches[font_id]
        else:
            #self._dbgout('desired font NOT cached! id:', font_id)
            font_cache = {}
            font_caches[font_id] = font_cache
        del font_caches, font_id

        # create a list of
        buffer_width = 1 # in pixels (not scalled by size)
        buffer_height = 0#1 #

        if center:
            domain_lines, buffer_width, buffer_height = self._last_calcualted_string_specs
        else:
            domain_lines = []
            for line in lines:
                domain_line = []
                line_width = 1
                domain_lines.append(domain_line)
                for char in line:

                    #get the glyph from the cache or the font
                    glyph_domain = font_cache.get(char)
                    # if glyph is not cached cache it
                    if glyph_domain == None:
                        #self._dbgout("caching new char:'"+char+"'")
                        glyph = font.get_glyph(ord(char))
                        glyph_domain = (glyph.tile_index, glyph.width, glyph.height)
                        font_cache[char] = glyph_domain

                    #add the glyph to the current line
                    domain_line.append((char, glyph_domain, line_width, buffer_height))
                    line_width += glyph_domain[1] + 1
                print('line_width', line_width)
                domain_line.append(line_width)
                print(domain_line[-1])
                buffer_width = max(buffer_width, line_width)
                buffer_height += fontmap.height
            del line, lines, line_width
            gc.collect()# incase low on ram

        if estimate:
            self._last_calcualted_string_specs = (domain_lines, buffer_width, buffer_height)
            return buffer_width*size, buffer_height*size
        else:
            self._last_calcualted_string_specs = ([None], -1, -1)

        #buffer_width *= size
        #buffer_height *= size
        buffer_length = buffer_width * buffer_height * 2 #* size**2
        buffer = bytearray(buffer_length)
        #self._dbgout(buffer_len = buffer_length, buffer_width=buffer_width, buffer_height=buffer_height)

        #write the
        for domain_line in domain_lines:
            for positioned_domain in domain_line[:-1]:
                char, domain, char_x, char_y = positioned_domain
                index, width, height = domain
                if center and fast: # if slow handled below line by line
                    char_x += (buffer_width - domain_line[-1])//2

                for pixel_y in range(height):
                    #stripe the left sode of the char w/ background
                    edge_pixel_index = (((char_y + pixel_y ) * buffer_width) + char_x - 1) * 2
                    buffer[edge_pixel_index] = background_high
                    buffer[edge_pixel_index + 1] = background_low

                    for pixel_x in range(width):

                        #if size == 1: # yeah, it;s an optimization but  ¯\_(ツ)_/¯
                        pixel_index = (((char_y + pixel_y) * buffer_width) + char_x + pixel_x) * 2
                        if fontmap[index*width + pixel_x, pixel_y]:
                            buffer[pixel_index] = color_high
                            buffer[pixel_index + 1] = color_low
                        else:
                            buffer[pixel_index] = background_high
                            buffer[pixel_index + 1] = background_low

        del domain_line, domain_lines, positioned_domain
        del char, domain, char_x, char_y
        del index, width, height
        del pixel_y, pixel_x, pixel_index
        del color_high, color_low, background_high, background_low

        #sendt he buffer to the display
        gc.collect() # incase low on ram before block goes out
        #if center:
            #x += buffer_width//2
        #    y -= buffer_height//2
        self._block(x, y, buffer_width + x - 1, buffer_height + y - 1, data=buffer, scale=size) # scale=size
        del buffer, x, y
        gc.collect()

        return buffer_width*size, buffer_height*size

    @property
    def rotation(self):
        """Set the default rotation"""
        return self._rotation

    @rotation.setter
    def rotation(self, val):
        if val not in (0, 90, 180, 270):
            raise ValueError('Rotation must be 0/90/180/270')
        self._rotation = val

class DisplaySPI(Display):
    """Base class for SPI type devices"""
    #pylint: disable-msg=too-many-arguments
    def __init__(self, spi, dc, cs, rst=None, width=1, height=1,
                 baudrate=12000000, polarity=0, phase=0, *,
                 x_offset=0, y_offset=0, rotation=0, **kwargs):
        self.spi_device = spi_device.SPIDevice(spi, cs, baudrate=baudrate,
                                               polarity=polarity, phase=phase)
        self.dc_pin = dc
        self.rst = rst
        self.dc_pin.switch_to_output(value=0)
        if self.rst:
            self.rst.switch_to_output(value=0)
            self.reset()
        self._X_START = x_offset # pylint: disable=invalid-name
        self._Y_START = y_offset # pylint: disable=invalid-name
        super().__init__(width, height, rotation, **kwargs)
    #pylint: enable-msg=too-many-arguments

    def reset(self):
        """Reset the device"""
        self.rst.value = 0
        time.sleep(0.050)  # 50 milliseconds
        self.rst.value = 1
        time.sleep(0.050)  # 50 milliseconds

    # pylint: disable=no-member
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
