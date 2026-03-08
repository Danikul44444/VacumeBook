import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3


def labirint_parse(search: str, name_table: str) -> str:
    ua = UserAgent()
    url = f'https://www.labirint.ru/search/{search}/'
    header = {'User-Agent': ua.edge}
    respo = requests.get(url, headers=header)
    status = respo.status_code

    if status == 200:
        soup = BeautifulSoup(respo.content, 'lxml')
        
        conn = sqlite3.connect('./database/database.db')
        cur = conn.cursor()

        data = soup.find('div', {'class': 'search-result'}).find_all('div', {'class': 'product-card need-watch'})
        for item in data:
            title = str(item.find('a', {'class': 'product-card__name'}).text).replace('\n', '').replace('  ', '')
            price_elem = item.find('div', {'class': 'product-card__price-current'})
            price = int(price_elem.text.replace(' ', '').replace('₽', '')) if price_elem else None
            link = f'https://www.labirint.ru{item.find('a', {'class': 'product-card__name'}).get('href')}'
            author_elem = item.find('a', {'class': 'ui-link ui-link__color-scheme--six ui-comma-separated-links__author base-link'})
            author = author_elem.find('span', {'class': 'ui-comma-separated-links__tag'}).text if author_elem else "Author not found!"
            cur.execute(f"""INSERT INTO {name_table}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()
    else:
        print(f'Error code: {status}')

