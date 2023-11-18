from mealObjects import *
from mealRequests import *

user_ingredients = ["chicken", "tomato", "carrots", "lime", "onions", "garlic clove"]

expire = ["chicken", "tomato"]

meals=get_meals_by_expire(expire)

items = rank_meals(meals, user_ingredients)

for item in items:
    print(item[0].get_meal(), item[1])