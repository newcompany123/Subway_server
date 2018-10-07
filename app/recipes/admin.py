from django.contrib import admin

from .models import (
    Recipe,
    RecipeName,
    LikedRecipe,
    BookmarkedRecipe,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sandwich', 'inventor', 'created_date', 'modified_date')


class RecipeNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeName, RecipeNameAdmin)
admin.site.register(LikedRecipe)
admin.site.register(BookmarkedRecipe)
