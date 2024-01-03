import requests
from bs4 import BeautifulSoup

def get_news(base_url, search):
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