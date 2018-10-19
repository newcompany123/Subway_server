from django.urls import path

from .apis import RecipeNameListCreateView, RecipeNameChoicesListAPIView, RecipeNameRetrieveUpdateDestroyView

urlpatterns = [
    path('', RecipeNameListCreateView.as_view()),
    path('<int:pk>/', RecipeNameRetrieveUpdateDestroyView.as_view()),

    path('choices/', RecipeNameChoicesListAPIView.as_view()),
]