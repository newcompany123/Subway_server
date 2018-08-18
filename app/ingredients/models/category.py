from django.db import models


class Category(models.Model):
    """
    Sandwich와 Many-to-many relationship으로 연결된 Category
    """
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return f'{self.pk}_{self.name}'
