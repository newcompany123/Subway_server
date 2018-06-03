from django.core.management import BaseCommand

from ...models import Vegetables, Breads


class Command(BaseCommand):
    def handle(self, *args, **options):
        vegetable_list = ['Lettuce', 'Tomatoes', 'Cucumbers', 'Peppers', 'Red Onions', 'Pickles', 'Olives', 'Jalapenos', 'Avocado']
        bread_list = ['Honey Oat', 'Hearty Italian', 'Wheat', 'Parmesan Oregano', 'White', 'Flat Bread']

        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Breads.objects.get_or_create(name=name) for name in bread_list]
