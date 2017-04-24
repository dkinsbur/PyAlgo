__author__ = 'dkinsbur'

from datetime import datetime, timedelta
from AlgoRepo.AlgoBase.Feed import *

def load_oil_reports(path):

    reports = []

    with open(path) as f:
        f.readline()  # read first line
        for line in f:
            dt, tm, color, actual, forcast, prev = line.split('|')
            date = datetime.strptime(dt + tm, '%b %d, %Y %H:%M')
            actual = float(actual.strip().strip('M'))
            forcast = float(forcast.strip().strip('M'))
            prev = float(prev.strip().strip('M'))
            actual_more_than_forcast = actual > forcast
            assert (actual_more_than_forcast and color == 'redFont') or (
            (not actual_more_than_forcast) and color == 'greenFont')
            reports.append({'DATE':date, 'ACTUAL':actual, 'FORCAST':forcast, 'TRIGGER': 'UWT' if color == 'greenFont' else 'DWT'})

    return reports

class Broker(object):

    def __init__(self, balance, slipage):
        self.slipage = slipage
        self.balance = balance

    def buy(self, symbol, amount, price, time=None):
        tm_str = '' if not time else '[{}]'.format(time)
        print '{}BUY {} {} {}'.format(tm_str, symbol, amount, price + self.slipage)
        self.balance -= amount * price

    def sell(self, symbol, amount, price, time=None):
        tm_str = '' if not time else '[{}]'.format(time)
        print '{}SELL {} {} {}'.format(tm_str, symbol, amount, price - self.slipage)
        self.balance += amount * price

    def get_ballance(self):
        return self.balance



ST_NONE = 0
ST_ENTER_TRIGGER_ARMED = 1
ST_ENTER_TRIGGER_FIRED = 2
ST_EXIT_TRIGGER = 3



class CrudeOilStrategy(object):

    def __init__(self, oil_reports, feed_bars_5min, broker, stocks, advance_stop=False):
        self.feed = feed_bars_5min
        self.reports = oil_reports
        self.feed.register(self.on_5min_bar, None)
        self.curr_report = None
        self.first_bar = None

        self.stocks = stocks
        self.advance_stop = advance_stop

        self.broker = broker
        self.state = ST_NONE

        self.prev_bal = broker.get_ballance()


    def on_5min_bar(self, feed, bars):

        if self.state == ST_NONE:
            if len(self.reports) == 0:
                print '+'*50
                print 'no more oil reports'
                feed.abort()
                return

            rep = self.reports[0]
            if rep['TRIGGER'] == 'UWT':
                bar = bars[0]
            else:
                bar = bars[1]

            if not bar or rep['DATE'] > bar.get_time():
                return

            self.curr_report = self.reports.pop(0)
            self.trigger_price = bar.get_high() + 0.01
            self.stop = (bar.get_low() + (bar.get_high() - bar.get_low())/2) - 0.01
            date = self.curr_report['DATE']
            self.end_of_day = datetime(date.year, date.month, date.day, hour=16, minute=0)

            self.state = ST_ENTER_TRIGGER_ARMED

            print '-'*50
            print 'Report:', self.curr_report
            print 'Trigger: {}   Stop: {}   Risk: {}'.format(self.trigger_price, self.stop, self.trigger_price - self.stop)

        elif self.state == ST_ENTER_TRIGGER_ARMED:
            if self.curr_report['TRIGGER'] == 'UWT':
                bar = bars[0]
            else:
                bar = bars[1]

            if not bar:
                return

            if bar.get_time() > self.end_of_day:
                self.state = ST_NONE

                print '!!! Day ended with NO trigger !!!'

            if bar.get_high() >= self.trigger_price:
                self.broker.buy(self.curr_report['TRIGGER'], self.stocks, self.trigger_price,time=bar.get_time())
                self.state = ST_ENTER_TRIGGER_FIRED

        elif self.state == ST_ENTER_TRIGGER_FIRED:
            if self.curr_report['TRIGGER'] == 'UWT':
                bar = bars[0]
            else:
                bar = bars[1]

            if not bar:
                return

            if self.end_of_day - bar.get_time() <= timedelta(minutes=5):
                self.broker.sell(self.curr_report['TRIGGER'], self.stocks, bar.get_close(), time=bar.get_time())
                self.state = ST_EXIT_TRIGGER

            elif bar.get_low() <= self.stop:
                self.broker.sell(self.curr_report['TRIGGER'], self.stocks, self.stop, time=bar.get_time())
                self.state = ST_EXIT_TRIGGER

            if self.advance_stop:
                self.stop = max(bar.get_low(), self.stop)

        elif self.state == ST_EXIT_TRIGGER:
            bal = self.broker.get_ballance()
            delta = bal - self.prev_bal
            self.prev_bal = bal
            print 'Ballance: {} [{}]'.format(bal, delta)
            self.state = ST_NONE

        else:
            raise Exception()



    def go(self):
        self.feed.go()

def FiveMinBarFeed(path):
    return MergeBarFeed(CsvBarFeed(path, first_line=CSV_FRST_LINE,date_format=CSV_DATE_FORMAT), 5)

if __name__ == '__main__':
    UWT_MIN_PATH = r'Data\UWT.txt'
    DWT_MIN_PATH = r'Data\DWT.txt'
    UWT_DAY_PATH = r'Data\UWT_DAY.txt'
    DWT_DAY_PATH = r'Data\DWT_DAY.txt'
    CRUDE_OI_REPORT_PATH = r'Data\Crude_Oil_Report.txt'
    CSV_FRST_LINE = 'date,hi,lo,open,close,volume'
    CSV_DATE_FORMAT = '%Y/%m/%d %H:%M'

    reports = load_oil_reports(CRUDE_OI_REPORT_PATH)
    reports.sort(key=lambda x:x['DATE'])
    uwt_feed = FiveMinBarFeed(UWT_MIN_PATH)
    dwt_feed = FiveMinBarFeed(DWT_MIN_PATH)


    strategy = CrudeOilStrategy(reports, DuplicateBarFeed(uwt_feed, dwt_feed), Broker(10000, 0.05), 200, False)
    strategy.go()







