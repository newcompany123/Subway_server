from django.urls import path

from recipes.apis.recipe_name import RecipeNameListCreateView
from ingredients.apis.sandwich import SandwichListCreateView
from .apis.recipe_bookmark import BookmarkedRecipeListCreateView
from .apis.recipe_like import LikedRecipeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', LikedRecipeListCreateView.as_view()),
    path('<int:pk>/bookmark/', BookmarkedRecipeListCreateView.as_view()),

    path('name/', RecipeNameListCreateView.as_view()),
    path('sandwich/', SandwichListCreateView.as_view()),
]
