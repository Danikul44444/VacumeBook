<<<<<<< HEAD
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
=======
from parse.book24 import book24_parse
from parse.labirint import labirint_parse
from parse.bookvoed import bookvoed_parse
from threading import Thread
import sqlite3
import time
CREATE_TABLE = """CREATE TABLE BOOK(
    TITLE TEXT,
    PRICE INTEGER,
    LINK TEXT,
    AUTHOR TEXT
)"""

conn = sqlite3.connect('./database/database.db')
cur = conn.cursor()

cur.execute(CREATE_TABLE)
conn.commit()

search = input("Enter book search: ")

book24_parse(search, "BOOK")
time.sleep(3)
labirint_parse(search, "BOOK")
time.sleep(3)
bookvoed_parse(search, "BOOK")
>>>>>>> 8ad9f10 (Added three parser)
