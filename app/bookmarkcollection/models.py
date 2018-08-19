from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import BookmarkedRecipe

User = get_user_model()


class BookmarkCollection(models.Model):
    """
    Recipes which are Bookmarked by user
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmarked_recipe = models.ManyToManyField(
        BookmarkedRecipe,
        verbose_name='북마크 콜렉션',
        blank=True
    )
