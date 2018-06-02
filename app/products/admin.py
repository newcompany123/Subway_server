from django.contrib import admin

from .models import (
    Product,
    Vegetables,
)

admin.site.register(Product)
admin.site.register(Vegetables)
