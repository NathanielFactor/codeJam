import sqlite3
from flask import Flask, render_template, redirect, url_for, request
import sys

from mealRequests import *
from mealObjects import *

from datetime import datetime



app = Flask(__name__)


recipes = []
def shortest_date_interval(date_str1, date_str2):
    date1 = datetime.strptime(date_str1, '%Y-%m-%d')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d')
    delta = abs(date2 - date1)
    return delta.days
    

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    conn.close()
    return render_template('index.html', post=ingredients, data=recipes)

@app.route('/add', methods = ['POST'])
def add():
    conn =get_db_connection()
    cur = conn.cursor()
    ingredient =  request.form['ingredient']
    expiry = request.form['expdate']
    cur.execute("INSERT INTO ingredients (ingredient, expiry) VALUES (?, ?)",
           (ingredient, expiry)
           )

    #db stuff
    #cur.execute("INSERT INTO ingredients (ingredient, expiry, amount) VALUES (?, ?, ?)",
    #       ('Chicken', 0, 1)
    #       )

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

@app.route('/updateRecipes', methods = ['POST'])
def updateRecipes():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    i_list = []

    for item in ingredients:
        i_list.append(item['ingredient'])
    meals = get_meals_by_expire(i_list)
    ranked_meals = rank_meals(meals, i_list, i_list)
    names = get_meal_names(ranked_meals)
    if names != []:
        for name in names:
            recipes.append(name)
    else:
        recipes.clear()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)