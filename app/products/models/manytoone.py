from django.db import models


class MainIngredient(models.Model):
    """
    Product와 Many-to-one relationship(ForeignKey)으로 연결된 Main ingredient
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Product Ingredient의 이름을 저장합니다.'
    )

    def __str__(self):
        return f'{self.pk})_{self.name}'


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
        return f'{self.pk}_{self.name}'
