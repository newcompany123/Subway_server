from django.conf import settings
from django.db import models

from ..models import Toppings, Cheese, Sauces


class Recipe(models.Model):
    """
    Bread, Vegetables, Sauces, Cheese, Toppings의 조합으로 만들어진 Recipe object
    """
    # [ Shoveling log ]
    #   : OneToOneField -> ForeignKey fixed
    #
    # bread = models.OneToOneField(
    #     'bread',
    #     max_length=3,
    #     on_delete=models.SET_NULL,
    #     blank=False,
    #     null=True,
    #     verbose_name='빵',
    # )
    name = models.OneToOneField(
        'RecipeName',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='이름',
    )
    sandwich = models.ForeignKey(
        'Sandwich',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='기본 샌드위치',
    )
    bread = models.ForeignKey(
        'Bread',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='빵',
    )
    cheese = models.ForeignKey(
        Cheese,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='치즈',
    )
    toasting = models.BooleanField(default=False)

    toppings = models.ManyToManyField(
        Toppings,
        verbose_name='토핑',
    )
    vegetables = models.ManyToManyField(
        'Vegetables',
        verbose_name='야채',
    )
    sauces = models.ManyToManyField(
        Sauces,
        verbose_name='소스',
    )

    inventor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='made_recipe',
        verbose_name='레시피 제작자',
    )
    liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_recipe',
        through='RecipeLike',
    )
    bookmarker = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='bookmarked_recipe',
        through='RecipeBookmark',
    )
    # [ Shoveling log ]
    # 이곳이 아닌 sandwich에서 url을 설정하게 되면 매번 recipe를 생성할 때 마다 image 생성 작업을
    # 불필요하게 하지 않아도 됨.
    # image = models.ImageField(blank=True)
    # image2x = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.pk} {self.name} ' \
               f'[ {self.sandwich} {self.bread}, {list(self.vegetables.all().values_list("name", flat=True))} ]'
