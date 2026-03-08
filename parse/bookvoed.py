import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3


def bookvoed_parse(search: str, name_table: str) -> str:
    ua = UserAgent()
    url = f'https://www.bookvoed.ru/search?q={search}'
    header = {'User-Agent': ua.edge}
    respo = requests.get(url, headers=header)
    status = respo.status_code

    if status == 200:
        soup = BeautifulSoup(respo.content, 'lxml')
        data = soup.find_all('div', {'class': 'product-card'})
        conn = sqlite3.connect('./database/database.db')
        cur = conn.cursor()
        for item in data:

            title = item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link base-link'})

            price_elem = item.find('span', {'class': 'price-info__price--sale price-info__price'})
            price = int(price_elem.text.replace('\xa0', '').replace('₽', '')) if price_elem else None

            link = f'https://www.bookvoed.ru{item.find('a', {'class': 'product-card__image-link base-link'}).get('href')}'
            author_elem = item.find('a', {'class': 'ui-link ui-link__color-scheme--six ui-comma-separated-links__author base-link'})
            author = item.find('span', {'class': 'ui-comma-separated-links__tag'}).text if author_elem else "Author not found!"
            cur.execute(f"""INSERT INTO {name_table}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title.text, price, link, author))
            conn.commit()


    else:
        print(f'Error code: {status}')

