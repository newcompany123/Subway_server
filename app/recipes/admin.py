from django.contrib import admin

from .models import (
    Recipe,
    Vegetables,
    Sandwich,
    Bread,
    RecipeName
)

admin.site.register(Recipe)
admin.site.register(Sandwich)
admin.site.register(Bread)
admin.site.register(Vegetables)
admin.site.register(RecipeName)
