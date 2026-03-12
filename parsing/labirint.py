from bs4 import BeautifulSoup
import time
import sqlite3

def parse(driver, search: str, name_table: str):
    driver.get(f'https://www.bookvoed.ru/search?q={search}')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    data = soup.find_all('div', {'class': 'product-list__item'})
    conn = sqlite3.connect('./database/database.db')
    cur = conn.cursor()
    for item in data:
        title = str(item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link product-description__link--single base-link'}).text)
        price_elem = item.find('span', {'class': 'price-info__price price-info__price--sale'})
        try:
            price = int(str(price_elem.find('div', {'class': 'product-card__price-current'}).text).replace(' ', '').replace('₽', '')) if price_elem else None
        except:
            price = None
        link = f'https://www.bookvoed.ru{item.find('a', {'class': 'ui-link ui-link__color-scheme--two product-description__link product-description__link--single base-link'}).get('href')}'
        author_elem = item.find('div', {'class': 'ui-link ui-link__color-scheme--six ui-comma-separated-links__author base-link'})
        author = item.find('span', {'class': 'ui-comma-separated-links__tag'}).text if author_elem else "Author not found!"
        if price != None:
            cur.execute(f"""INSERT INTO {name_table}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()

