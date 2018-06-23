from django.urls import path

from recipes.apis.recipe_name import RecipeNameListCreateView
from recipes.apis.sandwich import SandwichListCreateView
from .apis.recipe_bookmark import RecipeBookmarkListCreateView
from .apis.recipe_like import RecipeLikeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', RecipeLikeListCreateView.as_view()),
    path('<int:pk>/bookmark/', RecipeBookmarkListCreateView.as_view()),

    path('name/', RecipeNameListCreateView.as_view()),
    path('sandwich/', SandwichListCreateView.as_view()),
]
