from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
if __name__ == "__main__":
    from connector import conn
else:
    from db.connector import conn

engine = conn()

Base = declarative_base()

class Company(Base):
    __tablename__ = 'dim_company'

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(255))
    cod_search = Column(String(255))
    ticker = Column(String(255))

    # Relacionamentos bidirecionais
    news = relationship('News', back_populates='company', foreign_keys='News.company_id')
    prices = relationship('Prices', back_populates='company', foreign_keys='Prices.company_id')

class News(Base):
    __tablename__ = 'fat_news'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('dim_company.company_id'))
    title = Column(String(255))
    link = Column(String(255))
    dat_data = Column(DateTime(timezone=True))

    company = relationship('Company', back_populates='news', foreign_keys=[company_id])

class Prices(Base):
    __tablename__ = 'fat_prices'

    id = Column(Integer, primary_key=True)
    dat_data = Column(DateTime(timezone=True))
    company_id = Column(Integer, ForeignKey('dim_company.company_id'))
    open_price = Column(Float)
    max_price = Column(Float)
    min_price = Column(Float)
    close_price = Column(Float)
    adj_close_price = Column(Float)

    company = relationship('Company', back_populates='prices', foreign_keys=[company_id])

Base.metadata.create_all(engine)
