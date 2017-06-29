from AlgoRepo.AlgoBase.Bar import Bar
from AlgoRepo.AlgoBase.Feed import CsvBarFeed

class MeirStrategy(object):
    def __init__(self, feed, broker, yesterday_bar, bearish_threshold, correction_threshold, near_round_delta):
        self.feed = feed
        self.feed.register(self.on_bar, None)

        self.broker = broker

        self.bearish_threshold = bearish_threshold
        self.today_bar = None
        self.yesterday_bar = yesterday_bar
        self.correction_threshold = correction_threshold
        self.near_round_delta = near_round_delta

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
        is_bearish = self.is_bearish_today()
        correcting = self.is_correcting_up()
        reached_round = self.has_reached_round()
        moving_down = self.is_moving_back_down()
        print '[{}] bearish: {} | correct: {} | round: {} | move down: {}'.format(self.get_curr_bar().get_time(), is_bearish, correcting, reached_round, moving_down)
        return is_bearish and correcting and reached_round and moving_down



    def is_bearish_today(self):
        yesterday = self.get_yesterday_bar()
        yesterday_close = yesterday.get_close()
        bar = self.get_curr_bar()
        now_close = bar.get_close()
        change_price = (now_close - yesterday_close)
        change_percent = round(100*(change_price/yesterday_close), 2)

        return change_percent < self.bearish_threshold

    def is_moving_back_down(self):
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


    def has_reached_round(self):
        # bar = self.get_curr_bar()
        # high = bar.get_high()
        # frac = high - int(high) # get only fraction
        # if 0.45 <= frac <= 0.55 or frac <= 0.05 or frac >= 0.95:
        #     reached_round = True
        # else:
        #     reached_round = False

        return self._has_reached_round

    def is_correcting_up(self):

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

    # fs_path = r'C:\Users\dkinsbur\Desktop\ALDR_freestock.txt'
    # out_path = r'C:\Users\dkinsbur\Desktop\ALDR_csv.txt'
    # ConvertFreestockCsvToMyCsv(fs_path, out_path)
    # exit()

#2017-6-27-16-00,13.65,13.45,13.65,13.48,187700

    yesterday_bar = Bar(datetime(2017, 6, 27, 16, 0),13.65,13.45,13.65,13.48,187700)
    bearish_threshold = -3
    correction_threshold = 0.05
    m = MeirStrategy(CsvBarFeed(r'C:\Users\dkinsbur\Desktop\ALDR_part.txt'), None, yesterday_bar, bearish_threshold, correction_threshold, 0.05)
    m.go()