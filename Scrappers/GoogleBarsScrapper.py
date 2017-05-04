__author__ = 'dkinsbur'

from datetime import datetime, time, timedelta
from AlgoRepo.AlgoBase.Bar import Bar
import urllib2


URL_TEMPLATE = 'https://www.google.com/finance/getprices?i={interval}&p={period}&f=d,o,h,l,c,v&q={symbol}'

INTERVAL_MINUTE = 60
INTERVAL_5_MINUTE = 300
INTERVAL_DAY = 86400

INTERVALS = [INTERVAL_DAY, INTERVAL_MINUTE, INTERVAL_5_MINUTE]

NY_TIME_DELTA = timedelta(hours=-4)
CSV_BAR_DATE_FORMAT = '%Y-%m-%d-%H-%M'

def PERIOD_DAY(days):
    return '%ud' % days

def PERIOD_MINUTE(minutes):
    return '%um' % minutes

def PERIOD_YEAR(years):
    return '%uY' % years


class GoogleBarsScrapper(object):

    def _get_url(self, symbol, interval, period):
        return URL_TEMPLATE.format(interval=interval, period=period, symbol=symbol)

    def _epoch_to_datetime(self, epoch_date):
        return datetime.utcfromtimestamp(epoch_date) + NY_TIME_DELTA

    def collect(self, symbol, interval, period):
        return [Bar(self._epoch_to_datetime(date), high, low, Open, close, volume)
                for date, close, high, low, Open, volume in self.collect_raw(symbol, interval, period)]

    def collect_raw(self, symbol, interval, period):

        assert interval in INTERVALS

        url_page = urllib2.urlopen(self._get_url(symbol, interval, period))
        bars = []
        for line in url_page:

            # skip metadata
            if line[0] not in 'a1234567890':
                continue

            args = line.strip().split(',')
            data = [float(x) for x in args[1:-1]]
            data.append(int(args[-1]))
            if args[0].startswith('a'):
                curr_time = int(args[0][1:])
                data.insert(0, curr_time)
            else:
                data.insert(0, curr_time + int(args[0])*interval)

            bars.append(data)

        return bars

    def dump(self, symbol, interval, period, fname):
        data = self.collect(symbol, interval, period)
        with open(fname, 'w') as f:
            f.write('date,high,low,open,close,volume\n')
            for bar in data:
                f.write('{},{},{},{},{},{}\n'.format(
                    bar.get_time().strftime(CSV_BAR_DATE_FORMAT),
                    bar.get_high(), bar.get_low(),
                    bar.get_open(), bar.get_close(),
                    bar.get_volume())
                )


import unittest
class UltBar(unittest.TestCase):

    def test_collect_raw_minutes(self):
        g = GoogleBarsScrapper()
        bars = g.collect_raw('X', INTERVAL_MINUTE, PERIOD_MINUTE(22))
        for bar in bars:
            self.assertEqual(len(bar), 6)
            self.assertEqual([type(b) for b in bar], [int, float, float, float, float, int])
        print  g._get_url('X', INTERVAL_MINUTE, PERIOD_MINUTE(22))
        self.assertEquals(len(bars), 22+1)

    def test_collect_raw_5minutes(self):
        g = GoogleBarsScrapper()
        for bar in g.collect_raw('X', INTERVAL_5_MINUTE, PERIOD_DAY(1)):
            self.assertEqual(len(bar), 6)
            self.assertEqual([type(b) for b in bar], [int, float, float, float, float, int])

    def test_collect_raw_days(self):
        g = GoogleBarsScrapper()
        bars = g.collect_raw('X', INTERVAL_DAY, PERIOD_DAY(20))
        for bar in bars:
            self.assertEqual(len(bar), 6)
            self.assertEqual([type(b) for b in bar], [int, float, float, float, float, int])
        print  g._get_url('X', INTERVAL_DAY, PERIOD_DAY(20))
        self.assertEquals(len(bars), 20)

    def test_collect_bars(self):
        g = GoogleBarsScrapper()
        raw = g.collect_raw('X', INTERVAL_MINUTE, PERIOD_DAY(3))
        bars = g.collect('X', INTERVAL_MINUTE, PERIOD_DAY(3))
        self.assertEquals(len(raw), len(bars)) #compare lengths

        for i in range(len(raw)):
            r = raw[i]
            b = bars[i]

            # compare values
            date, close, high, low, Open, volume = r
            self.assertEquals(Bar(g._epoch_to_datetime(date), high, low, Open, close, volume), b)

            # check time zone
            self.assertTrue(time(hour=9, minute=30) <= b.get_time().time() and b.get_time().time() <= time(hour=16), "time={}|epoch={} expected to be between 9:30..16:00".format(b.get_time().time(), r[0]))

    def test_epoch_convert(self):
        g = GoogleBarsScrapper()

        epoch = 1493939420
        self.assertEquals(g._epoch_to_datetime(epoch), datetime.utcfromtimestamp(epoch) + NY_TIME_DELTA)

        epoch = 1493904600
        self.assertEquals(g._epoch_to_datetime(epoch), datetime(day=04, month=5, year=2017, hour=9, minute=30))

    def test_dump(self):
        import os
        from AlgoRepo.AlgoBase.Feed import CsvBarFeed

        fname = 'temp.txt'

        def on_bar(f, bar):
            f.count += 1

        g = GoogleBarsScrapper()
        g.dump('X', INTERVAL_DAY, PERIOD_DAY(13), fname)

        self.assertTrue(os.path.isfile(fname))

        feed = CsvBarFeed(fname)
        feed.count = 0
        feed.register(on_bar, None)
        feed.go()

        self.assertEquals(feed.count, 13)
        os.remove(fname)

if __name__ == '__main__':
    unittest.main()