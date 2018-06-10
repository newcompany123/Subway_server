from django.core.management import BaseCommand

from ...models import Vegetables, Bread, ProductName, MainIngredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        vegetable_list = ['Lettuce', 'Tomatoes', 'Cucumbers', 'Peppers', 'Red Onions', 'Pickles', 'Olives', 'Jalapenos', 'Avocado']
        bread_list = ['Honey Oat', 'Hearty Italian', 'Wheat', 'Parmesan Oregano', 'White', 'Flat Bread']
        productname_list = ['Sandwich1', 'Sandwich2', 'Sandwich3', 'Sandwich4', 'Sandwich5']
        mainingredient_list = ['Spicy Italian Avocado', 'Turkey Bacon Avocado', 'Veggie Avocado', 'Pulled Pork',
                               'Egg Mayo', 'Italian B.M.T', 'B.L.T', 'Meatball', 'Ham', 'Tuna', 'Rotisserie Chicken', 'Roasted Chicken']

        [MainIngredient.objects.get_or_create(name=name) for name in mainingredient_list]
        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Bread.objects.get_or_create(name=name) for name in bread_list]
        [ProductName.objects.get_or_create(name=name) for name in productname_list]
