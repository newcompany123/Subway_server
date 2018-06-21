from django.core.management import BaseCommand

from ...models import Vegetables, Bread, RecipeName, Sandwich


class Command(BaseCommand):
    def handle(self, *args, **options):
        vegetable_list = ['lettuce', 'tomatoes', 'cucumbers', 'peppers', 'red_onions', 'pickles', 'olives', 'jalapenos', 'avocado']
        bread_list = ['honey_oat', 'hearty_italian', 'wheat', 'parmesan_oregano', 'white', 'flat_bread']
        recipe_name_list = ['sandwich1', 'sandwich2', 'sandwich3', 'sandwich4', 'sandwich5']
        sandwich_list = ['spicy_italian_avocado', 'turkey_bacon_avocado', 'veggie_avocado', 'pulled_pork',
                               'egg_mayo', 'italian_bmt', 'blt', 'meatball', 'ham', 'tuna', 'rotisserie_chicken', 'roasted_chicken', 'roasted_beef', 'subway_club', 'turkey', 'veggie_delite']
        # vegetable_list = ['Lettuce', 'Tomatoes', 'Cucumbers', 'Peppers', 'Red Onions', 'Pickles', 'Olives', 'Jalapenos', 'Avocado']
        # bread_list = ['Honey Oat', 'Hearty Italian', 'Wheat', 'Parmesan Oregano', 'White', 'Flat Bread']
        # recipe_name_list = ['Sandwich1', 'Sandwich2', 'Sandwich3', 'Sandwich4', 'Sandwich5']
        # sandwich_list = ['Spicy Italian Avocado', 'Turkey Bacon Avocado', 'Veggie Avocado', 'Pulled Pork',
        #                        'Egg Mayo', 'Italian B.M.T', 'B.L.T', 'Meatball', 'Ham', 'Tuna', 'Rotisserie Chicken', 'Roasted Chicken']

        [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Bread.objects.get_or_create(name=name) for name in bread_list]
        [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]
