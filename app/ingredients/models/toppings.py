from django.db import models


class Toppings(models.Model):
    """
    Recipe와 Many-to-many relationship으로 연결된 Toppings
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Topping의 이름을 저장합니다.',
    )
    calories = models.SmallIntegerField(blank=True, null=True)
    image = models.FilePathField(max_length=255)
    image3x = models.FilePathField(max_length=255)

    def __str__(self):
        return f'{self.pk}_{self.name}'
