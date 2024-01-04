from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('mysql+mysqlconnector://psel_varos:psel_varos@localhost/teste', echo=True)

Base = declarative_base()

class Date(Base):
    __tablename__ = 'dim_tempo'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True))

class Stocks(Base):
    __tablename__ = 'dim_stocks'

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(255))
    cod_search = Column(String(255))

    news = relationship('News', back_populates='dim_stocks')   

class News(Base):
    __tablename__ = 'fat_news'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('dim_stocks.company_id'))
    title = Column(String(255))
    link = Column(String(255))
    dat_data = Column(DateTime(timezone=True))

    stock = relationship('Stocks', back_populates='fat_news')
    date = relationship('Date', back_populates='fat_news')


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

    stock = relationship('Stocks', back_populates='fat_prices')
    date = relationship('Date', back_populates='fat_prices')

Base.metadata.create_all(engine)

