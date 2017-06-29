__author__ = 'dkinsbur'

class Broker(object):

    def __init__(self, balance, commision=0, min_commision=0, slipage=0, log=True):
        self.slipage = slipage
        self.balance = balance
        self.positions = {}
        self.closed_positions = []
        self.log = log

    def buy(self, symbol, amount, price, time=None):

        assert amount > 0
        assert price > 0

        price = float(price)  # make sure it is float
        price += self.slipage  # increase slipage from price
        self.balance -= amount * price

        #  check if this is a new position
        if symbol not in self.positions:
            self.positions[symbol] = (amount, -price*amount)

        else:
            #  calc the new amount of position shares
            prev_amount, prev_balance = self.positions[symbol]
            new_amount = prev_amount + amount

            #  check if we closed short position
            if new_amount == 0:
                self.closed_positions.append((symbol, round(prev_balance - price*amount), 4))
                if self.log:
                    print ((symbol, round(prev_balance - price*amount), 4))
                self.positions.pop(symbol)

            #  we were in a short position and stayed in a short position
            elif new_amount < 0:
                self.positions[symbol] = (new_amount, prev_balance - price*amount)

            # check if we are in a long position
            elif new_amount > 0:
                # check if we were in a short position closed it and started a long position
                if prev_amount < 0:
                    amount_to_close_pos = -prev_amount
                    self.closed_positions.append((symbol, round(prev_balance-price*amount_to_close_pos, 4)))
                    if self.log:
                        print ((symbol, round(prev_balance-price*amount_to_close_pos, 4)))
                    self.positions[symbol] = (new_amount, -price*new_amount)

                # we added shares to our long position
                else:
                    self.positions[symbol] = (new_amount, prev_balance-price*amount)

        tm_str = '' if not time else '[{}]'.format(time)
        if self.log:
            print '{}BUY {} {} {}'.format(tm_str, symbol, amount, price)

    def sell(self, symbol, amount, price, time=None):

        assert amount > 0
        assert price > 0

        amount = -amount  # we are selling shares so the amount is negative
        price = float(price)  # make sure it is float
        price -= self.slipage  # decrease slipage from price
        self.balance -= amount * price

        #  check if this is a new position
        if symbol not in self.positions:
            self.positions[symbol] = (amount, -price*amount)

        else:
            #  calc the new amount of position shares
            prev_amount, prev_balance = self.positions[symbol]
            new_amount = prev_amount + amount

            #  check if we closed long position
            if new_amount == 0:
                self.closed_positions.append((symbol, round(prev_balance - price*amount, 4)))
                if self.log:
                    print ((symbol, round(prev_balance - price*amount, 4)))
                self.positions.pop(symbol)

            #  we were in a long position and stayed in a long position
            elif new_amount > 0:
                self.positions[symbol] = (new_amount, prev_balance - price*amount)

            # check if we are in a short position
            elif new_amount < 0:
                # check if we were in a long position closed it and started a short position
                if prev_amount > 0:
                    amount_to_close_pos = -prev_amount
                    self.closed_positions.append((symbol, round(prev_balance-price*amount_to_close_pos,4)))
                    if self.log:
                        print ((symbol, round(prev_balance-price*amount_to_close_pos,4)))
                    self.positions[symbol] = (new_amount, -price*new_amount)

                # we added shares to our short position
                else:
                    self.positions[symbol] = (new_amount, prev_balance-price*amount)

        tm_str = '' if not time else '[{}]'.format(time)
        if self.log:
            print '{}SELL {} {} {}'.format(tm_str, symbol, amount, price)

    def get_ballance(self):
        return self.balance

    def get_positions(self):
        return self.positions

    # average
    def get_average_price(self, symbol):
        if symbol not in self.positions:
            return None

        amount, balance = self.positions[symbol]
        return -round(float(balance)/amount, 4)


    def get_closed_positions(self):
        return self.closed_positions


import unittest

