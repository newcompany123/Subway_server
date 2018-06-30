from django.db import models
from django.conf import settings


class RecipeLike(models.Model):
    """
    Recipe와 좋아요한 User를 연결하는 intermediate model
    """
    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.liker}의' \
               f' Recipe {self.recipe} 좋아요'


class RecipeBookmark(models.Model):
    """
    Recipe와 Recipe를 북마크한 User를 연결하는 intermediate model
    """
    bookmarker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.bookmarker}의' \
               f' Recipe {self.recipe} 저장'
