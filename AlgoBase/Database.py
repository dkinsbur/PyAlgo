import sqlite3
from sqlite3 import Error
from Bar import Bar
from datetime import datetime

CREATE_MIN_TABLE_IF_NOT_EXIST = """
CREATE TABLE IF NOT EXISTS {source}_MIN_BARS(
Symbol char(6) NOT NULL,
Date date NOT NULL,
Time time NOT NULL,
Open decimal(6,2) NOT NULL,
High decimal(6,2) NOT NULL,
Low  decimal(6,2) NOT NULL,
Close decimal(6,2) NOT NULL,
Volume int NOT NULL,
PRIMARY KEY (Symbol, Date, Time));"""

CREATE_DAY_TABLE_IF_NOT_EXIST = """
CREATE TABLE IF NOT EXISTS {source}_DAY_BARS(
Symbol char(6) NOT NULL,
Date date NOT NULL,
Open decimal(6,2) NOT NULL,
High decimal(6,2) NOT NULL,
Low  decimal(6,2) NOT NULL,
Close decimal(6,2) NOT NULL,
Volume int NOT NULL,
PRIMARY KEY (Symbol, Date));"""

INSERT_DAY_BAR = "INSERT INTO {source}_DAY_BARS VALUES (?,?,?,?,?,?,?);"
INSERT_MIN_BAR = "INSERT INTO {source}_MIN_BARS VALUES (?,?,?,?,?,?,?,?);"

SELECT_DAY_BAR = "SELECT * FROM {source}_DAY_BARS {condition};"
SELECT_MIN_BAR = "SELECT * FROM {source}_MIN_BARS {condition};"

class Database(object):

    def __init__(self, db_file, source):
        self.db_file = db_file
        self.source = source.upper()
        with self._connect() as conn:
            conn.execute(CREATE_DAY_TABLE_IF_NOT_EXIST.format(source=self.source))
            conn.execute(CREATE_MIN_TABLE_IF_NOT_EXIST.format(source=self.source))

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def _make_day_bar_select_command(self, symbol, start, end=None):
        if end:
            range_cond = "(Date >= '{start}' AND Date <= '{end}')".format(start=str(start.date()), end=str(end.date()))
        else:
            range_cond = "Date = '{start}'".format(start=str(start.date()))

        condition="WHERE Symbol='{symbol}' AND {range_cond}".format(symbol=symbol, range_cond=range_cond)
        return SELECT_DAY_BAR.format(condition=condition, source=self.source)

    def _make_min_bar_select_command(self, symbol, start, end=None):
        start_date = str(start.date())
        start_time = str(start.time())
        if end:
            end_date = str(end.date())
            end_time = str(end.time())
            range_cond = "((Date > '{start_date}' AND Date < '{end_date}') OR (Date = '{start_date}' AND Time >= '{start_time}') OR (Date = '{end_date}' AND Time <= '{end_time}'))".format(
                start_date=start_date,
                start_time=start_time,
                end_date=end_date,
                end_time=end_time)
        else:
            range_cond = "(Date = '{start_date}' AND Time = '{start_time}')".format(start_date=start_date, start_time=start_time)

        condition="WHERE Symbol='{symbol}' AND {range_cond}".format(symbol=symbol, range_cond=range_cond)

        return SELECT_MIN_BAR.format(condition=condition, source=self.source)

    def min_bars_get(self, symbol, start, end=None, pre_post_market=True):
        with self._connect() as conn:
            cur = conn.cursor()
            SQL = self._make_min_bar_select_command(symbol, start, end)
            print SQL
            cur.execute(SQL)
            return tuple(Bar(datetime.strptime(dt + ' ' + tm, '%Y-%m-%d %H:%M:%S'),h, l, o, c, v)
                         for sym, dt, tm, o, h, l, c, v in cur.fetchall())

    def min_bars_add(self, symbol, bars, overwrite=False):
        bs = ((symbol,
               str(bar.get_time().date()),
               str(bar.get_time().time()),
               bar.get_open(),
               bar.get_high(),
               bar.get_low(),
               bar.get_close(),
               bar.get_volume()) for bar in bars)

        with self._connect() as conn:
            conn.executemany(INSERT_MIN_BAR.format(source=self.source), bs)

    def day_bars_get(self, symbol, start, end=None):
        with self._connect() as conn:
            cur = conn.cursor()
            SQL = self._make_day_bar_select_command(symbol, start, end)
            print SQL
            cur.execute(SQL)
            return tuple(Bar(datetime.strptime(dt, '%Y-%m-%d'),h, l, o, c, v)
                             for sym, dt, o, h, l, c, v in cur.fetchall())

    def day_bars_add(self, symbol, bars, overwrite=False):
        bs = ((symbol,
               str(bar.get_time().date()),
               bar.get_open(),
               bar.get_high(),
               bar.get_low(),
               bar.get_close(),
               bar.get_volume()) for bar in bars)

        with self._connect() as conn:
            conn.executemany(INSERT_DAY_BAR.format(source=self.source), bs)


if __name__ == '__main__':

    db_file = r"C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\data.db"
    # from datetime import date, time,datetime

    # create_connection("C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\data.db")
    # bars = []
    # with open(r'C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\uwt_day.txt') as f:
    #     f.readline()
    #     for line in f:
    #         d, h, l, o, c, v = line.strip().split(',')
    #         h = float(h)
    #         l = float(l)
    #         o = float(o)
    #         c = float(c)
    #         v = int(v)
    #
    #         dt = datetime.strptime(d, '%Y/%m/%d')
    #         # dt = datetime.strptime(d, '%Y/%m/%d %H:%M')
    #         bars.append(Bar(dt, h, l, o, c, v))
    #
    #         # d, t = d.split()
    #         # y, m, d = d.split('/')
    #         # hr, mn = t.split(':')
    #         #
    #         # d = date(int(y), int(m), int(d))
    #         # t = time(hour=int(hr), minute=int(mn))
    #         # data.append(('UWT', str(d), str(t), o, h, l, c, v))

    # db = Database()
    # # db.add_minute_bars('UWT', bars)
    # bars = db.get_minute_bars('UWT', time_range=(datetime(1000, 1, 1, 9, 30).time(),))#,(datetime(2017, 4, 19).date(), datetime(2017, 4, 19).date()))
    # print len(bars)
    # for b in bars:
    #     print b

    # db = Database(db_file)
    # db2 = Database(db_file)

    db = Database(db_file, 'google')
    # db.day_bars_add('UWT', bars)
    # db.min_bars_add('UWT', bars)
    # from datetime import timedelta
    bars = db.day_bars_get('UWT', start=datetime(year=2017, month=4, day=19), end=datetime(year=2017, month=4, day=21))
    # bars = db.min_bars_get('UWT', start=datetime(year=2017, month=4, day=19, hour=9, minute=59), end=datetime(year=2017, month=4, day=21))
    for x in bars:
        print x

    print len(bars)



# minute bars


import unittest
class UltDatabase(unittest.TestCase):
    pass