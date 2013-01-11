import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.executescript(open("setup.sql").read())
