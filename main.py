import requests
from bs4 import BeautifulSoup
import sqlite3
import time

conn = sqlite3.connect('./database/database.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS ALL_BOOKS(
            TITLE TEXT,
            PRICE INTEGER,
            LINK TEXT,
            AUTHOR TEXT)""")
conn.commit()
for page in range(1, 16):
    url = f'https://www.labirint.ru/books/?page={page}'
    respo = requests.get(url)
    status = respo.status_code
    if status == 200:
        
        soup = BeautifulSoup(respo.content, "lxml")
        data = soup.find_all('div', {'class': 'genres-carousel__item'})

        for item in data:
            title = item.find("span", {'class': 'product-title'}).text
            price = int(str(item.find("span", {'class': 'price-val'}).text).replace('\n', '').replace(' ₽\t\t', '').replace(' ', ''))
            link = f"https://www.labirint.ru{item.find('a', {'class': 'cover genres-cover'}).get('href')}"
            author_elem = item.find("div", {'class': 'product-author'})
            author = str(author_elem.text).replace(' \n', '').replace('\n', '') if author_elem else "Author not found"
            cur.execute("""INSERT OR IGNORE INTO ALL_BOOKS(TITLE, PRICE, LINK, AUTHOR) VALUES(?, ?, ?, ?)""", (title, price, link, author))
            conn.commit()
        print(f"Parse page {page}")
  

    else:
        print(f"Error code: {status}")
    
    time.sleep(4)
conn.close()
