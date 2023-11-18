import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO ingredients (ingredient, expiry, amount) VALUES (?, ?, ?)",
            ('First ingredient', 0, 1)
            )

cur.execute("INSERT INTO ingredients (ingredient, expiry, amount) VALUES (?, ?, ?)",
            ('Second ingredient', 0, 1)
            )

connection.commit()
connection.close()