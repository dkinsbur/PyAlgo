__author__ = 'dkinsbur'

from datetime import datetime, timedelta
from AlgoBase.Feed import *
from AlgoBase.Broker import Broker
def load_oil_reports(path):

    oil_reports = []

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
            oil_reports.append({'DATE':date, 'ACTUAL':actual, 'FORCAST':forcast, 'TRIGGER': 'UWT' if color == 'greenFont' else 'DWT'})

    return oil_reports



ST_NONE = 0
ST_ENTER_TRIGGER_ARMED = 1
ST_ENTER_TRIGGER_FIRED = 2
ST_EXIT_TRIGGER = 3


import random
class CrudeOilStrategy(object):

    def __init__(self, oil_reports, feed_bars_5min, broker, stocks, advance_stop=False, log=True):
        self.feed = feed_bars_5min
        self.reports = oil_reports
        self.feed.register(self.on_5min_bar, None)
        self.curr_report = None
        self.first_bar = None
        self.log = log

        self.stocks = stocks
        self.advance_stop = advance_stop

        self.broker = broker
        broker.log = enable_log
        self.state = ST_NONE

        self.prev_bal = broker.get_ballance()

        self.no_trigger = 0

    def on_5min_bar(self, feed, bars):

        if self.state == ST_NONE:
            if len(self.reports) == 0:
                if self.log:
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
            if self.log:
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

                if self.log:
                    print '!!! Day ended with NO trigger !!!'
                self.no_trigger += 1

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
            if self.log:
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


    stocks = 300
    enable_log = False
    random_remove = True
    results = []
    for i in range(1):

        for advance_stop in [False, True]:

            reports = load_oil_reports(CRUDE_OI_REPORT_PATH)
            reports.sort(key=lambda x:x['DATE'])
            # uwt_feed = CsvBarFeed(UWT_MIN_PATH, first_line=CSV_FRST_LINE,date_format=CSV_DATE_FORMAT)
            # dwt_feed = CsvBarFeed(DWT_MIN_PATH, first_line=CSV_FRST_LINE,date_format=CSV_DATE_FORMAT)
            uwt_feed = FiveMinBarFeed(UWT_MIN_PATH)
            dwt_feed = FiveMinBarFeed(DWT_MIN_PATH)
            feed = DuplicateBarFeed(uwt_feed, dwt_feed)
            strategy = CrudeOilStrategy(reports, feed, Broker(10000, 0.20), stocks, advance_stop, log=enable_log)
            strategy.go()

            loss_count = 0
            profit_count = 0
            adj_loss_count = 0
            adj_profit_count = 0
            max_loss = 0
            max_profit = 0
            sum_loss = 0
            sum_profit = 0

            curr_adj_loss = 0
            curr_adj_prof = 0

            for pos in strategy.broker.get_closed_positions():
                if pos[1] > 0:
                    profit_count += 1
                    max_profit = max(pos[1], max_profit)
                    sum_profit += pos[1]

                    curr_adj_prof += 1
                    curr_adj_loss = 0
                    adj_profit_count = max(adj_profit_count, curr_adj_prof)

                else:
                    loss_count += 1
                    max_loss = min( pos[1], max_loss)
                    sum_loss += pos[1]

                    curr_adj_loss += 1
                    curr_adj_prof = 0
                    adj_loss_count = max(adj_loss_count, curr_adj_loss)
            from tabulate import tabulate

            avg_profit = 0 if profit_count == 0 else round(sum_profit/profit_count, 2)
            avg_loss = 0 if loss_count == 0 else round(sum_loss/loss_count, 2)

            table = [['Total Days', strategy.no_trigger + profit_count+ loss_count],
                     ['Days with no trigger', strategy.no_trigger],
                     ['profit/loss ratio', -round(avg_profit/avg_loss,2)],
                     ['stocks traded', stocks],
                     ['advance stop', advance_stop],
                     ['total profit', sum_profit+sum_loss],
                     ]
            print tabulate(table, tablefmt='grid')

            header = ['', 'profit', 'loss']
            table = [
                ['max', max_profit, max_loss],
                ['avg', avg_profit, avg_loss],
                ['%', 100*round(profit_count/float(profit_count+loss_count+strategy.no_trigger),2), 100*round(loss_count/float(profit_count+loss_count+strategy.no_trigger), 2)],
                ['sum', sum_profit, sum_loss],
                ['count', profit_count, loss_count],
                ['adj', adj_profit_count, adj_loss_count],
            ]
            print tabulate(table, header, tablefmt='grid')

            results.append((sum_profit+sum_loss, advance_stop))

            for i in range(20):
                positions = list(strategy.broker.get_closed_positions())
                to_drop = len(positions)/2
                while to_drop > 0:
                    pos = positions.pop(random.randint(0, len(positions)-1))
                    to_drop -= 1
                    print 'Dropping:', pos

                s = sum(pos[1] for pos in positions)
                print s, float(s)/len(positions)









