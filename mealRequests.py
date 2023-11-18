import requests
from urllib import parse
from fuzzywuzzy import fuzz


from mealObjects import Category, Meal, Recipe, Area

def get_meals_by_category(category):
    url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=' + category
    meals = []

    try:
        data = requests.get(url).json()
        for item in data['meals']:
            meal = Meal(item['idMeal'],
                        item['strMeal'],
                        item['strMealThumb'])
            meals.append(meal)
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return meals

def get_recipe_by_name(meal):
    url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=' + parse.quote(meal)
    recipe = None
    try:
        data = requests.get(url).json()   
        for recipe_data in data['meals']:
            recipe = Recipe(recipe_data['idMeal'],
                            recipe_data['strMeal'],
                            recipe_data['strCategory'],
                            recipe_data['strInstructions'],
                            recipe_data['strMealThumb'])
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

    return recipe

def get_meals_by_ingredient(ingredient):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=" + parse.quote(ingredient)
    meals = []
    try:
        data = requests.get(url).json()
        for item in data['meals']:
            meal = Meal(item['idMeal'],
                        item['strMeal'],
                        item['strMealThumb'])
            meals.append(meal)
    except (ValueError, KeyError, TypeError):
        print("JSON format erro")
    return meals

def get_ingredients_by_id(id):
    url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + id
    ingredients = []
    try:
        data = requests.get(url).json()
        for item in data['meals']:
            for i in range(1, 21):
                if (item[f'strIngredient{i}'] != "" and item[f'strIngredient{i}'] != None):
                    ingredients.append(item[f'strIngredient{i}'])
    except (ValueError, KeyError, TypeError):
        print("JSON format error")
    return ingredients

def compare(str1, str2, threshold=70):
    similarity_score = fuzz.partial_ratio(str1, str2)
    return similarity_score >= threshold

def get_suitability(meal, user_ingredients):
    suitability = 0
    meal_ingredients = get_ingredients_by_id(meal.get_id())
    i_length = len(meal_ingredients)
    for i in range(len(user_ingredients)):
        for j in range(len(meal_ingredients)):
            if compare(user_ingredients[i], meal_ingredients[j]):
                suitability += 1
    suitability = suitability/i_length
    return suitability

def rank_meals(meals, user_ingredients):
    ranked_meals = []
    for meal in meals:
        ranked_meals.append((meal, get_suitability(meal, user_ingredients)))
    ranked_meals.sort(key=lambda x: x[1], reverse=True)
    return ranked_meals

def get_meals_by_expire(expiring):
    meals = []
    ids = []
    for ingredient in expiring:
        temp = get_meals_by_ingredient(ingredient)
        for meal in temp:
            id = meal.get_id()
            if id not in ids:
                meals.append(meal)
                ids.append(id)
    return meals

def get_meal_names(meals):
    names = []
    for meal in meals:
        names.append(meal.get_meal())
    return names

