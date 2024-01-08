from sqlalchemy.orm import sessionmaker
import yfinance as yf
import requests
from datetime import datetime
from bs4 import BeautifulSoup
if __name__ == "__main__":
    from connector import conn
    from model import Company
    from model import News
    from model import Stocks
else:
    from db.connector import conn
    from db.model import Company
    from db.model import News
    from db.model import Stocks

engine = conn()

JOURNAL_URL = "https://braziljournal.com/"
search_term_id = {"petr4": 1, "weg": 2, "c%26a": 3}
ticker_id = {"PETR4.SA": 1, "WEGE3.SA": 2, "CEAB3.SA": 3}

def get_stock_yahoo(ticker, start_date, end_date = datetime.today().strftime('%Y-%m-%d')):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        data = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close']]
        return data
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def scrapp_news(base_url, search):
    url = f"{base_url}?s={search}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('h2', class_='boxarticle-infos-title')
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except Exception as ex:
        print(f"Ocorreu um erro inesperado: {ex}")

Session = sessionmaker(bind=engine)
session = Session()

################################
PETR = Company(company_id = 1, company_name='Petrobrás', cod_search="petr4", ticker="PETR4.SA")
WEG = Company(company_id = 2, company_name='WEG', cod_search="weg", ticker="WEGE3.SA")
CEA = Company(company_id = 3, company_name='C&A', cod_search="c%26a", ticker="CEAB3.SA")

session.add(PETR)
session.add(WEG)
session.add(CEA)
session.commit()

#################################
for item in search_term_id.items():
    print(f"Obtendo Notícias de {item[0]}")
    articles = scrapp_news(JOURNAL_URL, item[0])

    for article, _ in zip(articles[:3], range(3)):
        title = article.text.strip()
        link = article.find('a')['href']
        if not session.query(News).filter_by(title=title, link=link).first():
            new_news = News(
                title=title,
                link=link,
                dat_data=datetime.now(),
                company_id=item[1],
            )
            session.add(new_news)
    session.commit()

###################################
for item in ticker_id.items():
    stock_data_yahoo = get_stock_yahoo(item[0], '2023-01-01') 

    for index, row in stock_data_yahoo.iterrows():
        new_stock_data = Stocks(
            dat_data=index,
            company_id=item[1],
            open_price=row['Open'],
            max_price=row['High'],
            min_price=row['Low'],
            close_price=row['Close'],
            adj_close_price=row['Adj Close']
        )
        session.add(new_stock_data)     
    session.commit()

session.close()