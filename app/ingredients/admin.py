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


class SandwichAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering_num')


admin.site.register(Sandwich, SandwichAdmin)
admin.site.register(MainIngredient)
admin.site.register(Bread)
admin.site.register(Cheese)
admin.site.register(Toasting)
admin.site.register(Vegetables)
admin.site.register(Toppings)
admin.site.register(Sauces)
