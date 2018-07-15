from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """
    Post model on noticeboard
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_date']

    def __str__(self):
        return self.title
