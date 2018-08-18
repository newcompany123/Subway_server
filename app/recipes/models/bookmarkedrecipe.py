from django.db import models
from django.conf import settings


class BookmarkedRecipe(models.Model):
    """
    Recipe와 Recipe를 북마크한 User를 연결하는 intermediate model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
    )
    # # Circling Import Issue
    # collection = models.ForeignKey(
    #     BookmarkCollection,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     default=None
    # )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user}의' \
               f' Recipe {self.recipe} 저장'