class UltBrokerBasic(unittest.TestCase):

    def test_long_basic(self):
        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.sell('X', 100, 10.5)
        self.assertEquals(brok.get_ballance(), 10000 + 100*0.5)

    def test_long_2buy(self):
        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.buy('X', 100, 10)
        brok.sell('X', 200, 10.5)
        self.assertEquals(brok.get_ballance(), 10000 + 200*0.5)

        brok = Broker(10000)
        brok.buy('X', 100, 10)
        brok.buy('X', 100, 10.5)
        brok.sell('X', 200, 10.5)
        self.assertEquals(brok.get_ballance(), 10000 + 100*0.5)

    def test_long_2sell(self):
        brok = Broker(10000)
        brok.buy('X', 300, 10)
        brok.sell('X', 100, 11)
        brok.sell('X', 150, 8.5)
        brok.sell('X', 50, 8.5)
        self.assertEquals(brok.get_ballance(), 10000 + 100 + 200 * (-1.5))

    def test_long_loss(self):
        brok = Broker(10000)
        brok.buy('X', 200, 10)
        brok.sell('X', 100, 9.5)
        brok.sell('X', 100, 9.75)
        self.assertEquals(brok.get_ballance(), 10000 - 200*10 + 100*9.5 + 100*9.75)

    #################### SHORT ##########################

    def test_short_basic(self):
        brok = Broker(10000)
        brok.sell('X', 100, 10)
        brok.buy('X', 100, 10.5)
        brok.buy('X', 100, 10.75)
        self.assertEquals(brok.get_ballance(), 10000 + 100*10 - 100*10.75 - 100*10.5)

    def test_short_2sell(self):
        brok = Broker(10000)
        brok.sell('X', 100, 10.5)
        brok.sell('X', 100, 10.5)
        brok.buy('X', 200, 10)
        self.assertEquals(brok.get_ballance(), 10000 + 100*10.5  + 100*10.5 - 200*10)

        brok = Broker(10000)
        brok.sell('X', 100, 10.5)
        brok.sell('X', 100, 10)
        brok.buy('X', 200, 10.5)
        self.assertEquals(brok.get_ballance(), 10000 + 100*10.5 + 100*10 - 200*10.5)

class UltBrokerPosition(unittest.TestCase):
    def test_long_position1(self):
        brok = Broker(10000)
        brok.buy('AMD', 100, 50)
        brok.buy('AMD', 100, 100)
        pos = brok.get_positions()
        self.assertEquals(pos['AMD'], (200, -15000))
        self.assertEqual(brok.get_average_price('AMD'), round(float(15000)/200, 4))

    def test_long_position2(self):
        brok = Broker(10000)
        brok.buy('AMD', 100, 50)
        brok.buy('AMD', 200, 100)
        pos = brok.get_positions()
        self.assertEquals(pos['AMD'], (300, -25000))
        self.assertEqual(brok.get_average_price('AMD'), round(float(25000)/300, 4))

    def test_short_position1(self):
        brok = Broker(10000)
        brok.sell('AMD', 100, 50)
        brok.sell('AMD', 100, 100)
        pos = brok.get_positions()
        self.assertEquals(pos['AMD'], (-200, 15000))
        self.assertEqual(brok.get_average_price('AMD'), round(float(15000)/200, 4))

    def test_short_position2(self):
        brok = Broker(10000)
        brok.sell('AMD', 100, 50)
        brok.sell('AMD', 200, 100)
        pos = brok.get_positions()
        self.assertEquals(pos['AMD'], (-300, 25000))
        self.assertEqual(brok.get_average_price('AMD'), round(float(25000)/300, 4))

    def test_long_to_short(self):
        brok = Broker(10000)
        brok.buy('DAL', 100, 100)
        brok.sell('AAL', 100, 110)
        brok.sell('DAL', 200, 110)
        closed = brok.get_closed_positions()
        pos = brok.get_positions()
        self.assertEqual(1, len(closed))
        self.assertEqual(2, len(pos))

        self.assertEqual(closed[0][0], 'DAL')
        self.assertEqual(closed[0][1], 11000-10000)
        self.assertEqual(pos['AAL'], (-100, 11000))
        self.assertEqual(pos['DAL'], (-100, 11000))


    def test_short_to_long(self):
        brok = Broker(10000)
        brok.sell('DAL', 100, 100)
        brok.sell('DAL', 100, 110)
        brok.buy('DAL', 500, 230)
        closed = brok.get_closed_positions()
        pos = brok.get_positions()
        self.assertEqual(1, len(closed))
        self.assertEqual(1, len(pos))

        self.assertEqual(closed[0][0], 'DAL')
        self.assertEqual(closed[0][1], 110*100+100*100-200*230)
        self.assertEqual(pos['DAL'], (300, -300*230))


class UltCommision(unittest.TestCase):
    def test_basic_commision(self):
        self.skipTest('not implemented')

    def test_min_commision(self):
        self.skipTest('not implemented')

class UltSlipage(unittest.TestCase):
    def test_slipage(self):
        self.skipTest('not implemented')

class UltTestRubostness(unittest.TestCase):
    def test_buy_0_shares(self):
        self.skipTest('not implemented')

    def test_sell_0_shares(self):
        self.skipTest('not implemented')

    def test_buy_negative_shares(self):
        self.skipTest('not implemented')

    def test_sell_negative_shares(self):
        self.skipTest('not implemented')


if __name__ == '__main__':
    unittest.main()



