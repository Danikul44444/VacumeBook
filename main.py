from parse.book24 import book24_parse
from parse.labirint import labirint_parse
from parse.bookvoed import bookvoed_parse
from threading import Thread
>>>>>>> c8e6725 (Added three parser)
import sqlite3
import time
import os 
CREATE_TABLE = """CREATE TABLE BOOK(
    TITLE TEXT,
    PRICE INTEGER,
    LINK TEXT,
    AUTHOR TEXT
)"""
os.mkdir('./database')
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
<<<<<<< HEAD
bookvoed_parse(search, "BOOK")
=======

>>>>>>> 76b1e63 (Add README.md)
