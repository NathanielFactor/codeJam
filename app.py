import sqlite3
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/add', methods = ['POST'])
def add():
    conn =get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Fourth Post', 'Content for the fourth post')
            )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/clearTable', methods = ['POST'])
def remove():
    conn =get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)