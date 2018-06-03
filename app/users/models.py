from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.pk} {self.username}'


class UserOAuthID(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='oauthid',
    )
    kakao_id = models.CharField(max_length=255, blank=True)
    facebook_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'UserOAuthID'

    def __str__(self):
        return f'{self.user} [facebook_id: {self.facebook_id} | kakao_id: {self.kakao_id}]'
