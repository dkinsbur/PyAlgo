from AlgoRepo.AlgoBase.Bar import Bar
from collections import namedtuple
__author__ = 'dkinsbur'

TREND_DOWN = -1
TREND_UP = 1
PIVOT_LOW = 'L'
PIVOT_HIGH = 'H'
Pivot = namedtuple('Pivot', ('type','price', 'time'))

class Trend(object):
    def __init__(self, threshold):
        self.pivots = []
        self.started = False
        self.threshold = threshold

        self.price = None,

        self.absolute_max = None
        self.absolute_min = None

        self.local_max = None
        self.local_min = None
        self.local_max_time = None
        self.local_min_time = None

        self.trend = 0

        self.pivot_found = []

        self.trend_flip = False

    def register(self, pivot_found_callback):
        self.pivot_found.append(pivot_found_callback)

    def init(self, start_price, start_time):
        self.price = start_price,

        self.absolute_max = start_price
        self.absolute_min = start_price

        self.local_max = start_price
        self.local_min = start_price
        self.local_max_time = start_time
        self.local_min_time = start_time

    def get_pivots(self):
        return self.pivots

    def add(self, (price, time)):
        if not self.started:
            self.init(price, time)
            self.started = True
            return

        self.trend_flip = False

        self.absolute_max = max(price, self.absolute_max)
        self.absolute_min = min(price, self.absolute_min)

        if price > self.price:
            if self.trend == TREND_UP:
                if price > self.local_max:
                    self.local_max = price
                    self.local_max_time = time
            else:
                if price - self.threshold > self.local_min:
                    self.trend = TREND_UP
                    self.trend_flip = True
                    self.local_max = price
                    self.local_max_time = time
                    self._new_pivot('L', self.local_min, self.local_min_time)

        elif price < self.price:
            if self.trend == TREND_DOWN:
                if price < self.local_min:
                    self.local_min =  price
                    self.local_min_time =  time
            else:
                if price + self.threshold < self.local_max:
                    self.trend = TREND_DOWN
                    self.trend_flip = True
                    self.local_min = price
                    self.local_min_time = time
                    self._new_pivot('H', self.local_max, self.local_max_time)

        self.price = price

    def _new_pivot(self, type, price, time):
        p = Pivot(type, price, time)
        self.pivots.append(p)
        self._pivot_found(p)

    def get_trend(self):
        return self.trend

    def get_trend_flip(self):
        return self.trend_flip

    def _pivot_found(self, pivot):
        for cb in self.pivot_found:
            cb(pivot)

class TrendBar(Trend):

    def __init__(self, threshold, bar_attr):
        super(TrendBar, self).__init__(threshold)
        self.attr = bar_attr
        self.bar_price = getattr(Bar, bar_attr)
        assert callable(self.bar_price)

    #def add(self, (price, time)):
    def add(self, bar):
        super(TrendBar, self).add((self.bar_price(bar), bar.get_time()))
