from django.core.management import BaseCommand

from ...models import Vegetables


class Command(BaseCommand):
    def handle(self, *args, **options):
        vegetable_list = ['Tomatoes', 'Lettuce', 'Cucumbers', 'Peppers', 'Red Onions', 'Pickles', 'Olives', 'Jalapenos', 'Avocado']

        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
