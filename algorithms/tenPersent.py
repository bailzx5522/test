from algo_base import Algo_base

class TenPersent(Algo_base):
    def __init__(self, data):
        super(TenPersent, self).__init__(data)
        
    def algorithm(self):
        previous = 0
        won_d = 0
        balance = 10000
        buy_price = 0
        
        for day in self.data:
            # first day
            if previous == 0:
                previous = day.open
            else:
                change = (day.close-previous)/previous
                #print '%.2f%%'%(change*100)
                if won_d and day.close-day.open < 0 and buy_price == 0:
                    #print 'buy at %s' % day.time
                    buy_price = day.close
                    #print 'Buy %s at price %s' % (balance/buy_price, buy_price)
                if change< 0.11 and change >0.09:
                    won_d = day.time
                    #print '%s is a wonderful day!!!' % day.time
                else:
                    won_d = 0
                
                if buy_price and ((day.close-buy_price)/buy_price >= 0.2 or (day.close-buy_price)/buy_price <= -0.1):
                    balance += balance * (day.close-buy_price)/buy_price
                    print "Sell at %s.Buy %s ==>> Sell %s" % (day.time,buy_price, day.close)
                    buy_price = 0
                previous = day.close
                
        return balance
