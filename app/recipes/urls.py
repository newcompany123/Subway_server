from django.urls import path, include

from recipe_name.apis import RecipeNameListCreateView, RecipeNameChoicesListAPIView
from .apis.bookmark import BookmarkListCreateView
from .apis.like import LikeListCreateView
from .apis.recipe import RecipeListCreateView, RecipeRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeListCreateView.as_view()),
    path('<int:pk>/', RecipeRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', LikeListCreateView.as_view()),
    path('<int:pk>/bookmark/', BookmarkListCreateView.as_view()),

    path('name/', include('recipe_name.urls'))
]
