from django.urls import path

from .apis.collection import BookmarkCollectionListCreateView, BookmarkCollectionRetrieveUpdateDestroyView
from .apis.bookmark import BookmarkRetrieveUpdateDestroyView, BookmarkListCreateView

urlpatterns = [
    # 유저가 bookamrk한 모든 recipes
    path('bookmark/', BookmarkListCreateView.as_view()),
    path('bookmark/<int:pk>/', BookmarkRetrieveUpdateDestroyView.as_view()),

    # 유저의 collection
    path('collection/', BookmarkCollectionListCreateView.as_view()),
    path('collection/<int:pk>/', BookmarkCollectionRetrieveUpdateDestroyView.as_view()),
]
