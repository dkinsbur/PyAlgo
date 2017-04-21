__author__ = 'dkinsbur'

class Bar(object):

    def __init__(self, time, high, low, open, close, volume):
        self._time = time
        self._high = high
        self._low = low
        self._open = open
        self._close = close
        self._volume = volume

    def get_time(self):
        return self._time

    def get_high(self):
        return self._high

    def get_low(self):
        return self._low

    def get_open(self):
        return self._open

    def get_close(self):
        return self._close

    def get_volume(self):
        return self._volume

    def __str__(self):
        s = ''

        for attr in ['time', 'high', 'low', 'open', 'close', 'volume']:
            s += '{}={} | '.format(attr, getattr(self, 'get_'+attr)())

        return s


import unittest
class UltBar(unittest.TestCase):

    def test_bar_getters(self):
        time = 1
        high = 2
        low = 3
        Open = 4
        close = 5
        volume = 6
        b = Bar(time, high, low, Open, close, volume)
        self.assertEquals(time, b.get_time())
        self.assertEquals(high, b.get_high())
        self.assertEquals(low, b.get_low())
        self.assertEquals(Open, b.get_open())
        self.assertEquals(close, b.get_close())
        self.assertEquals(volume, b.get_volume())


if __name__ == '__main__':
    unittest.main()