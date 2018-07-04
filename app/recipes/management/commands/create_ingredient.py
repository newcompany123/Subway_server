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

        # main_ingredients는 get_or_create를 사용하지 않고,
        #   get_or_create_for_main_ingredient를 활용해 직접 생성
        main_ingredients_list = ['all_veggies',
                                 'chicken_breast',
                                 'chicken_strip',
                                 'chicken_teriyaki',
                                 'ham',
                                 'meat_ball',
                                 'pepperoni',
                                 'pulled_pork',
                                 'roast_beef',
                                 'rotisserie_chicken',
                                 'salami',
                                 'steak',
                                 'tuna',
                                 'turkey',

                                 'avocado',     # topping overlapped
                                 'bacon',       # topping overlapped
                                 'egg_mayo',    # topping overlapped
                                 'omelet',      # topping overlapped

                                 # 'american_cheese',
                                 ]

        bread_list = ['flat_bread',
                      'hearty_italian',
                      'honey_oat',
                      'parmesan_oregano',
                      'wheat',
                      'white',
                      ]

        cheese_list = ['american_cheese',
                       'no_cheese',
                       'shrewd_cheese',
                       ]

        topping_list = ['american_cheese',
                        'avocado',
                        'bacon',
                        'double_up',
                        'egg_mayo',
                        'omelet',
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

        def get_or_create(class_name, folder_name, obj_name_list):
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

        def get_or_create_for_main_ingredient(obj_name, obj_quantity):
            obj, _ = MainIngredient.objects.get_or_create(name=obj_name, quantity=obj_quantity)

            image_path = 'main_ingredient/' + obj_name + '.png'
            image_path3x = 'main_ingredient/' + obj_name + '@3x.png'

            static_storage_class = import_string(settings.STATICFILES_STORAGE)
            static_storage = static_storage_class()

            image_url = static_storage.url(image_path)
            image_url3x = static_storage.url(image_path3x)
            obj.image = image_url
            obj.image3x = image_url3x
            obj.save()
            return obj

        [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]
        # [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        # [Bread.objects.get_or_create(name=name) for name in bread_list]
        # [Cheese.objects.get_or_create(name=name) for name in cheese_list]
        # [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        # [Toppings.objects.get_or_create(name=name) for name in topping_list]
        # [Sauces.objects.get_or_create(name=name) for name in sauce_list]

        get_or_create(Bread, 'bread/', bread_list)
        get_or_create(Cheese, 'cheese/', cheese_list)
        get_or_create(Toppings, 'toppings/', topping_list)
        get_or_create(Vegetables, 'vegetables/', vegetable_list)
        get_or_create(Sauces, 'sauces/', sauce_list)

        for name in sandwich_list:
            sandwich, _ = Sandwich.objects.get_or_create(name=name)

            # 1) Sandwich 인스턴스 생성 후 image url path 저장
            image_path_left = 'sandwich/left/' + name + '.png'
            image_path3x_left = 'sandwich/left/' + name + '@3x.png'

            image_path_right = 'sandwich/right/' + name + '.png'
            image_path3x_right = 'sandwich/right/' + name + '@3x.png'

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

            image_url_left = static_storage.url(image_path_left)
            image_url3x_left = static_storage.url(image_path3x_left)
            sandwich.image_left = image_url_left
            sandwich.image3x_left = image_url3x_left

            image_url_right = static_storage.url(image_path_right)
            image_url3x_right = static_storage.url(image_path3x_right)
            sandwich.image_right = image_url_right
            sandwich.image3x_right = image_url3x_right

            sandwich.save()

            # 2) Sandwich 인스턴스 생성 후 Main Ingredient 저장
            if sandwich.name == 'b_l_t':
                bacon = get_or_create_for_main_ingredient('bacon', '4_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    bacon,
                    # american_cheese,
                )
            elif sandwich.name == 'bacon_egg_cheese':
                omelet = get_or_create_for_main_ingredient('omelet', '1_slice')
                bacon = get_or_create_for_main_ingredient('bacon', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    omelet,
                    bacon,
                    # american_cheese,
                )
            elif sandwich.name == 'black_forest_ham_egg_cheese':
                omelet = get_or_create_for_main_ingredient('omelet', '1_slice')
                ham = get_or_create_for_main_ingredient('ham', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    # american_cheese,
                )
            elif sandwich.name == 'chicken_bacon_ranch':
                chicken_strip = get_or_create_for_main_ingredient('chicken_strip', '1_scoop')
                bacon = get_or_create_for_main_ingredient('bacon', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    chicken_strip,
                    bacon,
                    # american_cheese,
                )
            elif sandwich.name == 'chicken_teriyaki':
                chicken_strip = get_or_create_for_main_ingredient('chicken_teriyaki', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    chicken_strip,
                    # american_cheese,
                )
            elif sandwich.name == 'egg_mayo':
                egg_mayo = get_or_create_for_main_ingredient('egg_mayo', '2_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    egg_mayo,
                    # american_cheese,
                )
            elif sandwich.name == 'ham':
                ham = get_or_create_for_main_ingredient('ham', '4_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    ham,
                    # american_cheese,
                )
            elif sandwich.name == 'italian_b_m_t':
                pepperoni = get_or_create_for_main_ingredient('pepperoni', '3_slice')
                salami = get_or_create_for_main_ingredient('salami', '3_slice')
                ham = get_or_create_for_main_ingredient('ham', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    ham,
                    # american_cheese,
                )
            elif sandwich.name == 'meatball':
                meat_ball = get_or_create_for_main_ingredient('meat_ball', '4_piece')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    meat_ball,
                    # american_cheese,
                )
            elif sandwich.name == 'pulled_pork':
                pulled_pork = get_or_create_for_main_ingredient('pulled_pork', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    pulled_pork,
                    # american_cheese,
                )
            elif sandwich.name == 'roasted_beef':
                roast_beef = get_or_create_for_main_ingredient('roast_beef', '3_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    roast_beef,
                    # american_cheese,
                )
            elif sandwich.name == 'roasted_chicken':
                chicken_breast = get_or_create_for_main_ingredient('chicken_breast', '1_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    chicken_breast,
                    # american_cheese,
                )
            elif sandwich.name == 'rotisserie_chicken':
                rotisserie_chicken = get_or_create_for_main_ingredient('rotisserie_chicken', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    rotisserie_chicken,
                    # american_cheese,
                )
            elif sandwich.name == 'spicy_italian_avocado':
                pepperoni = get_or_create_for_main_ingredient('pepperoni', '5_slice')
                salami = get_or_create_for_main_ingredient('salami', '5_slice')
                avocado = get_or_create_for_main_ingredient('avocado', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    avocado,
                    # american_cheese
                )
            elif sandwich.name == 'spicy_italian':
                pepperoni = get_or_create_for_main_ingredient('pepperoni', '5_slice')
                salami = get_or_create_for_main_ingredient('salami', '5_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    # american_cheese
                )
            elif sandwich.name == 'steak_cheese':
                steak = get_or_create_for_main_ingredient('steak', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    steak,
                    # american_cheese,
                )
            elif sandwich.name == 'steak_egg_cheese':
                steak = get_or_create_for_main_ingredient('steak', '1_scoop')
                omelet = get_or_create_for_main_ingredient('omelet', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    steak,
                    omelet,
                    # american_cheese,
                )
            elif sandwich.name == 'subway_club':
                turkey = get_or_create_for_main_ingredient('turkey', '2_slice')
                ham = get_or_create_for_main_ingredient('ham', '1_slice')
                roast_beef = get_or_create_for_main_ingredient('roast_beef', '1_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    turkey,
                    ham,
                    roast_beef,
                    # american_cheese,
                )
            elif sandwich.name == 'subway_melt':
                turkey = get_or_create_for_main_ingredient('turkey', '2_slice')
                bacon = get_or_create_for_main_ingredient('bacon', '2_slice')
                ham = get_or_create_for_main_ingredient('ham', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    ham,
                    # american_cheese,
                )
            elif sandwich.name == 'tuna':
                tuna = get_or_create_for_main_ingredient('tuna', '2_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    tuna,
                    # american_cheese,
                )
            elif sandwich.name == 'turkey_bacon_avocado':
                turkey = get_or_create_for_main_ingredient('turkey', '3_slice')
                bacon = get_or_create_for_main_ingredient('bacon', '2_slice')
                avocado = get_or_create_for_main_ingredient('avocado', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    avocado,
                    # american_cheese,
                )
            elif sandwich.name == 'turkey_bacon':
                turkey = get_or_create_for_main_ingredient('turkey', '3_slice')
                bacon = get_or_create_for_main_ingredient('bacon', '2_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    # american_cheese,
                )
            elif sandwich.name == 'turkey':
                turkey = get_or_create_for_main_ingredient('turkey', '4_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    turkey,
                    # american_cheese,
                )
            elif sandwich.name == 'veggie_avocado':
                all_veggies = get_or_create_for_main_ingredient('all_veggies', '')
                avocado = get_or_create_for_main_ingredient('avocado', '1_scoop')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    all_veggies,
                    avocado,
                    # american_cheese,
                )
            elif sandwich.name == 'veggie_delite':
                all_veggies = get_or_create_for_main_ingredient('all_veggies', '')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    all_veggies,
                    # american_cheese,
                )
            elif sandwich.name == 'western_egg_cheese':
                omelet = get_or_create_for_main_ingredient('omelet', '1_slice')
                ham = get_or_create_for_main_ingredient('ham', '1_slice')
                # american_cheese = get_or_create_for_main_ingredient('american_cheese', '2_slice')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    # american_cheese,
                )
