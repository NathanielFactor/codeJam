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

def get_suitability(meal, user_ingredients, expiring):
    meal_ingredients = get_ingredients_by_id(meal.get_id())
    i_length = len(meal_ingredients)
    expire_length = len(expiring)
    suitability = 0
    expire_num = 0
    for i in range(len(user_ingredients)):
        for j in range(len(meal_ingredients)):
            if compare(user_ingredients[i], meal_ingredients[j]):
                if user_ingredients[i] in expiring:
                    expire_num += 1
                suitability += 1
                meal_ingredients.remove(meal_ingredients[j])
                break
    if i_length != 0:
        suitability = suitability/i_length
        print("previous " + str(suitability))
    if expire_length != 0:
        suitability = suitability*0.05 + (expire_num/expire_length)*0.95
        print("after " + str(suitability))
    return suitability

def rank_meals(meals, user_ingredients, expiring):
    if (user_ingredients == []):
        return []
    else:
        ranked_meals = [[meal, get_suitability(meal, user_ingredients, expiring)] for meal in meals]
        ranked_meals.sort(key=lambda x: x[1], reverse=True)
        if len(ranked_meals) > 10:
            ranked_meals = ranked_meals[:10]
        return_array = [ranked_meals[i][0] for i in range(len(ranked_meals))]
        return return_array

def get_meals_by_ingredients(ingredients):
    meals = []
    ids = []
    for ingredient in ingredients:
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

