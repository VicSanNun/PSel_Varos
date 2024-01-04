from scrapping_news import get_news
from get_stocks import get_stock_data
from db.connector import conn
from sqlalchemy.orm import sessionmaker
from db.model import Stocks

conn = conn()

Session = sessionmaker(bind=conn)
session = Session()

PETRO = session.query(Stocks).filter(Stocks.company_id == 1).all()
WEG = session.query(Stocks).filter(Stocks.company_id == 2).all()
CEA = session.query(Stocks).filter(Stocks.company_id == 3).all()

BASE_URL = "https://braziljournal.com/"
start_date = "2023-01-01"

for i in PETRO:
    print(i.company_name)

#print(PETRO.company_name)

# stock_data = get_stock_data(ticker, start_date)
# articles = get_news(BASE_URL, search)

# for article, _ in zip(articles[:3], range(3)):
#     header_text = article.text.strip()
#     link = article.a['href'].strip() if article.a else 'N/A'

#     print(f"Header: {header_text}")
#     print(f"Link: {link}")
#     print("------")

# print(stock_data)