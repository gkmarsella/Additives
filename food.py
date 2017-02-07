class Food():
    count = 1

    def __init__(self,brand,name,ingredients):
        self.brand = brand
        self.name = name
        self.ingredients = ingredients
        self.id = Food.count
        Food.count += 1