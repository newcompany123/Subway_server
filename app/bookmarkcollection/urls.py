from django.urls import path

from .apis.recipe import BookmarkListCreateAPIView


urlpatterns = [
    path('', BookmarkListCreateAPIView.as_view()),
]
