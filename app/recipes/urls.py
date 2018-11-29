from django.urls import path

from recipes.apis.recipe_name_choices import RecipeNameChoicesListAPIView
from .apis.validation import RecipeValidationAPIView
from .apis.bookmark_toggle import BookmarkListCreateView
from .apis.like_toggle import LikeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', LikeListCreateView.as_view()),
    path('<int:pk>/bookmark/', BookmarkListCreateView.as_view()),

    path('validation/', RecipeValidationAPIView.as_view()),

    path('name-choices/', RecipeNameChoicesListAPIView.as_view()),
]
