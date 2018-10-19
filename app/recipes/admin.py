from django.contrib import admin

from recipe_name.models import RecipeName
from .models import (
    Recipe,
    Like,
    Bookmark,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sandwich', 'inventor', 'created_date', 'modified_date')


class RecipeNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeName, RecipeNameAdmin)
admin.site.register(Like)
admin.site.register(Bookmark)
