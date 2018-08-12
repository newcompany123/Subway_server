from django.urls import path

from .apis.collection import BookmarkCollectionListCreateAPIView
from .apis.recipe import BookmarkListCreateAPIView


urlpatterns = [
    path('bookmark/', BookmarkListCreateAPIView.as_view()),
    path('collection/', BookmarkCollectionListCreateAPIView.as_view()),
]
