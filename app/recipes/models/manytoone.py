from django.db import models


class Sandwich(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)으로 연결된 Sandwich
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='100자까지 Sandwich의 이름을 저장합니다.'
    )
    # image = models.FilePathField(path='sandwich', blank=True, max_length=1000)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.pk})_{self.name}'


class Bread(models.Model):
    """
    Recipe와 Many-to-one relationship(ForeignKey)으로 연결된 Bread
    """
    name = models.CharField(
        max_length=100,
        # unique=True,
        help_text='100자까지 Bread 이름을 저장합니다.',
    )
    # image = models.ImageField(blank=True)
    image = models.ImageField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'bread'

    def __str__(self):
        return f'{self.pk}_{self.name}'
