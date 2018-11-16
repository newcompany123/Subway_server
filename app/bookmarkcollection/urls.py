from django.urls import path

from .apis import BookmarkListCreateView, BookmarkRetrieveUpdateDestroyView, CollectionListCreateView, \
    CollectionRetrieveUpdateDestroyView, CollectionRetrieveDefault

urlpatterns = [
    # User's bookamrked recipes
    path('bookmark/', BookmarkListCreateView.as_view()),
    path('bookmark/<int:pk>/', BookmarkRetrieveUpdateDestroyView.as_view()),

    # User's collection
    path('collection/', CollectionListCreateView.as_view()),
    path('collection/<int:pk>/', CollectionRetrieveUpdateDestroyView.as_view()),

    # Special API to load data in the front-end more efficiently
    path('collection/default/', CollectionRetrieveDefault.as_view()),
]
