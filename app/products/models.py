from django.conf import settings
from django.db import models


class Product(models.Model):
    """
    Bread, Vegetables, Sauces, Toppings의 조합으로 만들어진 샌드위치 object
    """
    # [ Shoveling log ]

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

    def __str__(self):
        return f'{self.pk} {self.name} [ {self.bread}, {list(self.vegetables.all().values_list("name", flat=True))} ]'


class MainIngredient(models.Model):
    """
    Product와 Many-to-one relationship(ForeignKey)으로 연결된 Main ingredient
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Product Ingredient의 이름을 저장합니다.'
    )


class Bread(models.Model):
    """
    Product와 Many-to-one relationship(ForeignKey)으로 연결된 bread
    """
    name = models.CharField(
        max_length=100,
        # unique=True,
        help_text='100자까지 bread의 이름을 저장합니다.',
    )

    class Meta:
        verbose_name_plural = '선택한 bread'

    def __str__(self):
        return f'{self.pk} {self.name}'


class Vegetables(models.Model):
    """
    Product와 Many-to-many relationship으로 연결된 vegetables
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 vegetable의 이름을 저장합니다.',
    )

    class Meta:
        verbose_name_plural = '선택한 vegetables'

    def __str__(self):
        return f'{self.pk} {self.name}'


class ProductName(models.Model):
    """
    Product의 Name을 저장하는 모델
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='255자까지 product의 이름을 저장합니다.'
    )

    def __str__(self):
        return f'{self.pk} {self.name}'


class ProductLike(models.Model):
    """
    Product와 좋아요한 User를 연결하는 intermediate model
    """
    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.liker}의' \
               f' Product {self.product} 좋아요'
