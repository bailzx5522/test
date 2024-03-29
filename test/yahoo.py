import urllib
from model import Quote

class YahooFinance(object):
    #002312.sz
    def __request(self, symbol, stat):
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
        return urllib.urlopen(url).read().strip().strip('"')

    def getAll(self, symbol):
        """
        Get all available quote data for the given ticker symbol.
        Returns a dictionary.
        """
        values = self.__request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        data = {}
        data['price'] = values[0]
        data['change'] = values[1]
        data['volume'] = values[2]
        data['avg_daily_volume'] = values[3]
        data['stock_exchange'] = values[4]
        data['market_cap'] = values[5]
        data['book_value'] = values[6]
        data['ebitda'] = values[7]
        data['dividend_per_share'] = values[8]
        data['dividend_yield'] = values[9]
        data['earnings_per_share'] = values[10]
        data['52_week_high'] = values[11]
        data['52_week_low'] = values[12]
        data['50day_moving_avg'] = values[13]
        data['200day_moving_avg'] = values[14]
        data['price_earnings_ratio'] = values[15]
        data['price_earnings_growth_ratio'] = values[16]
        data['price_sales_ratio'] = values[17]
        data['price_book_ratio'] = values[18]
        data['short_ratio'] = values[19]
        return data
    
    def getQuotes(self, symbol, start, end):
        start = str(start).replace('-', '')
        end = str(end).replace('-', '')
        retries = 3
        url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
            'd=%s&' % str(int(end[4:6]) - 1) + \
            'e=%s&' % str(int(end[6:8])) + \
            'f=%s&' % str(int(end[0:4])) + \
            'g=d&' + \
            'a=%s&' % str(int(start[4:6]) - 1) + \
            'b=%s&' % str(int(start[6:8])) + \
            'c=%s&' % str(int(start[0:4])) + \
            'ignore=.csv'
        for i in range(retries):
            try:
                days = urllib.urlopen(url).readlines()
                values = [day[:-2].split(',') for day in days]
                # sample values:[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], \
                #              ['2009-12-31', '112.77', '112.80', '111.39', '111.44', '90637900', '109.7']...]
                data = []
                for value in values[1:]:
                    data.append(Quote(symbol, value[0], value[1], value[2], value[3], value[4], value[5], value[6]))
                    dateValues = sorted(data, key = lambda q: q.time)
            except IOError:
                if retries == i+1:
                    return None
                else:
                    continue
            except:
                if retries == i+1:
                    print "URL: %s get unexcepted data %s." %(url, days)
                    return None
                else:
                    continue
            return dateValues
        
        
