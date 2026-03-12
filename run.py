from parsing import book24
from parsing import bookvoed
from parsing import labirint
#...
from browser import web
from sqlite3 import connect as sqlConnect
from datetime import datetime
import time
import os

os.mkdir('./database')

conn = sqlConnect('./database/database.db')
cur = conn.cursor()

CREATE_TABLE="""CREATE TABLE IF NOT EXISTS BOOK(
    TITLE TEXT, 
    PRICE INTEGER,
    LINK TEXT,
    AUTHOR TEXT
)"""
cur.execute(CREATE_TABLE)
conn.commit()
parsers = [{"name": "book24","run": book24},
           {"name": "bookvoed","run": bookvoed}, 
           {"name": "labirint","run": labirint}]

search = input("Enter the title of the book you want to search: ")
browser = web.browser()

for run in parsers:
    try:
        print(f"{run['name']} начал работу")
        start = time.time()
        run['run'].parse(browser, search, "BOOK")
        end = time.time()
        print(f'{run['name']} завешил работу за {time.strftime("%H:%M:%S", time.gmtime(end-start))}')
    except:
        print(f"{run['name']} не отработал")

conn.close()