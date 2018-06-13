from django.conf import settings
from django.db import models


class Product(models.Model):
    """
    Bread, Vegetables, Sauces, Toppings의 조합으로 만들어진 샌드위치 object
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
        'productname',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='이름',
    )

    main_ingredient = models.ForeignKey(
        'mainingredient',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='기본 샌드위치',
    )

    bread = models.ForeignKey(
        'bread',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='빵',
    )

    vegetables = models.ManyToManyField(
        'vegetables',
        blank=True,
        verbose_name='야채',
    )

    product_maker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='made_product',
        verbose_name='레시피 제작자',
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    img_profile_thumbnail = models.ImageField(upload_to='user', blank=True)

    product_liker = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_product',
        through='ProductLike',
    )

    product_saver = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_product',
        through='ProductSave',
    )

    def __str__(self):
        return f'{self.pk}) {self.name} ' \
               f'[ {self.main_ingredient} {self.bread}, {list(self.vegetables.all().values_list("name", flat=True))} ]'
