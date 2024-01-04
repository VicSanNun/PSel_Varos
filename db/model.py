from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from db.connector import conn

engine = conn()

Base = declarative_base()

class Date(Base):
    __tablename__ = 'dim_tempo'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True))

    # Relacionamentos bidirecionais
    news = relationship('News', back_populates='date', foreign_keys='News.date_id')
    prices = relationship('Prices', back_populates='date', foreign_keys='Prices.date_id')

class Stocks(Base):
    __tablename__ = 'dim_stocks'

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(255))
    cod_search = Column(String(255))
    ticker = Column(String(255))

    # Relacionamentos bidirecionais
    news = relationship('News', back_populates='stock', foreign_keys='News.company_id')
    prices = relationship('Prices', back_populates='stock', foreign_keys='Prices.company_id')

class News(Base):
    __tablename__ = 'fat_news'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('dim_stocks.company_id'))
    title = Column(String(255))
    link = Column(String(255))
    dat_data = Column(DateTime(timezone=True))

    stock = relationship('Stocks', back_populates='news', foreign_keys=[company_id])
    date_id = Column(Integer, ForeignKey('dim_tempo.id'))  
    date = relationship('Date', back_populates='news', foreign_keys=[date_id])

class Prices(Base):
    __tablename__ = 'fat_prices'

    id = Column(Integer, primary_key=True)
    dat_data = Column(DateTime(timezone=True))
    company_id = Column(Integer, ForeignKey('dim_stocks.company_id'))
    open_price = Column(Float)
    max_price = Column(Float)
    min_price = Column(Float)
    close_price = Column(Float)
    adj_close_price = Column(Float)

    stock = relationship('Stocks', back_populates='prices', foreign_keys=[company_id])
    date_id = Column(Integer, ForeignKey('dim_tempo.id'))  
    date = relationship('Date', back_populates='prices', foreign_keys=[date_id])

Base.metadata.create_all(engine)
