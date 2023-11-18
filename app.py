import sqlite3
from flask import Flask, render_template, redirect, url_for, request
import sys

from mealRequests import *
from mealObjects import *

from datetime import datetime



app = Flask(__name__)


recipes = []
recipeIds =[]
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
    collection = []
    exp_ing = []
    ret_ing = []
    exp_days = []
    ret_days = []
    e_ids = []
    i_ids = []
    for item in ingredients:
        ing = item['ingredient']
        expiry = item['expiry']
        id = item['id']
        day = shortest_date_interval(datetime.today().strftime('%Y-%m-%d'), expiry)
        collection.append([ing, day, id])
    collection.sort(key=lambda x: x[1], reverse=False)
    if len(collection) > 10:
        collection = collection[:10]
    for datapoint in collection:
        if datapoint[1] <= 5:
            exp_ing.append(datapoint[0])
            exp_days.append(datapoint[1])
            e_ids.append(datapoint[2])
        else:
            ret_ing.append(datapoint[0])
            ret_days.append(datapoint[1])
            i_ids.append(datapoint[2])  
    return render_template('index.html', post=ret_ing, days=ret_days, exp=exp_ing, eDays=exp_days, data=recipes, e_ids=e_ids, i_ids=i_ids)

@app.route('/add', methods = ['POST'])
def add():
    conn =get_db_connection()
    cur = conn.cursor()
    ingredients =  request.form['iList']
    expiries = request.form['eList']
    ingredient_list = ingredients.split(',')
    expiry_list = expiries.split(',')
    for i in range(len(ingredient_list)):
        ingredient = ingredient_list[i]
        expiry = expiry_list[i]
        if ingredient != "" and expiry != "":
            cur.execute("INSERT INTO ingredients (ingredient, expiry) VALUES (?, ?)",
                (ingredient, expiry)
                )

    conn.commit()
    recipes.clear()
    return redirect(url_for('index'))

@app.route('/updateIngredients', methods = ['POST'])
def updateIngredients():
    conn = get_db_connection()  
    cur = conn.cursor()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    print(ingredients)
    id_list = []
    for item in ingredients:
        id_list.append(str(item['id']))
    for id in id_list:
        print(id)
        try:
            deleted = request.form[id]
            if deleted == 'on':
                cur.execute("DELETE FROM ingredients WHERE id = ?", (id,))
                conn.commit()
        except:
            pass
    conn.close()
    recipes.clear()
    return redirect(url_for('index'))


@app.route('/updateRecipes', methods = ['POST'])
def updateRecipes():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
    i_list = []
    e_list = []
    recipes.clear()
    for item in ingredients:
        i_list.append(item['ingredient'])
        expiry = item['expiry']
        day = shortest_date_interval(datetime.today().strftime('%Y-%m-%d'), expiry)
        if day <= 5:
            e_list.append(item['ingredient'])
    print(i_list)
    meals = get_meals_by_ingredients(e_list)
    if meals == []:
        meals = get_meals_by_ingredients(i_list)

    ranked_meals = rank_meals(meals, i_list, e_list)
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