from sqlalchemy.orm import sessionmaker
from db.model import News
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class News_Controller:
    def __init__(self, conn) -> None:
        try:
            self.conn = conn
            self.Session = sessionmaker(bind=self.conn)
            self.session = self.Session()
        except Exception as e:
            print('A Classe não foi inicializada corretamente: ', e)

    def scrapp_news(self, base_url, search):
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

    def get_news(self, base_url, search, company_id):
        try:
            latest_news = self.session.query(News).filter_by(company_id=company_id).order_by(News.dat_data.desc()).limit(3).all()

            if not latest_news or (datetime.now() - latest_news[0].dat_data).days > 1:
                print("Obtendo Notícias")

                articles = self.scrapp_news(base_url, search)
                news_data = []

                for article, _ in zip(articles[:3], range(3)):
                    title = article.text.strip()
                    link = article.find('a')['href']

                    if not self.session.query(News).filter_by(title=title, link=link).first():
                        new_news = News(
                            title=title,
                            link=link,
                            dat_data=datetime.now(),
                            company_id=company_id,
                        )
                        self.session.add(new_news)

                    news_data.append({'title': title, 'link': link})

                self.session.commit()
                return news_data

            else:
                return [{'title': news.title, 'link': news.link, 'dat_data': news.dat_data} for news in latest_news]

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None