from django.urls import path

from products.apis.product_save import ProductSaveListCreateView
from .apis.product_like import ProductLikeListCreateView
from .apis.product import ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductNameListCreateView

urlpatterns = [
    path('', ProductListCreateView.as_view()),
    path('<int:pk>/', ProductRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/like/', ProductLikeListCreateView.as_view()),
    path('<int:pk>/save/', ProductSaveListCreateView.as_view()),
    path('name/', ProductNameListCreateView.as_view()),
]
