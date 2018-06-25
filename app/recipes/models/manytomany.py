from django.db import models


class Vegetables(models.Model):
    """
    Recipe와 Many-to-many relationship으로 연결된 Vegetables
    """
    VEGETABLE_LESS = 'LE'
    VEGETABLE_NORMAL = 'NO'
    VEGETABLE_MORE = 'MO'

    VEGETABLE_QUANTITY_CHOICES = (
        (VEGETABLE_LESS, 'LESS'),
        (VEGETABLE_NORMAL, 'NORMAL'),
        (VEGETABLE_MORE, 'MORE'),
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Vegetable의 이름을 저장합니다.',
    )
    quantity = models.CharField(
        max_length=2,
        choices=VEGETABLE_QUANTITY_CHOICES,
        default='NO'
    )
    image = models.FilePathField(max_length=255)

    def __str__(self):
        return f'{self.pk}_{self.name}'


class Toppings(models.Model):
    """
    Recipe와 Many-to-many relationship으로 연결된 Toppings
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Topping의 이름을 저장합니다.',
    )
    image = models.FilePathField(max_length=255)

    def __str__(self):
        return f'{self.pk}_{self.name}'


class Sauces(models.Model):
    """
    Recipe와 Many-to-many relationship으로 연결된 Sauces
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Sauce의 이름을 저장합니다.',
    )
    image = models.FilePathField(max_length=255)

    def __str__(self):
        return f'{self.pk}_{self.name}'
