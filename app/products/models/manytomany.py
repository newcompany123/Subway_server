from django.db import models


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
        return f'{self.pk}_{self.name}'
