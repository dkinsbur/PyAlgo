from tzlocal import get_localzone
from AlgoRepo.AlgoBase.Bar import Bar
import random
from ib.ext.Contract import Contract
import time
from datetime import datetime, timedelta
from threading import Semaphore
from ib.ext.EWrapper import EWrapper
from ib.ext.EClientSocket import EClientSocket
import logging
import pytz

TZ_LOCAL = get_localzone()
TZ_NY = pytz.timezone('US/Eastern')

DataRequests = {}

DATA_REQ_BAR_DAY = 1
DATA_REQ_BAR_MINUTE = 2

DATA_REQ_TYPES = (DATA_REQ_BAR_DAY, DATA_REQ_BAR_MINUTE)

def make_logger(obj):
    logger = logging.getLogger(obj.__class__.__name__)
    if not logger.handlers:
        hndlr = logging.StreamHandler()
        hndlr.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
        logger.addHandler(hndlr)
    return logger

class DataRequest(object):

    def __init__(self, req_type):
        self.sema = Semaphore(0)
        self.type = req_type
        assert req_type in DATA_REQ_TYPES
        self.logger = make_logger(self)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

        if req_type in (DATA_REQ_BAR_DAY, DATA_REQ_BAR_MINUTE):
            self.bars = []

    def wait(self):
        self.logger.error('--> wait() | {}'.format(self))
        self.sema.acquire()
        self.logger.error('<-- wait() | {}'.format(self))

    def done(self):
        self.logger.error('done(): {}'.format(self))
        self.sema.release()




