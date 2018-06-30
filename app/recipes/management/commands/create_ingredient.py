from django.conf import settings
from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from ...models import Vegetables, Bread, RecipeName, Sandwich, Cheese, Toppings, Sauces, MainIngredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        recipe_name_list = ['sandwich1',
                            'sandwich2',
                            'sandwich3',
                            'sandwich4',
                            'sandwich5',
                            ]

        sandwich_list = ['b_l_t',
                         'bacon_egg_cheese',
                         'black_forest_ham_egg_cheese',
                         'chicken_bacon_ranch',
                         'chicken_teriyaki',
                         'egg_mayo',
                         'ham',
                         'italian_b_m_t',
                         'meatball',
                         'pulled_pork',
                         'roasted_beef',
                         'roasted_chicken',
                         'rotisserie_chicken',
                         'spicy_italian_avocado',
                         'spicy_italian',
                         'steak_cheese',
                         'steak_egg_cheese',
                         'subway_club',
                         'subway_melt',
                         'tuna',
                         'turkey_bacon_avocado',
                         'turkey_bacon',
                         'turkey',
                         'veggie_avocado',
                         'veggie_delite',
                         'western_egg_cheese',
                         ]

        main_ingredients_list = ['all_veggies',
                                 'chicken_breast',
                                 'ham',
                                 'meat_ball',
                                 'mian_chicken_strip',
                                 'pepperoni',
                                 'pulled_pork',
                                 'roast_beef',
                                 'rotisserie_chicken',
                                 'salami',
                                 'steak',
                                 'teriyaki',
                                 'tuna',
                                 'turkey',

                                 'avocado',     # topping
                                 'bacon',       # topping
                                 'egg_mayo',    # topping
                                 'omelet',      # topping

                                 'american_cheese',   # cheese
                                 ]

        bread_list = ['flat_bread',
                      'hearty_italian',
                      'honey_oat',
                      'parmesan_oregano',
                      'wheat',
                      'white',
                      ]

        cheese_list = ['american_cheese',
                       'shrewd_cheese',
                       ]

        vegetable_list = ['cucumbers',
                          'jalapenos',
                          'lettuce',
                          'olives',
                          'peppers',
                          'pickles',
                          'red_onions',
                          'tomatoes',
                          # 'avocado',
                          ]

        topping_list = ['avocado',
                        'bacon',
                        'double_up',
                        'egg_mayo',
                        'omelet',
                        ]

        sauce_list = ['black_pepper',
                      'chipotle',
                      'honey_mustard',
                      'horseradish',
                      'hot_chilli',
                      'italian_dressing',
                      'mayonnaise',
                      'olive_oil',
                      'ranch',
                      'red_wine_vinaigrette',
                      'salt',
                      'smoke_bbq',
                      'sweet_chilli',
                      'sweet_onion',
                      'thousand_island',
                      'yellow_mustard',
                      ]

        def get_or_create_and_save_images(class_name, folder_name, obj_name_list):
            for obj_name in obj_name_list:
                obj, _ = class_name.objects.get_or_create(name=obj_name)

                image_path = folder_name + obj_name + '.png'
                image_path3x = folder_name + obj_name + '@3x.png'

                static_storage_class = import_string(settings.STATICFILES_STORAGE)
                static_storage = static_storage_class()

                image_url = static_storage.url(image_path)
                image_url3x = static_storage.url(image_path3x)
                obj.image = image_url
                obj.image3x = image_url3x
                obj.save()

        get_or_create_and_save_images(MainIngredient, 'main_ingredient/', main_ingredients_list)

        [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]
        # [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        [Bread.objects.get_or_create(name=name) for name in bread_list]
        [Cheese.objects.get_or_create(name=name) for name in cheese_list]
        [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        [Toppings.objects.get_or_create(name=name) for name in topping_list]
        [Sauces.objects.get_or_create(name=name) for name in sauce_list]

        for name in sandwich_list:
            sandwich, _ = Sandwich.objects.get_or_create(name=name)

            # 1) Sandwich 인스턴스 생성 후 image url path 저장
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

            # 2) Sandwich 인스턴스 생성 후 Main Ingredient 저장





        # get_or_create_and_save_images(Sandwich, sandwich_list)
