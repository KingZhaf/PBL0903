import sqlite3

def tables(path):
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return cur.fetchall()
    except Exception as e:
        return str(e)

print('DB-A tables:', tables('SiteA/DB-A.db'))
print('DB-B tables:', tables('SiteB/MS3/DB-B.db'))