class ReferenceWrapper(EWrapper):

    def showmessage(self, message, mapping):

        try:
            del(mapping['self'])
        except (KeyError, ):
            pass
        items = list(mapping.items())
        items.sort()
        self.logger.error(('### %s' % (message, )))
        for k, v in items:
            self.logger.error(('    %s:%s' % (k, v)))

    def __init__(self):
        super(ReferenceWrapper, self).__init__()
        self.logger = make_logger(self)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def tickPrice(self, tickerId, field, price, canAutoExecute):
        self.showmessage('tickPrice', vars())

    def tickSize(self, tickerId, field, size):
        self.showmessage('tickSize', vars())

    def tickOptionComputation(self, tickerId, field, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        self.showmessage('tickOptionComputation', vars())

    def tickGeneric(self, tickerId, tickType, value):
        self.showmessage('tickGeneric', vars())

    def tickString(self, tickerId, tickType, value):
        self.showmessage('tickString', vars())

    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        self.showmessage('tickEFP', vars())

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeId):
        self.showmessage('orderStatus', vars())

    def openOrder(self, orderId, contract, order, state):
        self.showmessage('openOrder', vars())

    def openOrderEnd(self):
        self.showmessage('openOrderEnd', vars())

    def updateAccountValue(self, key, value, currency, accountName):
        self.showmessage('updateAccountValue', vars())

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        self.showmessage('updatePortfolio', vars())

    def updateAccountTime(self, timeStamp):
        self.showmessage('updateAccountTime', vars())

    def accountDownloadEnd(self, accountName):
        self.showmessage('accountDownloadEnd', vars())

    def nextValidId(self, orderId):
        self.showmessage('nextValidId', vars())

    def contractDetails(self, reqId, contractDetails):
        self.showmessage('contractDetails', vars())

    def contractDetailsEnd(self, reqId):
        self.showmessage('contractDetailsEnd', vars())

    def bondContractDetails(self, reqId, contractDetails):
        self.showmessage('bondContractDetails', vars())

    def execDetails(self, reqId, contract, execution):
        self.showmessage('execDetails', vars())

    def execDetailsEnd(self, reqId):
        self.showmessage('execDetailsEnd', vars())

    def connectionClosed(self):
        self.showmessage('connectionClosed', {})

    def error(self, id=None, errorCode=None, errorMsg=None):
        global DataRequests
        if id == -1:
            return
        self.showmessage('error', vars())
        if type(id) == int:
            DataRequests[id].done()

        else:
            for req in DataRequests.values():
                req.done()



    def error_0(self, strvalue=None):
        self.showmessage('error_0', vars())

    def error_1(self, id=None, errorCode=None, errorMsg=None):
        self.showmessage('error_1', vars())

    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        self.showmessage('updateMktDepth', vars())

    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        self.showmessage('updateMktDepthL2', vars())

    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        self.showmessage('updateNewsBulletin', vars())

    def managedAccounts(self, accountsList):
        self.showmessage('managedAccounts', vars())

    def receiveFA(self, faDataType, xml):
        self.showmessage('receiveFA', vars())

    def historicalData(self, reqId, date, open, high, low, close, volume, count, WAP, hasGaps):
        # self.showmessage('historicalData', vars())
        req = DataRequests[reqId]

        if volume == -1:
            req.done()
        else:
            if req.type == DATA_REQ_BAR_DAY:
                time = TZ_NY.localize(datetime.strptime(date, "%Y%m%d"))
            else:
                time = datetime.fromtimestamp(int(date), TZ_NY)
            req.bars.append(Bar(time, high, low, open, close,volume))




    def scannerParameters(self, xml):
        self.showmessage('scannerParameters', vars())

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        self.showmessage('scannerData', vars())

    def accountDownloadEnd(self, accountName):
        self.showmessage('acountDownloadEnd', vars())

    def commissionReport(self, commissionReport):
        self.showmessage('commissionReport', vars())

    def contractDetailsEnd(self, reqId):
        self.showmessage('contractDetailsEnd', vars())

    def currentTime(self, time):
        self.showmessage('currentTime', vars())

    def deltaNeutralValidation(self, reqId, underComp):
        self.showmessage('deltaNeutralValidation', vars())

    def execDetailsEnd(self, reqId):
        self.showmessage('execDetailsEnd', vars())

    def fundamentalData(self, reqId, data):
        self.showmessage('fundamentalData', vars())

    def marketDataType(self, reqId, marketDataType):
        self.showmessage('marketDataType', vars())

    def openOrderEnd(self):
        self.showmessage('openOrderEnd', vars())

    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        self.showmessage('realtimeBar', vars())

    def scannerDataEnd(self, reqId):
        self.showmessage('scannerDataEnd', vars())

    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        self.showmessage('tickEFP', vars())

    def tickGeneric(self, tickerId, tickType, value):
        self.showmessage('tickGeneric', vars())

    def tickSnapshotEnd(self, reqId):
        self.showmessage('tickSnapshotEnd', vars())

    def error_0(self, strval):
        self.showmessage('error_0', vars())

    def error_1(self, id, errorCode, errorMsg):
        self.showmessage('error_1', vars())

    def position(self, account, contract, pos, avgCost):
        self.showmessage('position', vars())

    def positionEnd(self):
        self.showmessage('positionEnd', vars())

    def accountSummary(self, reqId, account, tag, value, currency):
        self.showmessage('accountSummary', vars())

    def accountSummaryEnd(self, reqId):
        self.showmessage('accountSummaryEnd', vars())

