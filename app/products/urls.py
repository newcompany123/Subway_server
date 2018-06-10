from django.urls import path

from .apis.product_like import ProductLikeListCreateAPIView
from .apis.product import ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductNameListCreateView

urlpatterns = [
    path('', ProductListCreateView.as_view()),
    path('<int:pk>/', ProductRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', ProductLikeListCreateAPIView.as_view()),
    path('name/', ProductNameListCreateView.as_view()),
]
