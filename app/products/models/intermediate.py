from django.db import models
from django.conf import settings


class ProductLike(models.Model):
    """
    Product와 좋아요한 User를 연결하는 intermediate model
    """
    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.liker}의' \
               f' Product {self.product} 좋아요'


class ProductSave(models.Model):
    """
    Product와 해당 product를 저장한 User를 연결하는 intermediate model
    """
    saver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.saver}의' \
               f' Product {self.product} 저장'
