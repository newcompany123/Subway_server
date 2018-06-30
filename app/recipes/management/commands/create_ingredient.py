from django.conf import settings
from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from ...models import Vegetables, Bread, RecipeName, Sandwich, Cheese, Toppings, Sauces


class Command(BaseCommand):
    def handle(self, *args, **options):
        recipe_name_list = ['sandwich1', 'sandwich2', 'sandwich3', 'sandwich4', 'sandwich5']
        sandwich_list = ['spicy_italian_avocado', 'turkey_bacon_avocado', 'veggie_avocado', 'pulled_pork',
                         'egg_mayo', 'italian_bmt', 'blt', 'meatball', 'ham', 'tuna', 'rotisserie_chicken',
                         'roasted_chicken', 'roasted_beef', 'subway_club', 'turkey', 'veggie_delite', 'steak_&_cheese',
                         'chicken_&_bacon_ranch', 'subway_melt', 'turkey_bacon']
        bread_list = ['honey_oat', 'hearty_italian', 'wheat', 'parmesan_oregano', 'white', 'flat_bread']
        cheese_list = ['american_cheese', 'shrewd_cheese']
        vegetable_list = ['lettuce', 'tomatoes', 'cucumbers', 'peppers', 'red_onions', 'pickles', 'olives', 'jalapenos', 'avocado']
        topping_list = ['double_up', 'egg_mayo', 'omelet']
        sauce_list = ['ranch', 'mayonnaise', 'sweet_onion']

        [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]
        # [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        [Cheese.objects.get_or_create(name=name) for name in cheese_list]

        [Bread.objects.get_or_create(name=name) for name in bread_list]
        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Toppings.objects.get_or_create(name=name) for name in topping_list]
        [Sauces.objects.get_or_create(name=name) for name in sauce_list]

        for name in sandwich_list:
            sandwich, _ = Sandwich.objects.get_or_create(name=name)

            image_path = 'sandwich/' + name + '.png'
            image_path3x = 'sandwich/' + name + '@3x.png'

            static_storage_class = import_string(settings.STATICFILES_STORAGE)
            static_storage = static_storage_class()

            # ----------------------------------------
            # # 1안) ImageField에 imagefile 저장
            # static_file = static_storage.open(
            #     image_path
            # )
            # # *ImageFileField.save()로 아래처럼 settings에 따른 분기가 필요 없어짐.
            # # 1) settings = local (Local storage, SQLite)
            # # if SETTINGS_MODULE == 'config.settings.local':
            # #     sandwich.image.save(image_path, static_file)
            # # 2) settings = prod (Amazon RDS, S3)
            # # else:
            # #     sandwich.image = static_file
            # #     sandwich.save()
            #
            # sandwich.image.save(image_path, static_file)

            # ----------------------------------------
            #  2안) image url 경로 저장
            #   : url에 expire가 포함된 hash 같이 붙는 S3의 특성상 file_path만 저장할 수 없고
            #       hash값 자체를 없애는 것도 적절한 방법이라고 보기 힘들기 때문에
            #       저장하는 단계를 추가하더라도 아래의 방법을 선택하게 됨.
            #       -> 때문에 위 방법 선택을 안하려고 했는데
            #          규혁님과 토의후 지속적으로 url에 hash가 붙게되면
            #          클라이언트(모바일)에서 (기본적으로 하게 되어있는)
            #          캐싱을 하는 의미가 없이 새로 앱을 작동시킬 때마다
            #          이미지를 다시 받아오는 문제가 있어서 다시 이 방법으로 회귀
            #          (* 클라이언트에서 이미지 캐싱은 url 주소로 판단한다고 함)

            image_url = static_storage.url(image_path)
            image_url3x = static_storage.url(image_path3x)
            sandwich.image = image_url
            sandwich.image3x = image_url3x
            sandwich.save()
