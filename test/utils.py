import os
from db.sqlite import Sqlite

def compare_date(date_1, date_2):
    date1 = date_1.split('-')
    date2 = date_2.split('-')
    for i in len(date1):
        if date1[i] > date2[i]:
            return date_1
        elif date1[i] < date2[i]:
            return date_2
        else:
            continue
    return 0

def generate_symbol_file(file, s, e, type):
    f = open(file, 'w')
    symbols = []
    while s <= e:
        if type == 'sz':
            symbol = '00' + str(s) + '.sz\n'
            symbols.append(symbol) 
        s += 1
    f.writelines(symbols)
    print "finish wirte %s!" % file

def get_symbols(symbol_file):
    f = open(symbol_file, 'r')
    symbols = f.readlines()
    #symbols = ['002001.sz', '002002.sz', '002003.sz', '002005.sz']#, '399001.sz']
    return symbols
    
def get_db(sqlite_file):
    db = Sqlite()
    sqlite_location = os.path.join(os.getcwd(), sqlite_file)
    db.setup({'db': 'sqlite:///%s'%sqlite_location})
    return db

def symbol2num(symbol):
    #convert 002312.sz to 002312
    if '.' in symbol:
        return symbol.split('.')[0]
    else:
        return symbol
#generate_symbol_file('../data/symbols_002000.sz', 2001, 2725, 'sz')
