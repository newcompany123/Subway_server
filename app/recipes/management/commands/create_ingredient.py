from django.conf import settings
from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from ingredients.models import Bread, Toppings, Cheese, Toasting, Vegetables, Sauces, Sandwich, Category, MainIngredient
from utils.localization import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        # recipe_name_list = ['샌드위치1',
        #                     '샌드위치2',
        #                     '샌드위치3',
        #                     '샌드위치4',
        #                     '샌드위치5',
        #                     ]

        sandwich_list = ['로티세리 치킨',
                         '풀드포크',
                         '에그마요',
                         '이탈리안 비엠티',
                         '비엘티',
                         '미트볼',
                         '햄',
                         '참치',
                         '로스트 치킨',
                         '로스트 비프',
                         '써브웨이 클럽',
                         '터키',
                         '베지',
                         '스테이크 & 치즈',
                         '터키 베이컨 아보카도',
                         '치킨 베이컨 랜치',
                         '써브웨이 멜트',
                         '터키 베이컨',
                         '스파이시 이탈리안',
                         '치킨 데리야끼',
                         '블랙 포레스트햄 & 에그, 치즈',
                         '웨스턴, 에그 & 치즈',
                         '베이컨, 에그 & 치즈',
                         '스테이크, 에그 & 치즈',
                         ]

        # main_ingredients는 get_or_create를 사용하지 않고,
        #   get_or_create_for_main_ingredient를 활용해 직접 생성
        # main_ingredients_list = ['각종 야채',
        #                          '치즈',
        #
        #                          '치킨 브레스트',
        #                          '치킨 스트립',
        #                          '치킨 데리야끼',
        #                          '햄',
        #                          '미트볼',
        #                          '페퍼로니',
        #                          '풀드포크',
        #                          '로스트 비프',
        #                          '로티세리 치킨',
        #                          '살라미',
        #                          '스테이크',
        #                          '참치',
        #                          '터키',
        #
        #                          '아보카도',     # topping overlapped
        #                          '베이컨',       # topping overlapped
        #                          '에그마요',    # topping overlapped
        #                          '오믈렛',      # topping overlapped
        #                          ]
        main_ingredients_dict = {'각종 야채': 30,
                                 '치킨 브레스트': 120,
                                 '치킨 스트립': 330,
                                 '치킨 데리야끼': 170,
                                 '햄': 20,
                                 '미트볼': 70,
                                 '페퍼로니': 30,
                                 '풀드포크': 220,
                                 '로스트 비프': 40,
                                 '로티세리 치킨': 150,
                                 '살라미': 30,
                                 '스테이크': 180,
                                 '참치': 140,
                                 '터키': 20,

                                 # topping overlapped
                                 '아보카도': 60,
                                 '베이컨': 40,
                                 '에그마요': 123,
                                 '오믈렛': 140,

                                 # The calories should not be added to calories of recipe
                                 # (* Ask the reason to creator of Subway Korea Website)
                                 '치즈': None,
                                 }

        # bread_list = ['플랫브래드',
        #               '하티',
        #               '허니오트',
        #               '파마산 오레가노',
        #               '위트',
        #               '화이트',
        #               ]
        bread_dict = {'플랫브래드': 230,
                      '하티': 210,
                      '허니오트': 230,
                      '파마산 오레가노': 210,
                      '위트': 210,
                      '화이트': 200,
                      }

        # topping_list = ['아보카도',
        #                 '베이컨',
        #                 '더블 치즈',
        #                 '더블업',
        #                 '에그마요',
        #                 '오믈렛',
        #                 ]
        topping_dict = {'아보카도': 60,
                        '베이컨': 40,
                        # The calories of Double cheese & Double up option should be set apart from this module.
                        '더블 치즈': None,
                        '더블업': None,
                        '에그마요': 123, # 1스쿱 from FatSecret
                        '오믈렛': 140, # calculation
                        }

        # cheese_list = ['아메리칸 치즈',
        #                '치즈없음',
        #                '슈레드 치즈',
        #                ]
        cheese_dict = {'아메리칸 치즈': 40,
                       '치즈없음': None,
                       '슈레드 치즈': 50,
                       }

        toasting_list = ['토스팅',
                         '토스팅없음',
                         ]

        # vegetable_list = ['오이',
        #                   '할라피뇨',
        #                   '양상추',
        #                   '올리브',
        #                   '피망',
        #                   '피클',
        #                   '양파',
        #                   '토마토',
        #                   # '아보카도',
        #                   ]
        vegetable_dict = {'오이': 5,
                          '할라피뇨': 5,
                          '양상추': 5,
                          '올리브': 5,
                          '피망': 5,
                          '피클': 5,
                          '양파': 5,
                          '토마토': 5,
                           # '아보카도': 60,
                          }

        # sauce_list = ['랜치드레싱',
        #               '마요네즈',
        #               '스위트 어니언',
        #               '허니 머스터드',
        #               '스위트 칠리',
        #               '핫 칠리',
        #               '사우스 웨스트',
        #               '머스타드',
        #               '디종홀스래디쉬',
        #               '사우전 아일랜드',
        #               '이탈리안 드레싱',
        #               '올리브 오일',
        #               '레드와인식초',
        #               '소금',
        #               '후추',
        #               '스모크 바비큐',
        #               ]
        sauce_dict = {'리치시저': 100,
                      '랜치드레싱': 110,
                      '마요네즈': 110,
                      '스위트 어니언': 40,
                      '허니 머스터드': 30,
                      '스위트 칠리': 30,
                      '핫 칠리': 40,
                      '사우스 웨스트': 100,
                      '머스타드': 5,
                      '디종홀스래디쉬': 110,
                      '사우전 아일랜드': 80,
                      '이탈리안 드레싱': 80,
                      '올리브 오일': 45,
                      '레드와인식초': 40,
                      '소금': None,
                      '후추': None,
                      '스모크 바비큐': 35,
        }

        category_list = ['신제품',
                         '프로모션',
                         '클래식',
                         '프레쉬 & 라이트',
                         '프리미엄',
                         '아침메뉴',
                         ]

        def get_or_create(class_name, folder_name, obj_name_list):
            for obj_name in obj_name_list:
                obj, _ = class_name.objects.get_or_create(name=obj_name)

                image_path = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '.png'
                image_path3x = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '@3x.png'

                static_storage_class = import_string(settings.STATICFILES_STORAGE)
                static_storage = static_storage_class()

                image_url = static_storage.url(image_path)
                image_url3x = static_storage.url(image_path3x)
                obj.image = image_url
                obj.image3x = image_url3x
                obj.save()

        def get_or_create_with_calories(class_name, folder_name, obj_name_dict):
            for obj_name in obj_name_dict:
                obj, _ = class_name.objects.get_or_create(name=obj_name)

                image_path = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '.png'
                image_path3x = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '@3x.png'

                static_storage_class = import_string(settings.STATICFILES_STORAGE)
                static_storage = static_storage_class()

                image_url = static_storage.url(image_path)
                image_url3x = static_storage.url(image_path3x)
                obj.image = image_url
                obj.image3x = image_url3x

                obj.calories = obj_name_dict[obj_name]
                obj.save()

        def get_or_create_with_calories_for_vegetables(class_name, folder_name, obj_name_dict):
            for obj_name in obj_name_dict:
                for quantity in ['조금', '보통', '많이']:
                    obj, _ = class_name.objects.get_or_create(name=obj_name, quantity=quantity)

                    image_path = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '.png'
                    image_path3x = folder_name + '/' + eval(folder_name + '_dict')[obj_name] + '@3x.png'

                    static_storage_class = import_string(settings.STATICFILES_STORAGE)
                    static_storage = static_storage_class()

                    image_url = static_storage.url(image_path)
                    image_url3x = static_storage.url(image_path3x)
                    obj.image = image_url
                    obj.image3x = image_url3x

                    obj.calories = obj_name_dict[obj_name]

                    # 2018.11.19
                    # Quantity process added
                    obj.quantity = quantity

                    obj.save()

        def get_or_create_for_main_ingredient(obj_name, obj_quantity):
            obj, _ = MainIngredient.objects.get_or_create(name=obj_name, quantity=obj_quantity)

            image_path = 'main_ingredient/' + main_ingredient_dict[obj_name] + '.png'
            image_path3x = 'main_ingredient/' + main_ingredient_dict[obj_name] + '@3x.png'

            static_storage_class = import_string(settings.STATICFILES_STORAGE)
            static_storage = static_storage_class()

            image_url = static_storage.url(image_path)
            image_url3x = static_storage.url(image_path3x)
            obj.image = image_url
            obj.image3x = image_url3x

            # calories counter
            obj_name_calories = main_ingredients_dict[obj_name]
            if obj_quantity:
                obj_name_calories *= int(obj_quantity[0])
            obj.calories = obj_name_calories

            obj.save()
            return obj

        # [Sandwich.objects.get_or_create(name=name) for name in sandwich_list]
        # [Bread.objects.get_or_create(name=name) for name in bread_list]
        # [Toppings.objects.get_or_create(name=name) for name in topping_list]
        # [Cheese.objects.get_or_create(name=name) for name in cheese_list]
        # [Vegetables.objects.get_or_create(name=name) for name in vegetable_list]
        # [Sauces.objects.get_or_create(name=name) for name in sauce_list]
        # [Category.objects.get_or_create(name=name) for name in category_list]

        # 유일하게 진짜 'get_or_create'를 사용하던 recipe_name_list도 비지니스 로직이 변경되면서 주석처리 -> 결국 get_or_create안씀
        # [RecipeName.objects.get_or_create(name=name) for name in recipe_name_list]

        # get_or_create(Bread, 'bread', bread_list)
        # get_or_create(Toppings, 'toppings', topping_list)
        # get_or_create(Cheese, 'cheese', cheese_list)
        get_or_create(Toasting, 'toasting', toasting_list)
        # get_or_create(Vegetables, 'vegetables', vegetable_list)
        # get_or_create(Sauces, 'sauces', sauce_list)

        get_or_create_with_calories(Bread, 'bread', bread_dict)
        get_or_create_with_calories(Cheese, 'cheese', cheese_dict)
        get_or_create_with_calories(Toppings, 'toppings', topping_dict)
        # get_or_create_with_calories(Vegetables, 'vegetables', vegetable_dict)
        get_or_create_with_calories(Sauces, 'sauces', sauce_dict)

        get_or_create_with_calories_for_vegetables(Vegetables, 'vegetables', vegetable_dict)

        for name in sandwich_list:
            sandwich, _ = Sandwich.objects.get_or_create(name=name)

            # 1) Sandwich 인스턴스 생성 후 image url path 저장
            image_path_full = 'sandwich/full/' + sandwich_dict[name] + '.png'
            image_path3x_full = 'sandwich/full/' + sandwich_dict[name] + '@3x.png'

            image_path_left = 'sandwich/left/' + sandwich_dict[name] + '.png'
            image_path3x_left = 'sandwich/left/' + sandwich_dict[name] + '@3x.png'

            image_path_right = 'sandwich/right/' + sandwich_dict[name] + '.png'
            image_path3x_right = 'sandwich/right/' + sandwich_dict[name] + '@3x.png'

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

            image_url_full = static_storage.url(image_path_full)
            image_url3x_full = static_storage.url(image_path3x_full)
            sandwich.image_full = image_url_full
            sandwich.image3x_full = image_url3x_full

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

            if sandwich.name == '로티세리 치킨':
                rotisserie_chicken = get_or_create_for_main_ingredient('로티세리 치킨', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')

                # 2) Sandwich 인스턴스 생성 후 Main Ingredient field 저장
                sandwich.main_ingredient.add(
                    rotisserie_chicken,
                    # cheese,
                )
                # 3) Sandwich 인스턴스 생성 후 Category field 저장
                event, _ = Category.objects.get_or_create(name='프로모션')
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    event,
                    fresh_and_light,
                )
                # 4) Sandwich Nutrition Information 설정
                sandwich.serving_size = 247
                sandwich.calories = 350
                sandwich.sugars = 7
                sandwich.protein = 29
                sandwich.saturated_fat = 1.5
                sandwich.sodium = 660
                # 5) Sandwich 인스턴스 생성 후 ordering_num 설정
                sandwich.ordering_num = 1

            elif sandwich.name == '풀드포크':
                pulled_pork = get_or_create_for_main_ingredient('풀드포크', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    pulled_pork,
                    # cheese,
                )
                new, _ = Category.objects.get_or_create(name='신제품')
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    new,
                    premium,
                )
                sandwich.serving_size = 276
                sandwich.calories = 420
                sandwich.sugars = 24
                sandwich.protein = 23
                sandwich.saturated_fat = 2
                sandwich.sodium = 980
                sandwich.ordering_num = 2

            elif sandwich.name == '에그마요':
                egg_mayo = get_or_create_for_main_ingredient('에그마요', '2스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    egg_mayo,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 247
                sandwich.calories = 480
                sandwich.sugars = 7
                sandwich.protein = 17
                sandwich.saturated_fat = 6
                sandwich.sodium = 450
                sandwich.ordering_num = 3

            elif sandwich.name == '이탈리안 비엠티':
                pepperoni = get_or_create_for_main_ingredient('페퍼로니', '3장')
                salami = get_or_create_for_main_ingredient('살라미', '3장')
                ham = get_or_create_for_main_ingredient('햄', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    ham,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 226
                sandwich.calories = 410
                sandwich.sugars = 8
                sandwich.protein = 20
                sandwich.saturated_fat = 6
                sandwich.sodium = 1260
                sandwich.ordering_num = 4

            elif sandwich.name == '비엘티':
                bacon = get_or_create_for_main_ingredient('베이컨', '4장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    bacon,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 165
                sandwich.calories = 380
                sandwich.sugars = 7
                sandwich.protein = 20
                sandwich.saturated_fat = 4
                sandwich.sodium = 1130
                sandwich.ordering_num = 5

            elif sandwich.name == '미트볼':
                meatball = get_or_create_for_main_ingredient('미트볼', '4개')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    meatball,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 301
                sandwich.calories = 480
                sandwich.sugars = 12
                sandwich.protein = 21
                sandwich.saturated_fat = 7
                sandwich.sodium = 1000
                sandwich.ordering_num = 6

            elif sandwich.name == '햄':
                ham = get_or_create_for_main_ingredient('햄', '4장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    ham,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 219
                sandwich.calories = 290
                sandwich.sugars = 8
                sandwich.protein = 18
                sandwich.saturated_fat = 1
                sandwich.sodium = 800
                sandwich.ordering_num = 7

            elif sandwich.name == '참치':
                tuna = get_or_create_for_main_ingredient('참치', '2스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    tuna,
                    # cheese,
                )
                classic, _ = Category.objects.get_or_create(name='클래식')
                sandwich.category.add(
                    classic,
                )
                sandwich.serving_size = 237
                sandwich.calories = 480
                sandwich.sugars = 7
                sandwich.protein = 20
                sandwich.saturated_fat = 4.5
                sandwich.sodium = 580
                sandwich.ordering_num = 8

            elif sandwich.name == '로스트 치킨':
                chicken_breast = get_or_create_for_main_ingredient('치킨 브레스트', '1장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    chicken_breast,
                    # cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.serving_size = 233
                sandwich.calories = 320
                sandwich.sugars = 8
                sandwich.protein = 23
                sandwich.saturated_fat = 1.5
                sandwich.sodium = 610
                sandwich.ordering_num = 9

            elif sandwich.name == '로스트 비프':
                roast_beef = get_or_create_for_main_ingredient('로스트 비프', '3장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    roast_beef,
                    # cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.serving_size = 233
                sandwich.calories = 320
                sandwich.sugars = 7
                sandwich.protein = 25
                sandwich.saturated_fat = 1.5
                sandwich.sodium = 660
                sandwich.ordering_num = 10

            elif sandwich.name == '써브웨이 클럽':
                turkey = get_or_create_for_main_ingredient('터키', '2장')
                ham = get_or_create_for_main_ingredient('햄', '1장')
                roast_beef = get_or_create_for_main_ingredient('로스트 비프', '1장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    turkey,
                    ham,
                    roast_beef,
                    # cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.serving_size = 240
                sandwich.calories = 310
                sandwich.sugars = 8
                sandwich.protein = 23
                sandwich.saturated_fat = 1.5
                sandwich.sodium = 840
                sandwich.ordering_num = 11

            elif sandwich.name == '터키':
                turkey = get_or_create_for_main_ingredient('터키', '4장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    turkey,
                    # cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.serving_size = 219
                sandwich.calories = 280
                sandwich.sugars = 7
                sandwich.protein = 18
                sandwich.saturated_fat = 1
                sandwich.sodium = 760
                sandwich.ordering_num = 12

            elif sandwich.name == '베지':
                all_veggies = get_or_create_for_main_ingredient('각종 야채', '')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    all_veggies,
                    # cheese,
                )
                fresh_and_light, _ = Category.objects.get_or_create(name='프레쉬 & 라이트')
                sandwich.category.add(
                    fresh_and_light,
                )
                sandwich.serving_size = 162
                sandwich.calories = 230
                sandwich.sugars = 7
                sandwich.protein = 8
                sandwich.saturated_fat = 0.5
                sandwich.sodium = 280
                sandwich.ordering_num = 13

            elif sandwich.name == '스테이크 & 치즈':
                steak = get_or_create_for_main_ingredient('스테이크', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('오믈렛', '2장')
                sandwich.main_ingredient.add(
                    steak,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 245
                sandwich.calories = 380
                sandwich.sugars = 9
                sandwich.protein = 26
                sandwich.saturated_fat = 4.5
                sandwich.sodium = 1030
                sandwich.ordering_num = 14

            elif sandwich.name == '터키 베이컨 아보카도':
                turkey = get_or_create_for_main_ingredient('터키', '3장')
                bacon = get_or_create_for_main_ingredient('베이컨', '2장')
                avocado = get_or_create_for_main_ingredient('아보카도', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    avocado,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 270
                sandwich.calories = 420
                sandwich.sugars = 8
                sandwich.protein = 24
                sandwich.saturated_fat = 3.5
                sandwich.sodium = 1190
                sandwich.ordering_num = 15

            elif sandwich.name == '치킨 베이컨 랜치':
                chicken_strip = get_or_create_for_main_ingredient('치킨 스트립', '1스쿱')
                bacon = get_or_create_for_main_ingredient('베이컨', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    chicken_strip,
                    bacon,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 298
                sandwich.calories = 610
                sandwich.sugars = 8
                sandwich.protein = 38
                sandwich.saturated_fat = 10
                sandwich.sodium = 1290
                sandwich.ordering_num = 16

            elif sandwich.name == '써브웨이 멜트':
                turkey = get_or_create_for_main_ingredient('터키', '2장')
                bacon = get_or_create_for_main_ingredient('베이컨', '2장')
                ham = get_or_create_for_main_ingredient('햄', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    ham,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 246
                sandwich.calories = 410
                sandwich.sugars = 9
                sandwich.protein = 26
                sandwich.saturated_fat = 5
                sandwich.sodium = 1410
                sandwich.ordering_num = 17

            elif sandwich.name == '터키 베이컨':
                turkey = get_or_create_for_main_ingredient('터키', '3장')
                bacon = get_or_create_for_main_ingredient('베이컨', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    turkey,
                    bacon,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 234
                sandwich.calories = 360
                sandwich.sugars = 8
                sandwich.protein = 23
                sandwich.saturated_fat = 3
                sandwich.sodium = 1190
                sandwich.ordering_num = 18

            elif sandwich.name == '스파이시 이탈리안':
                pepperoni = get_or_create_for_main_ingredient('페퍼로니', '5장')
                salami = get_or_create_for_main_ingredient('살라미', '5장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    pepperoni,
                    salami,
                    # cheese
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 222
                sandwich.calories = 480
                sandwich.sugars = 8
                sandwich.protein = 20
                sandwich.saturated_fat = 9
                sandwich.sodium = 1490
                sandwich.ordering_num = 19

            elif sandwich.name == '치킨 데리야끼':
                chicken_strip = get_or_create_for_main_ingredient('치킨 데리야끼', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    chicken_strip,
                    # cheese,
                )
                premium, _ = Category.objects.get_or_create(name='프리미엄')
                sandwich.category.add(
                    premium,
                )
                sandwich.serving_size = 269
                sandwich.calories = 370
                sandwich.sugars = 16
                sandwich.protein = 25
                sandwich.saturated_fat = 1
                sandwich.sodium = 770
                sandwich.ordering_num = 20

            elif sandwich.name == '블랙 포레스트햄 & 에그, 치즈':
                omelet = get_or_create_for_main_ingredient('오믈렛', '1장')
                ham = get_or_create_for_main_ingredient('햄', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    # cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='아침메뉴')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.serving_size = 203
                sandwich.calories = 400
                sandwich.sugars = 6
                sandwich.protein = 24
                sandwich.saturated_fat = 5
                sandwich.sodium = 1150
                sandwich.ordering_num = 21

            elif sandwich.name == '웨스턴, 에그 & 치즈':
                omelet = get_or_create_for_main_ingredient('오믈렛', '1장')
                ham = get_or_create_for_main_ingredient('햄', '1장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    omelet,
                    ham,
                    # cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='아침메뉴')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.serving_size = 174
                sandwich.calories = 370
                sandwich.sugars = 5
                sandwich.protein = 19
                sandwich.saturated_fat = 4.5
                sandwich.sodium = 880
                sandwich.ordering_num = 22

            elif sandwich.name == '베이컨, 에그 & 치즈':
                omelet = get_or_create_for_main_ingredient('오믈렛', '1장')
                bacon = get_or_create_for_main_ingredient('베이컨', '2장')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    omelet,
                    bacon,
                    # cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='아침메뉴')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.serving_size = 190
                sandwich.calories = 450
                sandwich.sugars = 6
                sandwich.protein = 25
                sandwich.saturated_fat = 7
                sandwich.sodium = 1310
                sandwich.ordering_num = 23

            elif sandwich.name == '스테이크, 에그 & 치즈':
                steak = get_or_create_for_main_ingredient('스테이크', '1스쿱')
                omelet = get_or_create_for_main_ingredient('오믈렛', '1스쿱')
                # cheese = get_or_create_for_main_ingredient('치즈', '2장')
                sandwich.main_ingredient.add(
                    steak,
                    omelet,
                    # cheese,
                )
                breakfast, _ = Category.objects.get_or_create(name='아침메뉴')
                sandwich.category.add(
                    breakfast,
                )
                sandwich.serving_size = 217
                sandwich.calories = 440
                sandwich.sugars = 6
                sandwich.protein = 28
                sandwich.saturated_fat = 6
                sandwich.sodium = 1210
                sandwich.ordering_num = 24

            sandwich.save()

