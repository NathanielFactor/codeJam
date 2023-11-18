import sqlite3
from flask import Flask, render_template, redirect, url_for
import sys

from mealRequests import *
from mealObjects import *


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

recipes = []

@app.route('/')
def index():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    print(ingredients)
    conn.close()
    return render_template('index.html', post=ingredients, data=recipes)

@app.route('/add', methods = ['POST'])
def add():
    conn =get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ingredients (ingredient, expiry, amount) VALUES (?, ?, ?)",
            ('Fourth ingredients', 0, 1)
            )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/clearTable', methods = ['POST'])
def remove():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ingredients  ")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/updateRecipes')
def updateRecipes():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    print(ingredients)
    conn.close()

    
    return redirect(url_for('index'))

if __name__ == '__main__':
    ingredients = ["chicken", "tomato", "carrots", "lime", "onions", "garlic clove"]
    get_meals_by_expire(ingredients)
    app.run(debug=True)