# allMethods = []
# def ref(method):
#     allMethods.append(method.__name__)
#     return method
#
#
# class ReferenceApp:
#     def __init__(self, host='localhost', port=7496, clientId=0):
#         self.host = host
#         self.port = port
#         self.clientId = clientId
#         self.wrapper = ReferenceWrapper()
#         self.connection = EClientSocket(self.wrapper)
#
#     @ref
#     def eConnect(self):
#         self.connection.eConnect(self.host, self.port, self.clientId)
#
#     @ref
#     def reqAccountUpdates(self):
#         self.connection.reqAccountUpdates(1, '')
#
#     @ref
#     def reqOpenOrders(self):
#         self.connection.reqOpenOrders()
#
#     @ref
#     def reqExecutions(self):
#         filt = ExecutionFilter()
#         self.connection.reqExecutions(0, filt)
#
#     @ref
#     def reqIds(self):
#         self.connection.reqIds(10)
#
#     @ref
#     def reqNewsBulletins(self):
#         self.connection.reqNewsBulletins(1)
#
#     @ref
#     def cancelNewsBulletins(self):
#         self.connection.cancelNewsBulletins()
#
#     @ref
#     def setServerLogLevel(self):
#         self.connection.setServerLogLevel(3)
#
#     @ref
#     def reqAutoOpenOrders(self):
#         self.connection.reqAutoOpenOrders(1)
#
#     @ref
#     def reqAllOpenOrders(self):
#         self.connection.reqAllOpenOrders()
#
#     @ref
#     def reqManagedAccts(self):
#         self.connection.reqManagedAccts()
#
#     @ref
#     def requestFA(self):
#         self.connection.requestFA(1)
#
#     @ref
#     def reqMktData(self):
#         contract = Contract() #
#         contract.m_symbol = 'AUD'
#         contract.m_currency = 'USD'
#         contract.m_secType = 'CASH'
#         contract.m_exchange = 'IDEALPRO'
#         self.connection.reqMktData(1, contract, '', False)
#
#     @ref
#     def reqHistoricalData(self):
#         contract = Contract()
#         contract.m_symbol = 'QQQQ'
#         contract.m_secType = 'STK'
#         contract.m_exchange = 'SMART'
#         endtime = strftime('%Y%m%d %H:%M:%S')
#         self.connection.reqHistoricalData(
#             tickerId=1,
#             contract=contract,
#             endDateTime=endtime,
#             durationStr='1 D',
#             barSizeSetting='1 min',
#             whatToShow='TRADES',
#             useRTH=0,
#             formatDate=1)
#
#
#     def eDisconnect(self):
#         sleep(5)
#         self.connection.eDisconnect()
#
#
# if __name__ == '__main__':
#     app = ReferenceApp()
#     methods = argv[1:]
#
#     if not methods:
#         methods = ['eConnect', 'eDisconnect', ]
#     elif methods == ['all']:
#         methods = allMethods
#     if 'eConnect' not in methods:
#         methods.insert(0, 'eConnect')
#     if 'eDisconnect' not in methods:
#         methods.append('eDisconnect')
#
#     print(('### calling functions:', str.join(', ', methods)))
#     for mname in methods:
#         call = getattr(app, mname, None)
#         if call is None:
#             print(('### warning: no call %s' % (mname, )))
#         else:
#             print(('## calling', call.__func__.__name__))
#             call()
#             print(('## called', call.__func__.__name__))

BAR_MIN = "1 min"
BAR_DAY = "1 day"
BAR_TYPES = (BAR_MIN,BAR_DAY)

BAR_TYPE_TO_REQ = {
    BAR_MIN: DATA_REQ_BAR_MINUTE,
    BAR_DAY: DATA_REQ_BAR_DAY
}

