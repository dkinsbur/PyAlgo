__author__ = 'dkinsbur'

DOWN = -1
UP = 1

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

    def init(self, start_price, start_time):
        self.price = start_price,

        self.absolute_max = start_price
        self.absolute_min = start_price

        self.local_max = start_price
        self.local_min = start_price
        self.local_max_time = start_time
        self.local_min_time = start_time

    def add(self, (price, time)):
        if not self.started:
            self.init(price, time)
            self.started = True
            return
        self.absolute_max = max(price, self.absolute_max)
        self.absolute_min = min(price, self.absolute_min)

        if price > self.price:
            if self.trend == UP:
                if price > self.local_max:
                    self.local_max = price
                    self.local_max_time = time
            else:
                if price - self.threshold > self.local_min:
                    self.trend = UP
                    self.local_max = price
                    self.local_max_time = time
                    self.pivots.append(('L', self.local_min, self.local_min_time))

        elif price < self.price:
            if self.trend == DOWN:
                if price < self.local_min:
                    self.local_min =  price
                    self.local_min_time =  time
            else:
                if price + self.threshold < self.local_max:
                    self.trend = DOWN
                    self.local_min = price
                    self.local_min_time = time
                    self.pivots.append(('H', self.local_max, self.local_max_time))

        self.price = price

