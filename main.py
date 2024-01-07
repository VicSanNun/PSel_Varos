from db.connector import conn
from CRUD.companies import Companies_CRUD
from CRUD.news import News_CRUD
from CRUD.stocks import Stocks_CRUD

JOURNAL_URL = "https://braziljournal.com/"

ids = {"petro_id": 1, "weg_id": 2, "cea_id": 3}

company = Companies_CRUD(conn())
news = News_CRUD(conn())
stocks = Stocks_CRUD(conn())

petro_data = company.get_company_data(ids["petro_id"])
weg_data = company.get_company_data(ids["weg_id"])
cea_data = company.get_company_data(ids["cea_id"])

petro_cod_search = petro_data[0].cod_search
weg_cod_search = weg_data[0].cod_search
cea_cod_search = cea_data[0].cod_search

petro_ticker= petro_data[0].ticker
weg_ticker= weg_data[0].ticker
cea_ticker= cea_data[0].ticker

start_date = "2023-01-01"

stock_data = stocks.get_stock_data(ids["petro_id"], weg_ticker, start_date)

print(stock_data)

for stock in stock_data:
    print(f"Date: {stock.dat_data}, Open: {stock.open_price}, High: {stock.max_price}, Low: {stock.min_price}, Close: {stock.close_price}, Adj Close: {stock.adj_close_price}")


petro_articles = news.get_news(JOURNAL_URL, weg_cod_search, ids["petro_id"])
print(petro_articles)

if petro_articles is not None:
    for news_item in petro_articles:
        print(f"Title: {news_item['title']}")
        print(f"Link: {news_item['link']}")
        if 'dat_data' in news_item:
            print(f"Date: {news_item['dat_data']}")
        print("------")
else:
    print("Não foi possível obter as notícias.")
