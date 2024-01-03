from scrapping_news import get_news
from get_stocks import get_stock_data

BASE_URL = "https://braziljournal.com/"
#search = "c%26a"
search = "petr4"
ticker = "PETR4.SA"
start_date = "2023-01-01"

stock_data = get_stock_data(ticker, start_date)
articles = get_news(BASE_URL, search)

for article, _ in zip(articles[:3], range(3)):
    header_text = article.text.strip()
    link = article.a['href'].strip() if article.a else 'N/A'

    print(f"Header: {header_text}")
    print(f"Link: {link}")
    print("------")

print(stock_data)