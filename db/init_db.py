import sqlite3
connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Third Post', 'Content for the third post')
            )

#CONVERTING QUERY RESULTS INTO PYTHON DICT
desc = cursor.description
column_names = [col[0] for col in desc]
data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

connection.commit()
connection.close()