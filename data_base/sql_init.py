import sqlite3 as sq


base = sq.connect('profcom_base.db', timeout=10)
cur = base.cursor()

if __name__ == 'main':
    print(cur, base)
