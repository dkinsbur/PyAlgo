__author__ = 'dkinsbur'

from AlgoBase.Broker import Broker

ST_WAIT_FOR_CORRECTION = 'ST_WAIT_FOR_CORRECTION'
ST_FIND_STOP = 'ST_FIND_STOP'
ST_WAIT_ENTRANCE = 'ST_WAIT_ENTRANCE'
ST_ENTERED = 'ST_ENTERED'
ST_FIND_EXIT = 'ST_FIND_EXIT'
ST_EXITED = 'ST_EXITED'

ST_DONE = 0

MIN_CORRECTION = 0

MARKET = 1
LIMIT = 2
STOP_MARKET = 3
STOP_LIMIT = 4

BUY = 1
SELL = 2
from collections import namedtuple
Order = namedtuple('Order', ('type', 'operation', 'price', 'trigger', 'amount'))

class NesiMomentumStrategy(object):
    def __init__(self, bar_feed):
        self.feed = bar_feed
        self.feed.register(self.on_bar, None)
        self.state = None
        self.high_of_day = -1
        self.broker = Broker(10000)
        self.orders = []

    def stop_market(self, operation, trigger_price, amount):

        assert operation in [BUY, SELL]

        order = Order(type=STOP_MARKET, operation=operation, price=0, trigger=trigger_price, amount=amount)
        print order
        self.orders.append(order)

        return order

    def change_state(self, new_state):
        self.state = new_state
        print '--> {}'.format(new_state)

        if self.state == ST_ENTERED:
            # TODO: check corner case where bar triggers buy and immediatly triggers sell
            self.stop_market(SELL, 0, self.trigger_bar.get_low(), 1000)


    def handle_orders(self, bar):
        new_orders = []
        while len(self.orders) > 0:
            order = self.orders.pop(0)
            if order.type == STOP_MARKET:
                if order.operation == BUY:
                    if bar.get_high() >= order.trigger:
                        print '>>> BUY {} {}'.format(order.trigger, order.amount)
                        if self.state == ST_WAIT_ENTRANCE:
                            self.change_state(ST_ENTERED)

                    else:
                        new_orders.append(order)
                else: # SELL
                    if bar.get_low() <= order.trigger:
                        print '>>> SELL {} {}'.format(order.trigger, order.amount)

                        if self.state == ST_ENTERED:
                            self.change_state(ST_WAIT_FOR_CORRECTION)

                    else:
                        new_orders.append(order)

            else:
                raise NotImplementedError()

        self.orders = new_orders



    def on_bar(self, feed, bar):

        # print bar
        self.handle_orders(bar)

        self.high_of_day = max(self.high_of_day, bar.get_high())

        if self.state == ST_WAIT_FOR_CORRECTION:
            if bar.get_high() < self.high_of_day - MIN_CORRECTION:
                self.change_state(ST_FIND_STOP)
                self.curr_low = bar.get_low()
                print '[high_of_day:{}]'.format(self.high_of_day)


        elif self.state == ST_FIND_STOP:
            bar_low = bar.get_low()
            if bar_low < self.curr_low:
                self.curr_low = bar_low
            else:
                self.trigger_bar = bar
                self.change_state(ST_WAIT_ENTRANCE)
                print '[trigger_bar:{}]'.format(bar)
                self.stop_market(BUY, bar.get_high(), 1000)

        elif self.state == ST_WAIT_ENTRANCE:
            pass

        elif self.state == ST_ENTERED:
            self.enter_bar = bar
            self.change_state(ST_FIND_EXIT)

        elif self.state == ST_FIND_EXIT:
            pass


        else:
            raise NotImplementedError()







    def go(self):
        self.change_state(ST_WAIT_FOR_CORRECTION)
        self.feed.go()

from AlgoBase.Feed import CsvBarFeed
if __name__ == '__main__':

   strategy = NesiMomentumStrategy(CsvBarFeed('pirs_min.txt'))

   strategy.go()



