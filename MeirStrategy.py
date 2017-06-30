from AlgoRepo.AlgoBase.Bar import Bar
from AlgoRepo.AlgoBase.Feed import CsvBarFeed

class MeirStrategy(object):
    def __init__(self, feed, broker, config): # yesterday_bar, bearish_threshold, correction_threshold, near_round_delta):

        self.feed = feed
        self.feed.register(self.on_bar, None)

        self.broker = broker
# config = {
#         'YESTERDAY_BAR': Bar(datetime(2017, 6, 27, 16, 0),13.65,13.45,13.65,13.48,187700),
#         'BEARISH_THRESHOLD_PERCENT' : -3,
#         'CORRECTION_THRESHOLD': 0.05,
#         'ROUND_DELTA': 0.05
#     }
        self.bearish_threshold = config['BEARISH_THRESHOLD_PERCENT']
        self.yesterday_bar = config['YESTERDAY_BAR']
        self.correction_threshold = config['CORRECTION_THRESHOLD']
        self.near_round_delta = config['ROUND_DELTA']

        self.today_bar = None

        self._has_reached_round = False

    def on_bar(self, feed, bar):
        self.update_today_bar(bar)  # to simulate today's daily bar
        self.curr_bar = bar
        self.update_has_reached()

        if self.check_trigger():
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'



    def go(self):
        self.feed.go()

    # stock is moving down
    # stock is correcting up
    # stock reached round/half price
    # stock moving back down
    def check_trigger(self):
        is_bearish = self.trigger_is_bearish_today()
        correcting = self.trigger_is_correcting_up()
        reached_round = self.trigger_has_reached_round()
        moving_down = self.trigger_is_moving_back_down()

        print '[{}] bearish: {} | correct: {} | round: {} | move down: {}'.format(self.get_curr_bar().get_time(), is_bearish, correcting, reached_round, moving_down)
        return is_bearish and correcting and reached_round and moving_down

    def trigger_is_bearish_today(self):
        yesterday = self.get_yesterday_bar()
        yesterday_close = yesterday.get_close()
        bar = self.get_curr_bar()
        now_close = bar.get_close()
        change_price = (now_close - yesterday_close)
        change_percent = round(100*(change_price/yesterday_close), 2)

        return change_percent < self.bearish_threshold

    def trigger_is_moving_back_down(self):
        bar = self.get_curr_bar()
        is_bearish_bar = (bar.get_close() - bar.get_open()) < 0
        return is_bearish_bar

    def next_pivot_above(self, price):
        round_price = int(price)
        half = round_price + 0.5

        if price <= half:
            return half

        return round_price + 1

    def in_pivot_range(self, pivot, price):
        return abs(pivot - price) <= self.near_round_delta

    def update_has_reached(self):
        bar = self.get_curr_bar()
        open_next_pivot = self.next_pivot_above(bar.get_open())
        in_range = self.in_pivot_range(open_next_pivot, bar.get_high())
        if not in_range:
            high_next_pivot = self.next_pivot_above(bar.get_high())
            if high_next_pivot != open_next_pivot:
                in_range = self.in_pivot_range(high_next_pivot, bar.get_high())

        self._has_reached_round = in_range

    def trigger_has_reached_round(self):
        # bar = self.get_curr_bar()
        # high = bar.get_high()
        # frac = high - int(high) # get only fraction
        # if 0.45 <= frac <= 0.55 or frac <= 0.05 or frac >= 0.95:
        #     reached_round = True
        # else:
        #     reached_round = False

        return self._has_reached_round

    def trigger_is_correcting_up(self):

        bar = self.get_curr_bar()
        toady = self.get_today_bar()
        correction = bar.get_close() - toady.get_low()
        assert correction >= 0, str('{},{},{}'.format(bar.get_time(), bar.get_close(), toady.get_low()))
        return correction > self.correction_threshold

    def get_yesterday_close(self):
        return self.get_yesterday_bar().get_close()

    def get_curr_bar(self):
        return self.curr_bar

    def get_yesterday_bar(self):
        return self.yesterday_bar

    def get_today_bar(self):
        return self.today_bar

    def update_today_bar(self, bar):
        if self.today_bar is None:
            self.today_bar = bar
            return
        today = self.today_bar
        self.today_bar = Bar(today.get_time(),
                          max(today.get_high(), bar.get_high()),
                          min(today.get_low(), bar.get_low()),
                          today.get_open(),
                          bar.get_close(),
                          today.get_volume() + bar.get_volume())


