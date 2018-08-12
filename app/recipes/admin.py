from django.contrib import admin

from .models import (
    Recipe,
    RecipeName,

    Sandwich,
    MainIngredient,
    Bread,
    Cheese,
    Toasting,
    Vegetables,
    Toppings,
    Sauces,

    LikedRecipe,
    BookmarkedRecipe,
)

admin.site.register(Recipe)
admin.site.register(RecipeName)

admin.site.register(Sandwich)
admin.site.register(MainIngredient)
admin.site.register(Bread)
admin.site.register(Cheese)
admin.site.register(Toasting)
admin.site.register(Vegetables)
admin.site.register(Toppings)
admin.site.register(Sauces)

admin.site.register(LikedRecipe)
admin.site.register(BookmarkedRecipe)
