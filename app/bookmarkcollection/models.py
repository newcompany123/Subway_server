from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BookmarkCollection(models.Model):
    """
    Recipes which are Bookmarked by user
    """
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # bookmarked_recipe = models.ManyToManyField(
    #     Bookmark,
    #     verbose_name='북마크 콜렉션',
    #     blank=True
    # )

    def __str__(self):
        return f'{self.user}의 북마크콜렉션 {self.name}'
