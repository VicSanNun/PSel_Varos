from scrapping_news import get_news

BASE_URL = "https://braziljournal.com/"
search = "c%26a"

articles = get_news(BASE_URL, search)

for article, _ in zip(articles[:3], range(3)):
    header_text = article.text.strip()
    link = article.a['href'].strip() if article.a else 'N/A'

    print(f"Header: {header_text}")
    print(f"Link: {link}")
    print("------")
