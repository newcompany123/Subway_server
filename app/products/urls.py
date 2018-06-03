from django.urls import path

from .apis.product import ProductListCreateView, UserRetrieveUpdataeDestroyView

urlpatterns = [
    path('', ProductListCreateView.as_view()),
    path('<int:pk>/', UserRetrieveUpdataeDestroyView.as_view()),
]