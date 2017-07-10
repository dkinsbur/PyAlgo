import sqlite3
from sqlite3 import Error
from Bar import Bar
from datetime import datetime

CREATE_TABLE_IF_NOT_EXIST = """
CREATE TABLE IF NOT EXISTS MINUTE_BARS(
Symbol char(6) NOT NULL,
Date date NOT NULL,
Time time NOT NULL,
Open decimal(6,2) NOT NULL,
High decimal(6,2) NOT NULL,
Low  decimal(6,2) NOT NULL,
Close decimal(6,2) NOT NULL,
Volume int NOT NULL,
PRIMARY KEY (Symbol, Date, Time));"""

class Database(object):
    def __init__(self, db_file):
        self.db_file = db_file
        with self._connect() as conn:
            conn.execute(CREATE_TABLE_IF_NOT_EXIST)

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def add_minute_bars(self, symbol, bars):

        bs = [(symbol,
               str(bar.get_time().date()),
               str(bar.get_time().time()),
               bar.get_open(),
               bar.get_high(),
               bar.get_low(),
               bar.get_close(),
               bar.get_volume()) for bar in bars]

        with self._connect() as conn:
            conn.executemany("INSERT INTO MINUTE_BARS VALUES (?,?,?,?,?,?,?,?);", bs)

    def get_minute_bars(self, symbol, date_range=None, time_range=None):
        with self._connect() as conn:
            cur = conn.cursor()
            where_time = where_date = ''

            if time_range is not None:
                if len(time_range) == 1:
                    where_date = "AND '{}' = Time".format(str(time_range[0]))
                else:
                    where_date = "AND ('{}' <= Time AND Time <= '{}')".format(str(time_range[0]), str(time_range[1]))

            if date_range is not None:
                if len(date_range) == 1:
                    where_date = "AND '{}' = Date".format(str(date_range[0]))
                else:
                    where_date = "AND ('{}' <= Date AND DATE <= '{}')".format(str(date_range[0]), str(date_range[1]))

            SQL = "SELECT * FROM MINUTE_BARS WHERE Symbol = '%s' %s %s;" % (symbol, where_date, where_time)
            print SQL
            cur.execute(SQL)

            return cur.fetchall()

if __name__ == '__main__':
    # from datetime import date, time,datetime

    # create_connection("C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\data.db")
    # bars = []
    # with open(r'C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\uwt.txt') as f:
    #     f.readline()
    #     for line in f:
    #         d, h, l, o, c, v = line.strip().split(',')
    #         h = float(h)
    #         l = float(l)
    #         o = float(o)
    #         c = float(c)
    #         v = int(v)
    #
    #         dt = datetime.strptime(d, '%Y/%m/%d %H:%M')
    #         bars.append(Bar(dt, h, l, o, c, v))
    #
    #         d, t = d.split()
    #         y, m, d = d.split('/')
    #         hr, mn = t.split(':')
    #
    #         d = date(int(y), int(m), int(d))
    #         t = time(hour=int(hr), minute=int(mn))
    #         # data.append(('UWT', str(d), str(t), o, h, l, c, v))

    # db = Database(r"C:\Users\dkinsbur\Documents\Work\pythonProjects\AlgoTrade\AlgoRepo\Data\data.db")
    # # db.add_minute_bars('UWT', bars)
    # bars = db.get_minute_bars('UWT', time_range=(datetime(1000, 1, 1, 9, 30).time(),))#,(datetime(2017, 4, 19).date(), datetime(2017, 4, 19).date()))
    # print len(bars)
    # for b in bars:
    #     print b

    pass