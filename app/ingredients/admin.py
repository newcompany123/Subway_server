from django.contrib import admin

from .models import (
    Sandwich,
    MainIngredient,
    Bread,
    Cheese,
    Toasting,
    Vegetables,
    Toppings,
    Sauces,
)

admin.site.register(Sandwich)
admin.site.register(MainIngredient)
admin.site.register(Bread)
admin.site.register(Cheese)
admin.site.register(Toasting)
admin.site.register(Vegetables)
admin.site.register(Toppings)
admin.site.register(Sauces)
