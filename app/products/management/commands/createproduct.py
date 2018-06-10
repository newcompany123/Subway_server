from django.core.management import BaseCommand

from ...models import Vegetables, Bread, ProductName


class Command(BaseCommand):
    def handle(self, *args, **options):
        vegetable_list = ['Lettuce', 'Tomatoes', 'Cucumbers', 'Peppers', 'Red Onions', 'Pickles', 'Olives', 'Jalapenos', 'Avocado']
        bread_list = ['Honey Oat', 'Hearty Italian', 'Wheat', 'Parmesan Oregano', 'White', 'Flat Bread']
        productname_list = ['샌드위치이름1', '샌드위치이름2', '샌드위치이름3', '샌드위치이름4', '샌드위치이름5']

        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Bread.objects.get_or_create(name=name) for name in bread_list]
        [ProductName.objects.get_or_create(name=name) for name in productname_list]
