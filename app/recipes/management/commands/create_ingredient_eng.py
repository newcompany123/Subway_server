from django.conf import settings
from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from ingredients.models import Bread, Toppings, Cheese, Toasting, Vegetables, Sauces, Sandwich, Category, MainIngredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        recipe_name_list = ['sandwich1',
                            'sandwich2',
                            'sandwich3',
                            'sandwich4',
                            'sandwich5',
                            'sandwich6',
                            'sandwich7',
                            'sandwich8',
                            'sandwich9',
                            'sandwich10',
                            ]

        sandwich_list = ['Spicy Italian Avocado',
                         'Turkey Bacon Avocado',
                         'Veggie Avocado',
                         'Pulled Pork',
                         'Egg Mayo',
                         'Italian B.M.T',
                         'B.L.T',
                         'Meatball',
                         'Ham',
                         'Tuna',
                         'Rotisserie Chicken',
                         'Roasted Chicken',
                         'Roasted Beef',
                         'Subway Club',
                         'Turkey',
                         'Veggie Delite',
                         'Steak & Cheese',
                         'Chicken Bacon Ranch',
                         'Subway Melt',
                         'Turkey Bacon',
                         'Spicy Italian',
                         'Chicken Teriyaki',
                         'Black Forest Ham & Egg, Cheese',
                         'Western, Egg & Cheese',
                         'Bacon, Egg & Cheese',
                         'Steak, Egg & Cheese',
                         ]

        # main_ingredients는 get_or_create를 사용하지 않고,
        #   get_or_create_for_main_ingredient를 활용해 직접 생성
        main_ingredients_list = ['All Veggies',
                                 'Cheese',

                                 'Chicken Breast',
                                 'Chicken Strip',
                                 'Chicken Teriyaki',
                                 'Ham',
                                 'Meatball',
                                 'Pepperoni',
                                 'Pulled Pork',
                                 'Roasted Beef',
                                 'Rotisserie Chicken',
                                 'Salami',
                                 'Steak',
                                 'Tuna',
                                 'Turkey',

                                 'Avocado',     # topping overlapped
                                 'Bacon',       # topping overlapped
                                 'Egg Mayo',    # topping overlapped
                                 'Omelet',      # topping overlapped
                                 ]

        bread_list = ['Flat Bread',
                      'Hearty Italian',
                      'Honey Oat',
                      'Parmesan Oregano',
                      'Wheat',
                      'White',
                      ]

        topping_list = ['Avocado',
                        'Bacon',
                        'Double Cheese',
                        'Double Up',
                        'Egg Mayo',
                        'Omelet',
                        ]

        cheese_list = ['American Cheese',
                       'No Cheese',
                       'Shredded Cheese',
                       ]

        toasting_list = ['Toasting',
                         'No Toasting',
                         ]

        vegetable_list = ['Cucumbers',
                          'Jalapenos',
                          'Lettuce',
                          'Olives',
                          'Peppers',
                          'Pickles',
                          'Red Onions',
                          'Tomatoes',
                          # 'Avocado',
                          ]

        sauce_list = ['Black Pepper',
                      'Chipotle',
                      'Honey Mustard',
                      'Horseradish',
                      'Hot Chilli',
                      'Italian Dressing',
                      'Mayonnaise',
                      'Olive Oil',
                      'Ranch',
                      'Red Wine Vinaigrette',
                      'Salt',
                      'Smoke BBQ',
                      'Sweet Chilli',
                      'Sweet Onion',
                      'Thousand Island',
                      'Yellow Mustard',
                      ]

        category_list = ['NEW',
                         'EVENT',
                         'CLASSIC',
                         'FRESH AND LIGHT',
                         'PREMIUM',
                         'BREAKFAST',
                         ]

        def get_or_create(class_name, folder_name, obj_name_list):
            for obj_name in obj_name_list:
                obj, _ = class_name.objects.get_or_create(name=obj_name)

                image_path = folder_name + obj_name.replace(' ', '_').lower() + '.png'
                image_path3x = folder_name + obj_name.replace(' ', '_').lower() + '@3x.png'

                static_storage_class = import_string(settings.STATICFILES_STORAGE)
                static_storage = static_storage_class()

                image_url = static_storage.url(image_path)
                image_url3x = static_storage.url(image_path3x)
                obj.image = image_url
                obj.image3x = image_url3x
                obj.save()

        def get_or_create_for_main_ingredient(obj_name, obj_quantity):
            obj, _ = MainIngredient.objects.get_or_create(name=obj_name, quantity=obj_quantity)

            image_path = 'main_ingredient/' + obj_name.replace(' ', '_').lower() + '.png'
            image_path3x = 'main_ingredient/' + obj_name.replace(' ', '_').lower() + '@3x.png'

            static_storage_class = import_string(settings.STATICFILES_STORAGE)
            static_storage = static_storage_class()

            image_url = static_storage.url(image_path)
            image_url3x = static_storage.url(image_path3x)
            obj.image = image_url
            obj.image3x = image_url3x
            obj.save()
            return obj

        # [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]
        # [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        # [Bread.objects.get_or_create(name=name) for name in bread_list]
        # [Toppings.objects.get_or_create(name=name) for name in topping_list]
        # [Cheese.objects.get_or_create(name=name) for name in cheese_list]
        # [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        # [Sauces.objects.get_or_create(name=name) for name in sauce_list]
        # [Category.objects.get_or_create(name=name) for name in category_list]

        get_or_create(Bread, 'bread/', bread_list)
        get_or_create(Toppings, 'toppings/', topping_list)
        get_or_create(Cheese, 'cheese/', cheese_list)
        get_or_create(Toasting, 'toasting/', toasting_list)
        get_or_create(Vegetables, 'vegetables/', vegetable_list)
        get_or_create(Sauces, 'sauces/', sauce_list)

        for name in sandwich_list:

            sandwich, _ = Sandwich.objects.get_or_create(name=name)

            # 1) Sandwich 인스턴스 생성 후 image url path 저장
            image_path_left = 'sandwich/left/' + name.replace(' ', '_').lower() + '.png'
            image_path3x_left = 'sandwich/left/' + name.replace(' ', '_').lower() + '@3x.png'

            image_path_right = 'sandwich/right/' + name.replace(' ', '_').lower() + '.png'
            image_path3x_right = 'sandwich/right/' + name.replace(' ', '_').lower() + '@3x.png'

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

            # 하단 과정에서
            # sandwich.save()

            if sandwich.name == 'Spicy Italian Avocado':
                pepperoni = get_or_create_for_main_ingredient('Pepperoni', '5 slices')
                salami = get_or_create_for_main_ingredient('Salami', '5 slices')
                avocado = get_or_create_for_main_ingredient('Avocado', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slice')

                # 2) Sandwich 인스턴스 생성 후 Main Ingredient field 저장
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    avocado,
                    cheese
                )
                # 3) Sandwich 인스턴스 생성 후 Category field 저장
                new, _ = Category.objects.get_or_create(name='NEW')
                event, _ = Category.objects.get_or_create(name='EVENT')
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    new,
                    event,
                    premium,
                )
                # 4) Sandwich 인스턴스 생성 후 ordering_num 설정
                sandwich.ordering_num = 1

            elif sandwich.name == 'Turkey Bacon Avocado':
                turkey = get_or_create_for_main_ingredient('Turkey', '3 slices')
                bacon = get_or_create_for_main_ingredient('Bacon', '2 slices')
                avocado = get_or_create_for_main_ingredient('Avocado', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    avocado,
                    cheese,
                )
                event, _ = Category.objects.get_or_create(name='EVENT')
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    event,
                    premium,
                )
                sandwich.ordering_num = 2

            elif sandwich.name == 'Veggie Avocado':
                all_veggies = get_or_create_for_main_ingredient('All Veggies', '')
                avocado = get_or_create_for_main_ingredient('Avocado', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    all_veggies,
                    avocado,
                    cheese,
                )
                new, _ = Category.objects.get_or_create(name='NEW')
                event, _ = Category.objects.get_or_create(name='EVENT')
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    new,
                    event,
                    fresh_and_light,
                )
                sandwich.ordering_num = 3

            elif sandwich.name == 'Pulled Pork':
                pulled_pork = get_or_create_for_main_ingredient('Pulled Pork', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    pulled_pork,
                    cheese,
                )
                new, _ = Category.objects.get_or_create(name='NEW')
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    new,
                    premium,
                )
                sandwich.ordering_num = 4

            elif sandwich.name == 'Egg Mayo':
                egg_mayo = get_or_create_for_main_ingredient('Egg Mayo', '2 scoops')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    egg_mayo,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 5

            elif sandwich.name == 'Italian B.M.T':
                pepperoni = get_or_create_for_main_ingredient('Pepperoni', '3 slices')
                salami = get_or_create_for_main_ingredient('Salami', '3 slices')
                ham = get_or_create_for_main_ingredient('Ham', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    ham,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 6

            elif sandwich.name == 'B.L.T':
                bacon = get_or_create_for_main_ingredient('Bacon', '4 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    bacon,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 7

            elif sandwich.name == 'Meatball':
                meatball = get_or_create_for_main_ingredient('Meatball', '4 piece')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    meatball,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 8

            elif sandwich.name == 'Ham':
                ham = get_or_create_for_main_ingredient('Ham', '4 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    ham,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 9

            elif sandwich.name == 'Tuna':
                tuna = get_or_create_for_main_ingredient('Tuna', '2 scoops')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    tuna,
                    cheese,
                )
                classic, _ = Category.objects.get_or_create(name='CLASSIC')
                sandwich.category.add(
                    classic,
                )
                sandwich.ordering_num = 10

            elif sandwich.name == 'Rotisserie Chicken':
                rotisserie_chicken = get_or_create_for_main_ingredient('Rotisserie Chicken', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    rotisserie_chicken,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 11

            elif sandwich.name == 'Roasted Chicken':
                chicken_breast = get_or_create_for_main_ingredient('Chicken Breast', '1 slice')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    chicken_breast,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 12

            elif sandwich.name == 'Roasted Beef':
                roasted_beef = get_or_create_for_main_ingredient('Roasted Beef', '3 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    roasted_beef,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 13

            elif sandwich.name == 'Subway Club':
                turkey = get_or_create_for_main_ingredient('Turkey', '2 slices')
                ham = get_or_create_for_main_ingredient('Ham', '1 slice')
                roasted_beef = get_or_create_for_main_ingredient('Roasted Beef', '1 slice')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    turkey,
                    ham,
                    roasted_beef,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 14

            elif sandwich.name == 'Turkey':
                turkey = get_or_create_for_main_ingredient('Turkey', '4 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    turkey,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH AND LIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 15

            elif sandwich.name == 'Veggie Delite':
                all_veggies = get_or_create_for_main_ingredient('All Veggies', '')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    all_veggies,
                    cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='FRESH_AND_RIGHT')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.ordering_num = 16

            elif sandwich.name == 'Steak & Cheese':
                steak = get_or_create_for_main_ingredient('Steak', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    steak,
                    cheese,
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 17

            elif sandwich.name == 'Chicken Bacon Ranch':
                chicken_strip = get_or_create_for_main_ingredient('Chicken Strip', '1 scoop')
                bacon = get_or_create_for_main_ingredient('Bacon', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    chicken_strip,
                    bacon,
                    cheese,
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 18

            elif sandwich.name == 'Subway Melt':
                turkey = get_or_create_for_main_ingredient('Turkey', '2 slices')
                bacon = get_or_create_for_main_ingredient('Bacon', '2 slices')
                ham = get_or_create_for_main_ingredient('Ham', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    ham,
                    cheese,
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 19

            elif sandwich.name == 'Turkey Bacon':
                turkey = get_or_create_for_main_ingredient('Turkey', '3 slices')
                bacon = get_or_create_for_main_ingredient('Bacon', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    cheese,
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 20

            elif sandwich.name == 'Spicy Italian':
                pepperoni = get_or_create_for_main_ingredient('Pepperoni', '5 slices')
                salami = get_or_create_for_main_ingredient('Salami', '5 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    cheese
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 21

            elif sandwich.name == 'Chicken Teriyaki':
                chicken_teriyaki = get_or_create_for_main_ingredient('Chicken Teriyaki', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    chicken_teriyaki,
                    cheese,
                )
                premium, _ = Category.objects.get_or_create(name='PREMIUM')
                sandwich.category.add(
                    premium,
                )
                sandwich.ordering_num = 22

            elif sandwich.name == 'Black Forest Ham & Egg, Cheese':
                omelet = get_or_create_for_main_ingredient('Omelet', '1 slice')
                ham = get_or_create_for_main_ingredient('Ham', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='Breakfast')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.ordering_num = 23

            elif sandwich.name == 'Western, Egg & Cheese':
                omelet = get_or_create_for_main_ingredient('Omelet', '1 slice')
                ham = get_or_create_for_main_ingredient('Ham', '1 slice')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='Breakfast')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.ordering_num = 24

            elif sandwich.name == 'Bacon, Egg & Cheese':
                omelet = get_or_create_for_main_ingredient('Omelet', '1 slice')
                bacon = get_or_create_for_main_ingredient('Bacon', '2 slices')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    omelet,
                    bacon,
                    cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='Breakfast')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.ordering_num = 25

            elif sandwich.name == 'Steak, Egg & Cheese':
                steak = get_or_create_for_main_ingredient('Steak', '1 scoop')
                omelet = get_or_create_for_main_ingredient('Omelet', '1 scoop')
                cheese = get_or_create_for_main_ingredient('Cheese', '2 slices')
                sandwich.main_ingredient.add(
                    steak,
                    omelet,
                    cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='Breakfast')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.ordering_num = 26

            sandwich.save()
