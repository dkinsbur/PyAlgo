__author__ = 'dkinsbur'

from datetime import timedelta, datetime

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
        return '[BAR]' + '|'.join('{}={}'.format(attr, getattr(self, 'get_'+attr)()) for attr in ['time', 'high', 'low', 'open', 'close', 'volume'])

    def __eq__(self, other):
        if (self.get_time() == other.get_time() and
            self.get_high() == other.get_high() and
            self.get_low() == other.get_low() and
            self.get_open()  == other.get_open() and
            self.get_close() == other.get_close() and
            self.get_volume() == other.get_volume()):
            return True
        else:
            return False


class CsvBar(Bar):
    def __init__(self, csv_line, time_format):
        time, high, low, Open, close, volume = csv_line.strip().split(',')
        time = datetime.strptime(time, time_format)
        high = float(high)
        low = float(low)
        Open = float(Open)
        close = float(close)
        volume = int(volume)
        super(CsvBar, self).__init__(time, high, low, Open, close, volume)


class MergedBar(Bar):

    def __init__(self, bars, round_mod=1):
        self._time = None
        for bar in bars:
            if not self._time:
                self._time = bar.get_time()
                self._high = bar.get_high()
                self._low = bar.get_low()
                self._open = bar.get_open()
                self._close = bar.get_close()
                self._volume = bar.get_volume()
            else:
                assert self._time < bar.get_time(), '{} - {}'.format(self._time, bar.get_time())  # make sure we start from first to last
                self._high = max(self._high, bar.get_high())
                self._low = min(self._low, bar.get_low())
                self._close = bar.get_close()
                self._volume += bar.get_volume()

        if round_mod > 1:

            self._time -= timedelta(minutes=self._time.minute % round_mod)




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