class IBMarketData(object):
    def __init__(self, host='127.0.0.1', port=7496, clientId=0):
        self.host = host
        self.port = port
        self.clientId = clientId
        self.wrapper = ReferenceWrapper()
        self.connection = EClientSocket(self.wrapper)
        self.logger = make_logger(self)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def market_data_get(self, symbol, data_type):
        self.connection.reqMktData(1, )
        contract = Contract()
        contract.m_symbol = 'QQQ'
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART'
        self.connection.reqMktData(1, contract, '', False)

    def market_data_register(self, symbol, data_type, handler, handler_ctx):
        pass

    def market_data_unregister(self, symbol, data_type):
        pass

    def _make_stock_contract(self, symbol):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = 'STK'
        contract.m_exchange = 'SMART/ISLAND'
        return contract

    def _generate_ticker_id(self):
        global DataRequests

        while True:
            id = random.randint(1,9999)

            if id not in DataRequests.keys():
                return id

    def historical_bars_get(self, symbol, bar_type, start, end=None):
        self.logger.error('symbol={}, bar_type={}, start={}, end={}'.format(symbol, bar_type, start, end))

        id = self._generate_ticker_id()

        global DataRequests
        data_request = DataRequest(BAR_TYPE_TO_REQ[bar_type])
        DataRequests[id] = data_request


        if end is None:
            end = start

        if bar_type == BAR_MIN:
            end += timedelta(minutes=1)
        elif bar_type == BAR_DAY:
            start = datetime(year=start.year, month=start.month, day=start.day)
            end = datetime(year=end.year, month=end.month, day=end.day)
            end += timedelta(days=1)
        else:
            raise ValueError()


        if start.tzname() == None:
            start = TZ_NY.localize(start)
            end = TZ_NY.localize(end)

        start = start.astimezone(TZ_LOCAL)
        end = end.astimezone(TZ_LOCAL)

        assert end >= start

        end_start_delta = end - start

        duration = '{days} D'.format(days=end_start_delta.days+1)
        if bar_type == BAR_DAY and end_start_delta.days+1 > 365:
            duration = '{years} Y'.format(years=(end_start_delta.days / 365) + 1)

        endtime = end.strftime('%Y%m%d %H:%M:%S')

        args = dict(
            tickerId=id,
            contract=self._make_stock_contract(symbol),
            endDateTime=endtime,
            durationStr=duration,
            barSizeSetting=bar_type,
            whatToShow='TRADES',
            useRTH=0,
            formatDate=2 #linux time
        )

        self.logger.error('reqHistoricalData(id:{} | type:"{}" | duration:"{}" | end:"{}"'.format(id, bar_type, duration, endtime))

        self.connection.reqHistoricalData(**args)

        data_request.wait()
        start = start.astimezone(TZ_NY)
        end = end.astimezone(TZ_NY)
        bars = [b for b in data_request.bars if start <= b.get_time() <= end]

        DataRequests.pop(id)


        return bars

    def bars_register(self, symbol, handler, handler_ctx):
        pass

    def bars_unregister(self, symbol):
        pass

    def connect(self):
        self.connection.eConnect(self.host, self.port, self.clientId)

    def disconnect(self):
        self.connection.eDisconnect()
        time.sleep(0.15)



import unittest
class UltMarketData(unittest.TestCase):

    def setUp(self):
        self.market_data = IBMarketData()
        self.market_data.connect()

    def tearDown(self):
        self.market_data.disconnect()

    def test_historical_bars_get_single(self):

        # minute single
        start = datetime(year=2017, month=8, day=8, hour=12, minute=2)
        bars = self.market_data.historical_bars_get('INTC', BAR_MIN, start)
        self.assertEquals(len(bars), 1)
        self.assertEquals(TZ_NY.localize(start), bars[0].get_time())

        # day single
        start = datetime(year=2017, month=3, day=2)
        bars = self.market_data.historical_bars_get('NVDA', BAR_DAY, start)
        self.assertEquals(len(bars), 1)
        self.assertEquals(TZ_NY.localize(start), bars[0].get_time())

    def test_historical_bars_get_multiple(self):

        start = datetime(year=2017, month=8, day=8, hour=12, minute=2)
        end = datetime(year=2017, month=8, day=8, hour=13, minute=32)
        bars = self.market_data.historical_bars_get('INTC', BAR_MIN, start, end)
        minutes = int((end-start).total_seconds() / 60) + 1
        self.assertEquals(len(bars), minutes)
        self.assertEquals(TZ_NY.localize(start), bars[0].get_time())
        self.assertEquals(TZ_NY.localize(end), bars[-1].get_time())

        start = datetime(year=2017, month=8, day=7)
        end = datetime(year=2017, month=8, day=8)
        bars = self.market_data.historical_bars_get('SPY', BAR_DAY, start, end)
        days = int((end-start).total_seconds() / 86400) + 1
        self.assertEquals(len(bars), days)
        print days
        self.assertEquals(TZ_NY.localize(start), bars[0].get_time())
        self.assertEquals(TZ_NY.localize(end), bars[1].get_time())

