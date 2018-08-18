from django.urls import path

from .apis import SandwichListCreateView, BreadListCreateView, CheeseListCreateView, ToastingListCreateView, \
    ToppingsListCreateView, VegetablesListCreateView, SaucesListCreateView

urlpatterns = [
    path('sandwich/', SandwichListCreateView.as_view()),
    path('bread/', BreadListCreateView.as_view()),
    path('cheese/', CheeseListCreateView.as_view()),
    path('toasting/', ToastingListCreateView.as_view()),
    path('toppings/', ToppingsListCreateView.as_view()),
    path('vegetables/', VegetablesListCreateView.as_view()),
    path('sauces/', SaucesListCreateView.as_view()),
]