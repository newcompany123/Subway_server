from django.db import models


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
