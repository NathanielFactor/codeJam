class Category:
    def __init__(self, category):
        self.category = category
    def get_category(self):
        return self.category
    def set_category(self, category):
        self.category = category

class Meal:
    def __init__(self, id, meal, thumbnail):
        self.id = id
        self.meal = meal
        self.thumbnail = thumbnail

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
        
    def get_meal(self):
        return self.meal
    
    def set_meal(self, meal):
        self.meal = meal
    
    def get_thumbnail(self):
        return self.thumbnail
    
    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def __str__(self):
        return f'{self.id} {self.meal} {self.thumbnail}'

class Recipe:
    def __init__(self, id, meal, category, instructions, thumbnail):
        self.id = id
        self.meal = meal
        self.category = category
        self.instructions = instructions
        self.thumbnail = thumbnail

    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
        
    def get_meal(self):
        return self.meal
    
    def set_meal(self, meal):
        self.meal = meal
    
    def get_category(self):
        return self.category
    
    def set_category(self, category):
        self.category = category
    
    def get_instructions(self):
        return self.instructions
    
    def set_instructions(self, instructions):
        self.instructions = instructions
    
    def get_thumbnail(self):
        return self.thumbnail
    
    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def __str__(self):
        return f'{self.id} {self.meal} {self.category} {self.instructions} {self.thumbnail}'

class Area:
    def __init__(self, area):
        self.area = area
    
    def get_area(self):
        return self.area
    
    def set_area(self, area):
        self.area = area