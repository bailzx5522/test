import os
import utils
from yahoo import YahooFinance
from model import Quote
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from algorithms.tenPersent import TenPersent

SYMBOL_FILE = '../data/symbols_002000.sz'
SQLITE_FILE = '../data/stock.sqlite'
S_DATE = '2013-01-01'
E_DATE = '2014-12-31'
    
def insert_history_prices(db, symbol, start, end):
    symbol = symbol.strip()
    exist = db.readQuotes(symbol.split('.')[0])
    n = len(exist)
    if n>0:
        print "%s has inserted!" % symbol
        return

    y = YahooFinance()
    h_prices = y.getQuotes(symbol, start, end)
    if not h_prices:
        print "Symbol %s is 404..." % symbol
        return
    print "It's a new symbol:%s, insert from %s to %s!" % (symbol, start, end)    
    db.writeQuotes(h_prices)
    db.commit()

def init_data(db, symbols):
    for symbol in symbols:
        insert_history_prices(db, symbol, S_DATE, E_DATE)

def analysis_data(db, symbols):
    sum_profit = 0
    sum_balance = 0
    win = 0
    lose = 0
    for s in symbols:
        data = db.readQuotes(utils.symbol2num(s))
        if data:
            algo = TenPersent(data)
            result = algo.algorithm()
            if result != 10000:
                print "Symbol:%s*******************10000 -> %s\n\n" % (s,result)
                if result > 10000:
                    win += 1
                if result < 10000:
                    lose += 1
                sum_profit += result
                sum_balance += 10000
    print sum_profit
    print sum_balance
    print win
    print lose

def main():
    #init
    symbols = utils.get_symbols(SYMBOL_FILE)
    db = utils.get_db(SQLITE_FILE)
    
    #download data from website, then update the database.
    #init_data(db, symbols)
    
    analysis_data(db, symbols)
    

if __name__ == '__main__':
    main()