from django.db.models import Count
from django.forms import model_to_dict

from rest_framework import status

from ingredients.models import Toppings, Vegetables, Sauces
from recipes.models import Recipe
from utils.exceptions import CustomAPIException


def recipe_uniqueness_validator(attrs, **kwargs):
    # ------------------------------------------------------------
    # [ Shoveling log ]
    #   : hardcoding eradicated

    # 과정1) self.initial_data에서 입력된 bread의 pk 데이터를 꺼내 attrs에 직접 할당
    # if self.initial_data.get('bread'):
    #     bread_pk = self.initial_data.get('bread')
    #     bread_obj = get_object_or_404(Bread, pk=bread_pk)
    #     attrs['bread'] = bread_obj
    # else:
    #     raise APIException("'bread' field is required.")

    # 과정2) self.initial_data에서 입력된 vetables의 pk 데이터를 꺼내 attrs에 직접 할당
    # if self.initial_data.get('vegetables'):
    #     veg_list = []
    #     veg_pk_list = self.initial_data.getlist('vegetables')
    #
    #     # 과정3_2) 하단의 uniqueness 검증을 위한 sort 과정 추
    #     veg_pk_list = sorted(veg_pk_list)
    #     for veg_pk in veg_pk_list:
    #         # veg_obj = get_object_or_404(Vegetables, pk=veg_pk)
    #         try:
    #             veg_obj = Vegetables.objects.get(pk=veg_pk)
    #         except Exception:
    #             raise APIException("Input non-existing 'vegetables' object.")
    #
    #         veg_list.append(veg_obj)
    #     attrs['vegetables'] = veg_list
    #     print(veg_list)
    # else:
    #     raise APIException("'vegetables' field is required.")

    # 과정3) product의 name 설정
    # if self.initial_data.get('name'):
    #     product_name_pk = self.initial_data.get('name')
    #     product_name_obj = get_object_or_404(RecipeName, pk=product_name_pk)
    #     attrs['name'] = product_name_obj
    # else:
    #     raise APIException("'name' field(recipe name) is required.")
    # ------------------------------------------------------------

    # 1) recipe name's uniqueness validation

    # [shoveling log]
    # O(n)
    # for recipe in Recipe.objects.all():
    #
    #     # 1) recipe name's uniqueness validation
    #     name = attrs.get('name')
    #     if recipe.name == name:
    #         raise CustomAPIException(
    #             detail='Same sandwich name already exists!',
    #             status_code=status.HTTP_400_BAD_REQUEST
    #         )

    # O(log n)
    print(attrs.get('name'))

    # Do not apply to Recipe Validation API
    if not kwargs.get('path') == '/recipe/validation/':
        if Recipe.objects.filter(name=attrs.get('name')):
            raise CustomAPIException(
                detail='Same sandwich name already exists!',
                status_code=status.HTTP_400_BAD_REQUEST
            )

    # 2) recipe ingredients' uniqueness validation

    # [shoveling log]
    # O(n) - Time: 150~200ms
    # for recipe in Recipe.objects.all():
    #
    #     sandwich = attrs.get('sandwich')
    #     if recipe.sandwich == sandwich:
    #
    #         bread = attrs.get('bread')
    #         # print(f'{recipe.bread} {bread_obj}')
    #         if recipe.bread == bread:
    #
    #             cheese = attrs.get('cheese')
    #             if recipe.cheese == cheese:
    #
    #                 toasting = attrs.get('toasting', False)
    #                 if recipe.toasting == toasting:
    #
    #                     topping_list = attrs.get('toppings')
    #                     # print(f'{list(recipe.toppings.all())} {topping_list}')
    #                     if set(recipe.toppings.all()) == (set(topping_list) if topping_list is not None else set()):
    #
    #                         vegetable_list = attrs.get('vegetables')
    #                         # print(f'{list(recipe.vegetables.all())} {vegetable_list}')
    #                         if set(recipe.vegetables.all()) == (set(vegetable_list) if vegetable_list is not None else set()):
    #
    #                             sauce_list = attrs.get('sauces')
    #                             if set(recipe.sauces.all()) == (set(sauce_list) if sauce_list is not None else set()):
    #
    #                                 raise CustomAPIException(
    #                                     detail='Same sandwich recipe already exists!',
    #                                     status_code=status.HTTP_400_BAD_REQUEST
    #                                 )

    # O(log n) - Time: 100~150ms
    recipe_filtered_list = Recipe.objects \
        .filter(sandwich=attrs.get('sandwich')) \
        .filter(bread=attrs.get('bread')) \
        .filter(cheese=attrs.get('cheese')) \
        .filter(toasting=attrs.get('toasting'))

    # # Filtering test 1
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects\
    #         .filter(toppings__in=attrs.get('toppings'))
    #
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #
    # # Filtering Test 1-2
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects\
    #         .filter(toppings__in=attrs.get('toppings')).distinct()
    #
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())

    """
    181029
    Without '.distinct()' querysets are duplicate.

    [ WIF ]
    And what I found out from the above code is this.
    ~.filter(<many_to_many_field>__in=[objectA, objectB, objectC]
    If one queryset has three ManyToMany relation objects, 
    Django evaluates '.filter' three times for each object.
    The way to check this out is using the code above changing the
    number of duplicate request data.
    """

    # Filtering Test 2-1
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects\
    #         .filter(toppings__in=attrs.get('toppings')).distinct() \
    #         .annotate(num_toppings=Count('toppings'))
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #     print(recipe_filtered_list2.values('toppings'))

    # Filtering Test 2-2 - switch the sequence of annotate & filter().distint()
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects \
    #         .annotate(num_toppings=Count('toppings')) \
    #         .filter(toppings__in=attrs.get('toppings')).distinct()
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #     print(recipe_filtered_list2.values('toppings'))

    # Filtering Test 2-3
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects\
    #         .filter(toppings__in=attrs.get('toppings')).distinct() \
    #         .annotate(num_toppings=Count('toppings', distinct=True)) \
    #         .filter(num_toppings=len(attrs.get('toppings')))
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #     print(recipe_filtered_list2.values('toppings'))

    # Filtering Test 2-4
    # topping_pk_list = []
    # for topping in attrs.get('toppings', []):
    #     topping_pk_list.append(topping.pk)
    #
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects \
    #         .filter(toppings__pk__in=[1, 6]).distinct() \
    #         .annotate(num_toppings=Count('toppings', distinct=True)) \
    #         .filter(num_toppings=len(attrs.get('toppings'))) \
    #         .exclude(toppings__in=Toppings.objects.exclude(pk__in=topping_pk_list))
    #         # .filter(toppings__in=attrs.get('toppings')).distinct() \
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #     print(recipe_filtered_list2.values('toppings'))

    # Filtering Test 2-5 : use exclude in a different way
    # if attrs.get('toppings'):
    #     recipe_filtered_list2 = Recipe.objects\
    #         .filter(toppings__in=attrs.get('toppings')).distinct() \
    #         .annotate(num_toppings=Count('toppings')) \
    #         .filter(num_toppings=len(attrs.get('toppings'))) \
    #         .exclude(pk__in=Recipe.objects
    #                  .annotate(num_toppings=Count('toppings'))
    #                  .filter(num_toppings__gt=len(attrs.get('toppings')))
    #                  )
    #
    #     print(len(recipe_filtered_list2))
    #     print(recipe_filtered_list2.values())
    #     print(recipe_filtered_list2.values('toppings'))

    # toppings
    if recipe_filtered_list:

        topping_pk_list = []
        for topping in attrs.get('toppings', []):
            topping_pk_list.append(topping.pk)

        if attrs.get('toppings'):
            recipe_filtered_list = recipe_filtered_list \
                .filter(toppings__in=attrs.get('toppings')).distinct() \
                .annotate(num_toppings=Count('toppings', distinct=True)) \
                .filter(num_toppings=len(attrs.get('toppings'))) \
                .exclude(toppings__in=Toppings.objects.exclude(pk__in=topping_pk_list))
        else:
            recipe_filtered_list \
                .filter(toppings__isnull=True)

    # vegetables
    if recipe_filtered_list:

        vegetable_pk_list = []
        for vegetable in attrs.get('vegetables', []):
            vegetable_pk_list.append(vegetable.pk)

        if attrs.get('vegetables'):
            recipe_filtered_list = recipe_filtered_list \
                .filter(vegetables__in=attrs.get('vegetables')).distinct() \
                .annotate(num_vegetables=Count('vegetables', distinct=True)) \
                .filter(num_vegetables=len(attrs.get('vegetables'))) \
                .exclude(vegetables__in=Vegetables.objects.exclude(pk__in=vegetable_pk_list))
        else:
            recipe_filtered_list \
                .filter(vegetables__isnull=True)

    # sauces
    if recipe_filtered_list:

        sauce_pk_list = []
        for sauce in attrs.get('sauces', []):
            sauce_pk_list.append(sauce.pk)

        if attrs.get('sauces'):
            recipe_filtered_list = recipe_filtered_list \
                .filter(sauces__in=attrs.get('sauces')).distinct() \
                .annotate(num_sauces=Count('sauces', distinct=True)) \
                .filter(num_sauces=len(attrs.get('sauces'))) \
                .exclude(sauces__in=Sauces.objects.exclude(pk__in=sauce_pk_list))
        else:
            recipe_filtered_list \
                .filter(sauces__isnull=True)

    # print(recipe_filtered_list)
    # for recipe in recipe_filtered_list:
    #     print(model_to_dict(recipe))

    if recipe_filtered_list:
        # pk = recipe_filtered_list.values('pk')[0]['pk']
        pk = recipe_filtered_list.values_list('pk', flat=True)[0]
        return pk
    else:
        return True
