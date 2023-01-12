import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id VARCHAR(255), lang VARCHAR(255))')
