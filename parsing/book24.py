from bs4 import BeautifulSoup
import time
import sqlite3

def parse(driver, search: str, name_table: str):
    driver.get(f'https://book24.ru/search/?q={search}')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = soup.find_all('div', {'class': 'product-list__item'})
    conn = sqlite3.connect('./database/database.db')
    cur = conn.cursor()

    for item in data:
        title = str(item.find('a', {'class': 'product-card__name'}).text)
        price_elem = item.find('span', {'class': 'app-price'})
        try:
            price = int(str(price_elem.text).replace(' ', '').replace('₽', '')) if price_elem else None
        except:
            price = None
        link = f'https://book24.ru{item.find('a', {'class': 'product-card__name'}).get('href')}'
        author_elem = item.find('div', {'class': 'author-list product-card__authors-holder'})
        author = item.find('a', {'class': 'author-list__item smartLink'}).text if author_elem else "Author not found!"
        if price != None:
            cur.execute(f"""INSERT INTO {name_table}(TITLE, PRICE, LINK, AUTHOR) VALUES (?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()
