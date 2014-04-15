import json

class Quote(object):
    ''' tick class '''
    def __init__(self, symbol, time, open, high, low, close, volume, adjClose):
        ''' constructor '''
        self.symbol = symbol[0:6]
        self.time = time
        self.open = 0 if ("-" == open) else float(open)
        self.high = 0 if ("-" == high) else float(high)
        self.low = 0 if ("-" == low) else float(low)
        self.close = 0 if ("-" == close) else float(close)
        self.volume = int(volume)
        self.adjClose = adjClose

    def __str__(self):
        ''' convert to string '''
        return json.dumps({"symbol": self.symbol,
                           "time": self.time,
                           "open": self.open,
                           "high": self.high,
                           "low": self.low,
                           "close": self.close,
                           "volume": self.volume,
                           "adjClose": self.adjClose})

    @staticmethod
    def fromStr(string):
        ''' convert from string'''
        d = json.loads(string)
        return Quote(d['symbol'], d['time'], d['open'], d['high'],
                     d['low'], d['close'], d['volume'], d['adjClose'])
