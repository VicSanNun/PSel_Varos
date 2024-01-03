import yfinance as yf
from datetime import datetime

def get_stock_data(ticker, start_date, end_date = datetime.today().strftime('%Y-%m-%d')):

    start_date = start_date

    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        data = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close']]

        return data

    except Exception as e:
        print(f"Ocorreu um erro: {e}")