import Queue as Q
import threading as T
import time
import random

####################### BASE ################################
class Algo(T.Thread):

    def __init__(self):
        super(Algo, self).__init__(target=self._worker)
        self.queue = Q.PriorityQueue()

    def push_event(self, event):
        assert issubclass(event.__class__, Event)
        self.queue.put(event)

    def _worker(self):
        """Example:
        while True:
            event = self.q.get()
            cls = event.__class__
            print '<--', event
            if cls == ExitEvent:
                break
            time.sleep(0.05)"""

        raise NotImplementedError()


class Event(object):
    def __init__(self, sender, args=None, priority=0):
        self.sender = sender
        self.args = args
        self.priority = priority
        # print self.__class__.__name__, priority

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    def __str__(self):
        return '[{cls}] pri={pri} | args={args}'.format(cls=self.__class__.__name__, pri=self.priority, args=self.args)

class EventSupplier(T.Thread):

    def __init__(self, algo):
        super(EventSupplier, self).__init__(target=self._worker)
        self.algo = algo
        self._kill= False

    def kill(self):
        if self.isAlive():
            self._kill = True
            print 'KILLLLLLL', self.__class__.__name__

    def _worker(self):
        raise NotImplementedError()

########################################################################

class RandomNumberEventSupplier(EventSupplier):
    def __init__(self, algo):
        super(RandomNumberEventSupplier, self).__init__(algo)

    def _worker(self):
        for i in xrange(10):
            self.algo.push_event(Event(self, args=random.randint(1, 100)))
            if self._kill:
                return
            time.sleep(0.5)

class BarEvent(Event):
    pass

class ExitEvent(Event):
    pass

class CsvBarEventSupplier(EventSupplier):
    def __init__(self, algo, csv_file, delay=0):
        super(CsvBarEventSupplier, self).__init__(algo)
        self.csv_file = csv_file

    def _worker(self):
        with open(self.csv_file) as f:
            f.readline() # skip first
            for line in f:
                self.algo.push_event(BarEvent(self, line.split(','), priority=1))
                if self._kill:
                    return
                time.sleep(0.02)

def EXIT(priority):
    return ExitEvent(None, priority=priority)

class ExitOnSupplierDoneEventSupplier(EventSupplier):
    def __init__(self, algo, suppliers):
        super(ExitOnSupplierDoneEventSupplier, self).__init__(algo)
        self.suppilers = suppliers

    def _worker(self):
        for sup in self.suppilers:
            if sup is self:
                continue
            sup.join()
            print 'ExitOnSupplierDoneEventSupplier: joined', sup.__class__.__name__
        print 'ExitOnSupplierDoneEventSupplier pushing EXIT'
        self.algo.push_event(ExitEvent(self))

class MyAlgo(Algo):

    def push_event(self, event):
        print 'PUT -->', event
        super(MyAlgo, self).push_event(event)

    def _worker(self):
        self._worker_pre()
        while True:
            event = self.queue.get()
            print 'GET <--', event
            cls = event.__class__

            if cls == ExitEvent:
                break

        self._worker_post()

    def _worker_pre(self):
        self.suppliers = []
        self.suppliers.append(RandomNumberEventSupplier(algo))
        self.suppliers.append(CsvBarEventSupplier(algo, 'DB_DAY_DWT.txt'))

        self.suppliers.append(ExitOnSupplierDoneEventSupplier(algo, self.suppliers))
        for sup in self.suppliers:
            sup.start()

    def _worker_post(self):
        for sup in self.suppliers:
            sup.kill()
        for sup in self.suppliers:
            sup.join()


algo = MyAlgo()
algo.start()
time.sleep(1)
algo.push_event(EXIT(5))
algo.join()


