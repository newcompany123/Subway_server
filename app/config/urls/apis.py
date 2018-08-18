from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('user/', include('users.urls')),
    path('recipe/', include('recipes.urls')),
    path('noticeboard/', include('noticeboard.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('api-docs/', schema_view),
]
