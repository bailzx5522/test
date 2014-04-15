import sqlite3
from sqlalchemy import Column, Integer, String, Float, Sequence, create_engine, and_, UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuoteSql(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    symbol = Column('symbol', String(12))
    time = Column('time', Integer)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    adjClose = Column(Float)

    def __init__(self, symbol, time, open, high, low, close, volume, adjClose):
        ''' constructor '''
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjClose = adjClose

    def __repr__(self):
        return "<Quote('%s', '%s','%s', '%s', '%s','%s', '%s', '%s')>" \
           % (self.symbol, self.time, self.open, self.high, self.low, self.close, self.volume, self.adjClose)


class Sqlite(object):
    def __init__(self, echo=False):
        self.sql_location = self._get_sql_location()
        self.echo = echo
        self.first = True
        self.engine = None
        self.session = None

    def setup(self, setting):
        if 'db' not in setting:
            print "db not specified in setting"
            return
        self.engine = create_engine(setting['db'], echo = self.echo)
        
    def connect(self):
        self.conn = sqlite3.connect(self.sql_location)
    
    def _get_sql_location(self, file=None, path=None):
        if path and file:
            return path + "/" + file
        else:
            return "../data/sql.db"

    def _get_session(self):
        self.session = sessionmaker(bind = self.engine)()
        return self.session

    def commit(self):
        ''' commit changes '''
        self.session.commit()

    def __quoteToSql(self, quote):
        ''' convert tick to QuoteSql '''
        return QuoteSql(quote.symbol, quote.time, quote.open, quote.high, quote.low, quote.close, quote.volume, quote.adjClose)

    def __sqlToQuote(self, row):
        ''' convert row result to Quote '''
        return QuoteSql(row.symbol, row.time, row.open, row.high, row.low, row.close, row.volume, row.adjClose)

    def writeQuotes(self, quotes):
        ''' write quotes '''
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        session = self._get_session()
        session.add_all([self.__quoteToSql(quote) for quote in quotes])


    def readQuotes(self, symbol, start=None, end=None):
        if self.first:
            Base.metadata.create_all(self.engine, checkfirst = True)
            self.first = False

        session = self._get_session()
        if start and end:
            rows = session.query(QuoteSql).filter(and_(QuoteSql.symbol == symbol,
                                                       QuoteSql.time >= start,
                                                       QuoteSql.time < end)).order_by('time')
        else:
            rows = session.query(QuoteSql).filter(QuoteSql.symbol==symbol).order_by('time')
        return [self.__sqlToQuote(row) for row in rows]





