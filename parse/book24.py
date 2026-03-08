import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3


def book24_parse(search: str, name_table: str) -> str:
    ua = UserAgent()
    url = f'https://book24.ru/search/?q={search}'
    header = {'User-Agent': ua.edge}
    respo = requests.get(url, headers=header)
    status = respo.status_code

    if status == 200:
        soup = BeautifulSoup(respo.content, 'lxml')
        data = soup.find_all('div', {'class': 'product-card'})
        conn = sqlite3.connect('./database/database.db')
        cur = conn.cursor()
        for item in data:
            title = str(item.find('a', {'class': 'product-card__name'}).text)

            price_elem = item.find('span', {'class': 'app-price'})
            price = int(price_elem.text.replace(' ', '').replace('₽', '')) if price_elem else None

            link = f'https://book24.ru{item.find('a', {'class': 'product-card__name'}).get('href')}'
            author_elem = item.find('div', {'class': 'author-list product-card__authors-holder'})
            author = item.find('a', {'class': 'author-list__item smartLink'}).text if author_elem else "Author not found!"
            cur.execute(f"""INSERT INTO {name_table}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()
        
    else:
        print(f'Error code: {status}')

