from dishes import DishCollection

maindishes = DishCollection() 

maindishes.add('Chicken', 70)
maindishes.add('Pork', 35)
maindishes.add('Beef', 30)
maindishes.add('Seafood', 30)
maindishes.add('Pasta', 30)
maindishes.add('Gourmet', 30)
maindishes.add('Steaks-and-Chops', 10)
maindishes.add('Casseroles', 20)
maindishes.add('Sandwiches', 20)
maindishes.add('Burgers', 30)
maindishes.add('Stir-Fry', 30)
maindishes.add('Curries', 10)
maindishes.add('Turkey', 20)
maindishes.add('Soups-and-Stews', 10)

recipe = maindishes.pick_recipe()

print("Name: %s" % recipe.name)
print("Rating: %.2f\n\n" % recipe.rating)

print("Ingredients:")
for i in recipe.ingredients:
    print("%s %s" % (i['amount'], i['name']))

print("\n\nInstructions:")
for i in range(0, len(recipe.instructions)):
    ins = recipe.instructions[i]
    print("%d. %s\n" % (i+1, ins))
