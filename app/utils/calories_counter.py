
def calories_counter(obj):
    calories = 0
    calories += obj.sandwich.calories - 200
    calories += obj.bread.calories
    calories += obj.cheese.calories
    for i in obj.toppings.all():
        if i.calories:
            calories += i.calories
    for i in obj.sauces.all():
        if i.calories:
            calories += i.calories
    for i in obj.vegetables.all():
        if i.calories:
            calories += i.calories

    # double cheese process
    if obj.toppings.filter(name='더블 치즈'):
        calories += obj.cheese.calories

    # double up process
    if obj.toppings.filter(name='더블업'):
        for i in obj.sandwich.main_ingredient.all():
            if i.calories:
                calories += i.calories

    return calories
