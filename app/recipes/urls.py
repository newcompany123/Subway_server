from django.urls import path, include

from .apis.validation import RecipeValidationAPIView
from .apis.bookmark import BookmarkListCreateView
from .apis.like import LikeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', LikeListCreateView.as_view()),
    path('<int:pk>/bookmark/', BookmarkListCreateView.as_view()),

    path('validation/', RecipeValidationAPIView.as_view()),

    path('name/', include('recipe_name.urls')),
]
