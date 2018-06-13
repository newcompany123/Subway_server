from django.db import models


class ProductName(models.Model):
    """
    Product의 Name을 One-to-one relationship으로 저장하는 모델
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='255자까지 product의 이름을 저장합니다.'
    )

    def __str__(self):
        return f'{self.pk}_{self.name}'
