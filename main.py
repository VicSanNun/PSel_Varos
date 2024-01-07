from db.connector import conn
from CRUD.companies import Companies_CRUD
from CRUD.news import News_CRUD

JOURNAL_URL = "https://braziljournal.com/"

company = Companies_CRUD(conn())
news = News_CRUD(conn())

petro_data = company.get_company_data(1)
weg_data = company.get_company_data(2)
cea_data = company.get_company_data(3)

petro_cod_search = petro_data[0].cod_search
weg_cod_search = weg_data[0].cod_search
cea_cod_search = cea_data[0].cod_search

petro_ticker= petro_data[0].ticker
weg_ticker= weg_data[0].ticker
cea_ticker= cea_data[0].ticker

# start_date = "2023-01-01"

print(petro_data[0].cod_search)

#print(PETRO.company_name)

# stock_data = get_stock_data(ticker, start_date)
petro_articles = news.get_news(JOURNAL_URL, petro_cod_search, 1)
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
