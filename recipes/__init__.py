import re
import requests as req
from bs4 import BeautifulSoup

#url = 'http://allrecipes.com/Recipe/Homemade-Chicken-Enchiladas/Detail.aspx?evt19=1&referringHubId=201'

class Recipe:

    def __init__(self, **kwargs):
        self.url = None
        if 'url' in kwargs:
            self.url = kwargs['url']
            self.get_recipe()

    def get_recipe(self):
        url = self.url
        resp = req.get(url)
        html = resp.text
        soup = BeautifulSoup(html)
        results = self._parse(soup)
        self.name = results['name']
        self.instructions = results['instructions']
        self.ingredients = results['ingredients']
        self.reviews = results['reviews']
        self.rating = results['rating']

    def _parse(self, soup):

        # name 
        name = soup.find(id='lblTitle').text

        # ingredients
        ingredients = []
        results = soup.findAll('p', {'itemprop' : 'ingredients'})
        for r in results:
            ing_name = r.find(id='lblIngName').text
            amount_e = r.find(id='lblIngAmount')
            if(amount_e):
                amount = amount_e.text
            else:
                amount = ''
            ingredients.append({'name': ing_name, 'amount': amount})

        # instructions
        instructions = []
        results = soup.find('div', {'itemprop' : 'recipeInstructions'})
        results = results.findAll('span', {'class': 'plaincharacterwrap break'})
        for r in results:
            instructions.append(r.text)

        # reviews
        reviews = []
        results = soup.findAll(id='reviewTile')
        for rev in results:
            reviews.append(rev.find(id='pReviewText').text)

        # rating
        try:
            rating = soup.find('meta', {'itemprop': 'ratingValue'}).get('content')
        except:
            rating = 0

        return {
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions,
            'reviews': reviews,
            'rating': float(rating)
        }
