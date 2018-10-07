from django.urls import path

from .apis.collection import BookmarkCollectionListCreateView, BookmarkCollectionUpdateDestroyView
from .apis.recipe import BookmarkListCreateAPIView


urlpatterns = [
    # 유저가 bookamrk한 모든 recipes
    path('bookmark/', BookmarkListCreateAPIView.as_view()),

    # 유저의 collection
    path('collection/', BookmarkCollectionListCreateView.as_view()),
    path('collection/<int:pk>/', BookmarkCollectionUpdateDestroyView.as_view()),
]
