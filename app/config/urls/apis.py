from django.urls import path, include

urlpatterns = [
    path('user/', include('users.urls')),
    path('recipe/', include('recipes.urls')),
    path('noticeboard/', include('noticeboard.urls')),
]
