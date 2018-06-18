from django.contrib import admin

from .models import (
    Recipe,
    Vegetables,
)

admin.site.register(Recipe)
admin.site.register(Vegetables)
