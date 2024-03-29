# The MIT License (MIT)
#
# Copyright (c) 2016 Radomir Dopieralski & Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
`adafruit_ht16k33.ht16k33`
===========================

* Authors: Radomir Dopieralski & Tony DiCola for Adafruit Industries

"""

from Adafruit_GPIO import I2C

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_HT16K33.git"

_HT16K33_BLINK_CMD = 0x80
_HT16K33_BLINK_DISPLAYON = 0x01
_HT16K33_CMD_BRIGHTNESS = 0xE0
_HT16K33_OSCILATOR_ON = 0x21


class HT16K33:
    """
    The base class for all displays. Contains common methods.

    :param int address: The I2C addess of the HT16K33.
    :param bool auto_write: True if the display should immediately change when
        set. If False, `show` must be called explicitly.
    """
    def __init__(self, address=0x70, auto_write=True):
        self.i2c_device = I2C.get_i2c_device(address)
        self._buffer = bytearray(16)
        self._auto_write = None
        self._auto_write = auto_write
        self.fill(0)
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self._blink_rate = None
        self._brightness = None
        self.blink_rate = 0
        self.brightness = 15

    def _write_cmd(self, byte):
        self.i2c_device.writeRaw8(byte)

    @property
    def blink_rate(self):
        """The blink rate. Range 0-3."""
        return self._blink_rate

    @blink_rate.setter
    def blink_rate(self, rate=None):
        if not 0 <= rate <= 3:
            raise ValueError('Blink rate must be an integer in the range: 0-3')
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD |
                        _HT16K33_BLINK_DISPLAYON | rate << 1)
        return None

    @property
    def brightness(self):
        """The brightness. Range 0-15."""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if not 0 <= brightness <= 15:
            raise ValueError('Brightness must be an integer in the range: 0-15')
        brightness = brightness & 0x0F
        self._brightness = brightness
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | brightness)
        return None

    @property
    def auto_write(self):
        """Auto write updates to the display."""
        return self._auto_write

    @auto_write.setter
    def auto_write(self, auto_write):
        if isinstance(auto_write, bool):
            self._auto_write = auto_write
        else:
            raise ValueError('Must set to either True or False.')

    def show(self):
        """Refresh the display and show the changes."""
        # 0x00 : address of LED data register.
        # bytes are the display register data to set.
        self.i2c_device.writeList(0x00, self._buffer)

    def fill(self, color):
        """Fill the whole display with the given color."""
        fill = 0xff if color else 0x00
        for i in range(16):
            self._buffer[i] = fill
        if self._auto_write:
            self.show()

    def _pixel(self, x, y, color=None):
        addr = 2*y + x // 8
        mask = 1 << x % 8
        if color is None:
            return bool(self._buffer[addr] & mask)
        if color:
            # set the bit
            self._buffer[addr] |= mask
        else:
            # clear the bit
            self._buffer[addr] &= ~mask
        if self._auto_write:
            self.show()
        return None

    def set_buffer(self, buffer):
         self._buffer = buffer
         if self._auto_write:
             self.show()
