from django.db import models


class MainIngredient(models.Model):
    """
    Sandwich와 Many-to-many relationship으로 연결된 MainIngredient
    """
    name = models.CharField(
        max_length=100,
        # unique=True,
        # 대신에 'unique_together' 추가
        help_text='100까지 MainIngredient의 이름을 저장합니다.',
    )
    quantity = models.CharField(
        max_length=100,
        blank=True,
        help_text='100자까지 MainIngredient의 quantity를 저장합니다.',
    )
    calories = models.SmallIntegerField(blank=True, null=True)
    image = models.FilePathField(max_length=255)
    image3x = models.FilePathField(max_length=255)

    class Meta:
        unique_together = (
            ('name', 'quantity'),
        )

    def __str__(self):
        return f'{self.pk}_{self.name} ({self.quantity})'
