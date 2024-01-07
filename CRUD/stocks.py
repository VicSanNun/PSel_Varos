import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from db.model import Stocks
import pandas as pd

class Stocks_CRUD:
    def __init__(self, conn) -> None:
        try:
            self.conn = conn
            self.Session = sessionmaker(bind=self.conn)
            self.session = self.Session()
        except Exception as e:
            print('A Classe não foi inicializada corretamente: ', e)
    
    def get_today_or_last_working_day(self):
        today = pd.Timestamp('today')
        if today.weekday() < 5:
            return today
        else:
            last_working_day = today - pd.tseries.offsets.BDay(1)
            return last_working_day


    def get_stock_yahoo(self, ticker, start_date, end_date = datetime.today().strftime('%Y-%m-%d')):
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            data = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close']]
            return data
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
    

    def get_stock_data(self, company_id, ticker, start_date):
        updated_data = []
        try:
            latest_record = self.session.query(Stocks).filter_by(company_id=company_id).order_by(Stocks.dat_data.desc()).all()
            if not latest_record:
                stock_data_yahoo = self.get_stock_yahoo(ticker, start_date) 
            
                for index, row in stock_data_yahoo.iterrows():
                    new_stock_data = Stocks(
                        dat_data=index,
                        company_id=company_id,
                        open_price=row['Open'],
                        max_price=row['High'],
                        min_price=row['Low'],
                        close_price=row['Close'],
                        adj_close_price=row['Adj Close']
                    )
                    self.session.add(new_stock_data)
                    updated_data.append(new_stock_data)

                self.session.commit()
                return updated_data
            
            elif (self.get_today_or_last_working_day() - latest_record[0].dat_data).days > 1:
                stock_data_yahoo = self.get_stock_yahoo(ticker, (latest_record[0].dat_data+timedelta(days=1)).strftime('%Y-%m-%d'))
                for index, row in stock_data_yahoo.iterrows():
                    new_stock_data = Stocks(
                        dat_data=index,
                        company_id=company_id,
                        open_price=row['Open'],
                        max_price=row['High'],
                        min_price=row['Low'],
                        close_price=row['Close'],
                        adj_close_price=row['Adj Close']
                    )
                    self.session.add(new_stock_data)
                    updated_data.append(new_stock_data)
            
                self.session.commit()
                return updated_data
            
            else:
                return latest_record

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None