def FreestockTimeToMyCsvTime(fs_time):
    fs_time = fs_time.strip()
    date, time, am_pm = fs_time.split()
    h, m, s = time.split(':')
    mn, dt, yr = date.split('/')

    if am_pm == 'PM' and h.strip() != '12':
        h = str(int(h) + 12)

    return '{year}-{month}-{day}-{hour}-{min}'.format(year=yr, month=mn, day=dt, hour=h, min=m)

def ConvertFreestockCsvToMyCsv(fs_path, out_path):
    with open(out_path, 'w') as out_fl:
        out_fl.write('date,high,low,open,close,volume\n')
        with open(fs_path) as in_fl:
            assert in_fl.readline().strip() == 'Date,Open,High,Low,Close,Volume'
            for line in in_fl:
                Date, Open, High, Low, Close, Volume = line.strip().split(',')
                Date = FreestockTimeToMyCsvTime(Date)
                out_fl.write('{},{},{},{},{},{}\n'.format(Date, High, Low, Open, Close, Volume))


if __name__ == '__main__':

    from datetime import datetime

    # time = datetime.strptime('6/26/2017 2:11:00 PM', '%m/%d/%Y %H:%M:00 %p')
    # print time
    # time = datetime.strptime('6/27/2017 9:40:00 AM', '%m/%d/%Y %H:%M:00 %p')
    # print time
    # print FreestockTimeToMyCsvTime('6/26/2017 2:11:00 PM')
    # print FreestockTimeToMyCsvTime('6/27/2017 9:40:00 AM')
    # print datetime.strptime(FreestockTimeToMyCsvTime('6/26/2017 2:11:00 PM'), '%Y-%m-%d-%H-%M')
    # print datetime.strptime(FreestockTimeToMyCsvTime('6/27/2017 9:40:00 AM'), '%Y-%m-%d-%H-%M')

    # fs_path = r'C:\Users\dkinsbur\Desktop\iphi_free.txt'
    # out_path = r'C:\Users\dkinsbur\Desktop\iphi_csv.txt'
    # ConvertFreestockCsvToMyCsv(fs_path, out_path)
    # exit()

#2017-6-27-16-00,13.65,13.45,13.65,13.48,187700


    from Analysis import *

    # def on_bar(feed, bar):
    #     feed.low_trend.add((bar.get_low(), bar.get_time()))
    #     feed.high_trend.add((bar.get_high(), bar.get_time()))
    #
    # f = CsvBarFeed(r'C:\Users\dkinsbur\Desktop\iphi_csv.txt')
    # f.high_trend = Trend(0.2)
    # f.low_trend = Trend(0.2)
    # f.register(on_bar)
    # f.go()
    #
    # pivots = [('U', p) for p in f.high_trend.pivots] + [('D', p) for p in f.low_trend.pivots]
    # pivots.sort(key= lambda x: x[1][2])
    # for c, p in pivots:
    #     if (c == 'U' and p[0] == 'H') or \
    #             (c == 'D' and p[0] == 'L'):
    #         print '{} -- {}: {} [{}]'.format(c, *p)


    # f = CsvBarFeed(r'C:\Users\dkinsbur\Desktop\iphi_csv.txt')
    # high_trend = TrendFeed(0.2, f, 'get_high')
    # low_trend = TrendFeed(0.2, f, 'get_low')
    # f.go()
    # pivots = [('U', p) for p in high_trend.pivots] + [('D', p) for p in low_trend.pivots]
    # pivots.sort(key= lambda x: x[1][2])
    # for c, p in pivots:
    #     if (c == 'U' and p[0] == 'H') or \
    #             (c == 'D' and p[0] == 'L'):
    #         print '{} -- {}: {} [{}]'.format(c, *p)
    #
    # exit()

    config = {
        'YESTERDAY_BAR': Bar(datetime(2017, 6, 27, 16, 0),13.65,13.45,13.65,13.48,187700),
        'BEARISH_THRESHOLD_PERCENT' : -3,
        'CORRECTION_THRESHOLD': 0.05,
        'ROUND_DELTA': 0.05
    }


    m = MeirStrategy(CsvBarFeed(r'C:\Users\dkinsbur\Desktop\ALDR_part.txt'), None, config)
    #m = MeirStrategy(CsvBarFeed(r'C:\Users\dkinsbur\Desktop\iphi_csv.txt'), None, config)
    m.go()