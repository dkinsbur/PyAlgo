__author__ = 'dkinsbur'

class Broker(object):

    def __init__(self, balance, commision=0, min_commision=0, slipage=0):
        self.slipage = slipage
        self.balance = balance
        self.positions = {}
        self.closed_positions = []

    def buy(self, symbol, amount, price, time=None):

        price = float(price)  # make sure it is float
        self.balance -= amount * price

        if symbol not in self.positions:
            self.positions[symbol] = (amount, price)
        else:
            prev_amount, prev_price = self.positions[symbol]
            new_amount = prev_amount + amount
            new_price = ((prev_amount * prev_price) + (amount * price))/new_amount
            self.positions[symbol] = (new_amount, new_price)

        tm_str = '' if not time else '[{}]'.format(time)
        print '{}BUY {} {} {}'.format(tm_str, symbol, amount, price + self.slipage)

    def sell(self, symbol, amount, price, time=None):

        price = float(price)  # make sure it is float
        self.balance += amount * price

        if symbol not in self.positions:
            self.positions[symbol] = (amount, price)
        else:
            prev_amount, prev_price = self.positions[symbol]
            new_amount = prev_amount + amount
            new_price = ((prev_amount * prev_price) + (amount * price))/new_amount
            self.positions[symbol] = (new_amount, new_price)

        tm_str = '' if not time else '[{}]'.format(time)
        print '{}SELL {} {} {}'.format(tm_str, symbol, amount, price - self.slipage)

    def get_ballance(self):
        return self.balance

    def get_positions(self):
        return self.positions

    def get_closed_positions(self):
        return self.closed_positions


import unittest

class UltBroker(unittest.TestCase):

    def test_long_basic(self):
        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.sell('X', 100, 10.5)
        assert brok.get_ballance() == 10000 + 100*0.5

    def test_long_2buy(self):
        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.buy('X', 100, 10)
        brok.sell('X', 200, 10.5)
        assert brok.get_ballance() == 10000 + 200*0.5

        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.buy('X', 100, 10.5)
        brok.sell('X', 200, 10.5)
        assert brok.get_ballance() == 10000 + 100*0.5

    def test_long_2sell(self):
        brok = Broker(10000)
        brok.buy('X', 300, 10)
        brok.sell('X', 100, 11)
        brok.sell('X', 150, 8.5)
        brok.sell('X', 50, 8.5)
        assert brok.get_ballance() == 10000 + 100 + 200 * (-1.5)



if __name__ == '__main__':
    unittest.main()



