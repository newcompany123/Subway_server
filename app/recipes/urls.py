from django.urls import path

from recipe_name.apis import RecipeNameListCreateView, RecipeNameChoicesListAPIView
from .apis.bookmark import BookmarkListCreateView
from .apis.like import LikeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', LikeListCreateView.as_view()),
    path('<int:pk>/bookmark/', BookmarkListCreateView.as_view()),

    path('name/', RecipeNameListCreateView.as_view()),
    path('name-choices/', RecipeNameChoicesListAPIView.as_view()),
]
