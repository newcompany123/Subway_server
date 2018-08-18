from django.contrib import admin

from .models import (
    Recipe,
    RecipeName,
    LikedRecipe,
    BookmarkedRecipe,
)

admin.site.register(Recipe)
admin.site.register(RecipeName)
admin.site.register(LikedRecipe)
admin.site.register(BookmarkedRecipe)
