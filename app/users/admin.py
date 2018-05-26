from django.contrib import admin

from .models import User, UserOAuthID

admin.site.register(User)
admin.site.register(UserOAuthID)
