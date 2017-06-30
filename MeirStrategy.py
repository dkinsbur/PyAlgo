from Analysis import *
from AlgoRepo.AlgoBase.Bar import Bar
from AlgoRepo.AlgoBase.Feed import CsvBarFeed

class MeirStrategy(object):
    def __init__(self, feed, broker, config): # yesterday_bar, bearish_threshold, correction_threshold, near_round_delta):

        self.filtered_triggers = []
        self.triggers = []
        self.feed = feed
        self.feed.register(self.on_bar, None)

        self.broker = broker

        self.bearish_threshold = config['BEARISH_THRESHOLD_PERCENT']
        self.yesterday_bar = config['YESTERDAY_BAR']
        self.correction_threshold = config['CORRECTION_THRESHOLD']
        self.near_round_delta = config['ROUND_DELTA']

        self.today_bar = None

        self.highs_trend = TrendBar(config['TREND_THRESHOLD'], 'get_high')
        self.lows_trend = TrendBar(config['TREND_THRESHOLD'], 'get_low')

        self._has_reached_round = False

    def on_bar(self, feed, bar):
        self.highs_trend.add(bar)
        self.lows_trend.add(bar)

        self.update_today_bar(bar)  # to simulate today's daily bar

        self.curr_bar = bar

        # self.update_has_reached()

        if self.trigger_check():
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            pl = ph = None
            try:
                pl = self.lows_trend.get_pivots()[-1]
                ph = self.highs_trend.get_pivots()[-1]
            except:
                pass
            print '----------------------', pl, ph
            self.triggers.append(bar)

            self.add_filtered_trigger(bar)

    def add_filtered_trigger(self, bar):
        ####### filtered_triggers - list with only new pivots #######
        new_pivot = False
        last_trigger = None
        last_pivot = None
        try:
            last_trigger = self.filtered_triggers[-1]
            last_pivot = self.lows_trend.get_pivots()[-1]
        except IndexError:
            pass

        # if there was no trigger before this is definitely a new one
        if last_trigger is None:
            new_pivot = True

        elif last_pivot is not None:
            if last_pivot.type == PIVOT_LOW and last_pivot.time > last_trigger.get_time():
                new_pivot = True
        else:
            assert False  # illegal case
        if new_pivot:
            self.filtered_triggers.append(bar)
            #################################################################

    def go(self):
        self.feed.go()

######################## TRIGGER FUNCTIONS #############################

    # stock is moving down
    # stock is correcting up
    # stock reached round/half price
    # stock moving back down

    def trigger_check(self):
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

    def trigger_has_reached_round(self):
        bar = self.get_curr_bar()
        high = bar.get_high()
        piv_above = self.next_pivot_above(high)
        piv_below = self.next_pivot_below(high)

        return self.in_pivot_range(piv_above, high) or self.in_pivot_range(piv_below, high)

    def trigger_is_correcting_up(self):

        # first check if we are in a up trend or if we just flipped down on this bar
        if self.highs_trend.get_trend() == TREND_UP or self.highs_trend.get_trend_flip():

            # find the previous local min pivot. if it doesn't exist this is not a corrections
            pivots = self.lows_trend.get_pivots()
            local_low = None
            try:
                if pivots[-1].type == PIVOT_LOW:
                    local_low = pivots[-1].price
                elif pivots[-2].type == PIVOT_LOW:
                    local_low = pivots[-2].price
            except IndexError:
                return False

            # compare prev min pivot to current high and check if the delta is passes expected threshold
            trend = self.highs_trend.get_trend()
            high = self.get_curr_bar().get_high()

            correction = high - local_low

            return correction > self.correction_threshold
        else:
            #if not up trend then this is not a correction
            return False

###################################################################################

    def next_pivot_above(self, price):
        round_price = int(price)
        half = round_price + 0.5

        if price <= half:
            return half

        return round_price + 1

    def next_pivot_below(self, price):
        # get round number above price
        round_price = int(price)
        if round_price < price:
            round_price += 1

        half = round_price - 0.5

        if price >= half:
            return half

        return round_price - 1

    def in_pivot_range(self, pivot, price):
        return abs(pivot - price) <= self.near_round_delta

    # def update_has_reached(self):
    #     bar = self.get_curr_bar()
    #     low_next_pivot = self.next_pivot_above(bar.get_low())
    #     in_range = self.in_pivot_range(low_next_pivot, bar.get_high())
    #     if not in_range:
    #         high_next_pivot = self.next_pivot_above(bar.get_high())
    #         if high_next_pivot != low_next_pivot:
    #             in_range = self.in_pivot_range(high_next_pivot, bar.get_high())
    #
    #     self._has_reached_round = in_range

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


    # ConvertFreestockCsvToMyCsv(r'C:\Users\dkinsbur\Desktop\gov_free_1.txt', r'.\Data\gov_csv_1.txt' )
    # exit()

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
    # high_trend = TrendBar(0.2, f, 'get_high')
    # low_trend = TrendBar(0.2, f, 'get_low')
    # f.go()
    # pivots = [('U', p) for p in high_trend.pivots] + [('D', p) for p in low_trend.pivots]
    # pivots.sort(key= lambda x: x[1][2])
    # for c, p in pivots:
    #     if (c == 'U' and p[0] == 'H') or \
    #             (c == 'D' and p[0] == 'L'):
    #         print '{} -- {}: {} [{}]'.format(c, *p)
    #
    # exit()

########### ALDR #################
    # config = {
    #     'YESTERDAY_BAR': Bar(datetime(2017, 6, 27, 16, 0),13.65,13.45,13.65,13.48,187700),
    #     'BEARISH_THRESHOLD_PERCENT' : -4,
    #     'CORRECTION_THRESHOLD': 0.15,
    #     'ROUND_DELTA': 0.03,
    #     'TREND_THRESHOLD': 0.05,
    # }
    # m = MeirStrategy(CsvBarFeed(r'C:\Users\dkinsbur\Desktop\ALDR_part.txt'), None, config)
    # m.go()


#############
    # config = {
    #     'YESTERDAY_BAR': Bar(datetime(2017, 6, 28, 16, 0),89.54,89.27, 89.39, 89.52, 49700),
    #     'BEARISH_THRESHOLD_PERCENT' : -4,
    #     'CORRECTION_THRESHOLD': 0.3,
    #     'ROUND_DELTA': 0.05,
    #     'TREND_THRESHOLD': 0.1,
    # }
    # m = MeirStrategy(CsvBarFeed(r'.\Data\gov_csv_1.txt'), None, config)
    # m.go()

  # config = {
  #       'YESTERDAY_BAR': Bar(datetime(2017, 6, 28, 16, 0),89.54,89.27, 89.39, 89.52, 49700),
  #       'BEARISH_THRESHOLD_PERCENT' : -4,
  #       'CORRECTION_THRESHOLD': 0.3,
  #       'ROUND_DELTA': 0.05,
  #       'TREND_THRESHOLD': 0.1,
  #   }
  #   m = MeirStrategy(CsvBarFeed(r'C:\Users\dkinsbur\Desktop\iphi_csv.txt'), None, config)
  #   m.go()
  #
    print '-' * 50

    for t in m.triggers:
        print t

    print '-' * 50

    for t in m.filtered_triggers:
        print t
