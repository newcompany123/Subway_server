from django.urls import path

from .apis.collection import BookmarkCollectionListCreateView
from .apis.recipe import BookmarkListCreateAPIView


urlpatterns = [
    path('bookmark/', BookmarkListCreateAPIView.as_view()),
    path('collection/', BookmarkCollectionListCreateView.as_view()),
]
