from django.db import models

from recipes.models import MainIngredient, Category


class Sandwich(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)으로 연결된 Sandwich
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Sandwich의 이름을 저장합니다.'
    )
    image_left = models.FilePathField(path='sandwich', max_length=255)
    image3x_left = models.FilePathField(path='sandwich', max_length=255)

    image_right = models.FilePathField(path='sandwich', max_length=255)
    image3x_right = models.FilePathField(path='sandwich', max_length=255)

    # image = models.ImageField(blank=True)
    # -> ImageField에 image의 url을 저장할 경우 아래와 같은 문제가 발생
    # (settings == local)
    # "image": "http://localhost:7000/media/static/sandwich/spicy_italian_avocado.jpg"
    # (settings == prod)
    # "image": "https://s3.ap-northeast-2.amazonaws.com/
    #           bucket-subway/media/https%3A/s3.ap-northeast-2.amazonaws.com/bucket-subway/static/sandwich/spicy_italian_avocado.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIM4DF24YBH6QS24Q%2F20180625%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20180625T102742Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1aa3b156a1d08c0c66e92fcb04b623bc6ea060bfca4b862c56d1ae82a0635559"

    main_ingredient = models.ManyToManyField(
        MainIngredient,
        blank=True,
        verbose_name='구성재료'
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='카테고리'
    )

    def __str__(self):
        return f'{self.pk})_{self.name}'


class Bread(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)으로 연결된 Bread
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Bread 이름을 저장합니다.',
    )
    image = models.FilePathField(max_length=255)
    image3x = models.FilePathField(max_length=255)

    class Meta:
        verbose_name_plural = 'bread'

    def __str__(self):
        return f'{self.pk}_{self.name}'


class Cheese(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)으로 연결된 Cheese
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Cheese 이름을 저장합니다.',
    )
    image = models.FilePathField(max_length=255)
    image3x = models.FilePathField(max_length=255)

    class Meta:
        verbose_name_plural = 'cheese'

    def __str__(self):
        return f'{self.pk}_{self.name}'


class Toasting(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)로 연결된 Toasting
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Toasting 이름을 저장합니다.',
    )
    image = models.FilePathField(max_length=255)
    image3x = models.FilePathField(max_length=255)

    class Meta:
        verbose_name_plural = 'Toasting'

    def __str__(self):
        return f'{self.pk}_{self.name}'
