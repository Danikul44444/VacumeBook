from bs4 import BeautifulSoup
from browser import web
import time
import sqlite3
from prettytable import PrettyTable


def parse(driver, search: str, table_name) -> None:
    table = PrettyTable()
    table.field_names = ['Title', 'Price', 'Author', 'Link']
    driver.get(f'https://www.bookvoed.ru/search?q={search.replace(' ', '+')}')
    source = driver.page_source

    soup = BeautifulSoup(source, 'lxml')

    conn = sqlite3.connect('./database/database.db')
    cur = conn.cursor()
    data = soup.find_all('div', {'class': 'product-card'})

    for item in data:
        try:
            title = item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link base-link'}).text
        except:
            title = item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link product-description__link--single base-link'}).text
        
        price_elem = item.find('div', {'class': 'price-info price-info--size-s product-card__price-row'})
        try:
            price = str(price_elem.find('span', {'class': 'price-info__price--sale price-info__price'}).text).replace('\xa0', '').replace('₽', '') if price_elem else None
        except:
            price = None
        try:
            link = f"https://bookvoed.ru{item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link base-link'}).get('href')}"
        except:
            link = f"https://bookvoed.ru{item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link product-description__link--single base-link'}).get('href')}"
        author_elem = item.find('a', {'class': 'ui-link ui-link__color-scheme--six ui-comma-separated-links__author base-link'})
        author = author_elem.find('span', {'class': 'ui-comma-separated-links__tag'}).text if author_elem else None
        if price != None:
            cur.execute(f"""INSERT INTO {table_name}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()
        else:
            break
    # print(table)
