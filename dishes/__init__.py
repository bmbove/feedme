import random
import requests as req
from bs4 import BeautifulSoup
from math import ceil
from recipes import Recipe

class Dish:

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.url = 'http://allrecipes.com/Recipes/Main-Dish/%s/Main.aspx' % name

class DishCollection:

    def __init__(self):
        self._weight_sum = 0
        self.dishes = [] 

    def add(self, name, weight):
        if not self.exists(name):
            dishes = self._unnormalize(self.dishes)
            dish = Dish(name, weight)
            dishes.append(dish)
            self.dishes = self._normalize(dishes)

    def remove(self, name):
        for d in self.dishes:
            if d.name == name:
                self.dishes.remove(d)
                break

    def _unnormalize(self, dishes):
        for i in range(0, len(dishes)):
            dishes[i].weight *= self._weight_sum 
        self._weight_sum = 0
        return dishes

    def _normalize(self, dishes):
        for d in dishes:
            self._weight_sum += d.weight
        for i in range(0, len(dishes)):
            dishes[i].weight /= self._weight_sum 
        return dishes

    def exists(self, name):
        for d in self.dishes:
            if d.name == name:
                return True
        return False

    def print_all(self):
        for d in self.dishes:
            print('Name: %20s Weight: %10.2f' % (d.name, d.weight))

    def pick_recipe(self):
        # pick random (weighted) dish type
        dish = self._pick_dish()
        # grab search page for type
        resp = req.get(dish.url)
        per_page = 20
        soup = BeautifulSoup(resp.text)
        # count results
        results = soup.find('p', {'class': 'searchResultsCount results'})
        count = int(results.find('span').text.replace(',', ''))
        # calculate number of pages
        pages = ceil(count/20)
        rating = 0

        while rating < 4:
            # grab random page
            page = random.randint(1, pages)
            resp = req.get(dish.url, params={'Page': page})
            soup = BeautifulSoup(resp.text)
            results = soup.findAll('div', {'class': 'recipe-info'})
            # grab link to random recipe on page
            recipe_num = random.randint(0, len(results)-1)
            result = results[recipe_num]
            url = 'http://www.allrecipes.com' + result.p.a.get('href')
            # grab the recipe
            try:
                recipe = Recipe(url=url)
                rating = recipe.rating
            except:
                rating = 0

        return recipe


    def _pick_dish(self):
        population = [d for d in self.dishes for i in range(ceil(d.weight*100))]
        return random.choice(population)
