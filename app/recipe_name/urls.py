from django.urls import path

from .apis import RecipeNameListCreateView, RecipeNameChoicesListAPIView

urlpatterns = [
    path('', RecipeNameListCreateView.as_view()),
    path('choices/', RecipeNameChoicesListAPIView.as_view()),
]