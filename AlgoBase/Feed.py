__author__ = 'dkinsbur'


class Feed(object):

    def __init__(self):
        self._evt_on_data = []
        self._evt_on_end = []
        self.abrt = False

    def register(self, on_data, on_end):
        if on_data:
            self._evt_on_data.append(on_data)
        if on_end:
            self._evt_on_end.append(on_end)

    def _get_data_iterator(self):
        raise NotImplementedError

    def go(self):
        for data in self._get_data_iterator():
            for cb in self._evt_on_data:
                cb(self, data)

            if self.abrt:
                return

        for cb in self._evt_on_end:
            cb(self)

    def abort(self):
        self.abrt = True

from Bar import CsvBar, MergedBar

class CsvBarFeed(Feed):
    def __init__(self, path, first_line='date,high,low,open,close,volume', date_format='%Y-%m-%d-%H-%M'):
        super(CsvBarFeed, self).__init__()
        self.path = path
        self.date_format = date_format
        self.first_line = first_line

    def _get_data_iterator(self):
        with open(self.path) as self.csv:
            first_line = self.csv.readline()  # skip title line
            assert first_line.strip() == self.first_line, '{} <> {}'.format([first_line.strip()], [self.first_line])
            for line in self.csv:
                b = CsvBar(line, self.date_format)
                yield b

class MergeBarFeed(Feed):

    _merge_options = [
        5 # five minutes
    ]

    def __init__(self, base_feed, merge):
        if merge not in self._merge_options:
            raise ValueError()

        super(MergeBarFeed, self).__init__()
        self._base_feed = base_feed
        self._merge_amount = merge

    def _get_data_iterator(self):
        lst = []
        for bar in self._base_feed._get_data_iterator():
            import datetime
            if bar.get_time() > datetime.datetime(2017,4,21,19,0):
                print lst
                print bar

            if len(lst) == 0:
                lst.append(bar)

            #  1) check if time delta between prev bar and curr bar is less than merge amount
            #  2) check that both prev minutes and curr bar minute are in the same merge amount slot
            else:

                delta_minutes = (bar.get_time() - lst[-1].get_time()).total_seconds()/60
                less_than_merge = delta_minutes < self._merge_amount
                cur_slot = (bar.get_time().minute / self._merge_amount)
                prv_slot = (lst[-1].get_time().minute / self._merge_amount)
                if less_than_merge and (cur_slot == prv_slot):
                    lst.append(bar)

                else:
                    m = MergedBar(lst, round_mod=self._merge_amount)
                    if bar.get_time() > datetime.datetime(2017,4,21,19,0):
                        print '>>>>>', m
                    yield m
                    lst = [bar]

        if len(lst) > 0:
            yield MergedBar(lst, round_mod=self._merge_amount)


import unittest
class UltFeed(unittest.TestCase):

    class TestFeed(Feed):
        pass

    def test_feed_basic(self):

        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals = list(xrange(10))
        feed.ended = 0

        def on_data_cb(feed_obj, data):
            self.assertEqual(feed_obj.on_data_vals.pop(0), data)
            self.assertEqual(feed, feed_obj)

        def on_end_cb(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed_obj.ended += 1

        feed.register(on_data_cb, on_end_cb)
        feed.go()

        self.assertEquals(0, len(feed.on_data_vals))
        self.assertEquals(1, feed.ended)

    def test_feed_multiple_callbacks(self):
        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals1 = list(xrange(10))
        feed.on_data_vals2 = list(xrange(10))
        feed.ended1 = 0
        feed.ended2 = 0

        def on_data_cb1(feed_obj, data):
            self.assertEqual(feed.on_data_vals1.pop(0), data)
            self.assertEqual(feed, feed_obj)

        def on_data_cb2(feed_obj, data):
            self.assertEqual(feed.on_data_vals2.pop(0), data)
            self.assertEqual(feed, feed_obj)

        def on_end_cb1(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed.ended1 += 1

        def on_end_cb2(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed.ended2 += 1

        feed.register(on_data_cb1, on_end_cb1)
        feed.register(on_data_cb2, on_end_cb2)

        feed.go()
        self.assertEquals(0, len(feed.on_data_vals1))
        self.assertEquals(0, len(feed.on_data_vals2))
        self.assertEquals(1, feed.ended1)
        self.assertEquals(1, feed.ended2)

    def test_no_callback_on_register(self):
        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals = list(xrange(10))
        feed.ended = 0

        def on_data_cb(feed_obj, data):
            self.assertEqual(feed_obj.on_data_vals.pop(0), data)
            self.assertEqual(feed, feed_obj)

        def on_end_cb(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed_obj.ended += 1

        feed.register(on_data_cb, None)
        feed.register(None, on_end_cb)
        feed.go()

        self.assertEquals(0, len(feed.on_data_vals))
        self.assertEquals(1, feed.ended)

    def test_no_callback_in_list(self):

        def on_data_cb(feed_obj, data):
            self.assertEqual(feed_obj.on_data_vals.pop(0), data)
            self.assertEqual(feed, feed_obj)

        def on_end_cb(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed_obj.ended += 1

        # no end callbacks

        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals = list(xrange(10))
        feed.ended = 0

        feed.register(on_data_cb, None)
        feed.go()

        self.assertEquals(0, len(feed.on_data_vals))
        self.assertEquals(0, feed.ended)

        # no data callbacks

        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals = list(xrange(10))
        feed.ended = 0

        feed.register(None, on_end_cb)
        feed.go()

        self.assertEquals(10, len(feed.on_data_vals))
        self.assertEquals(1, feed.ended)

    def test_abort(self):
        def on_data_cb(feed_obj, data):
            self.assertEqual(feed_obj.on_data_vals.pop(0), data)
            self.assertEqual(feed, feed_obj)

            if data == 7:
                feed_obj.abort()

        def on_end_cb(feed_obj):
            self.assertEqual(feed, feed_obj)
            feed_obj.ended += 1

        feed = UltFeed.TestFeed()
        feed._get_data_iterator = lambda: xrange(10)

        feed.on_data_vals = list(xrange(10))
        feed.ended = 0

        feed.register(on_data_cb, on_end_cb)
        feed.go()

        self.assertEquals(2, len(feed.on_data_vals))
        self.assertEquals(0, feed.ended)


if __name__ == '__main__':
    unittest.main()
