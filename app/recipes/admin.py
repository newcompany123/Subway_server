from django.contrib import admin

from .models import (
    Recipe,
    Like,
    Bookmark,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sandwich', 'inventor', 'created_date', 'modified_date')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Like)
admin.site.register(Bookmark)
