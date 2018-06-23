from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters import FilterSet, Filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework import generics, permissions
from utils.permission.custom_permission import IsProductMakerOrReadOnly

from ..serializers.product import ProductSerializer
from ..models import Product, MainIngredient

User = get_user_model()

__all__ = (
    'ProductListCreateView',
    'ProductRetrieveUpdateDestroyView',
)


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values_text = value.split(',')
        values = []
        for value in values_text:
            obj = MainIngredient.objects.get(name=value)
            values.append(obj.id)
        return super().filter(qs, values)


class ProductFilter(FilterSet):
    main_ingredient = ListFilter()

    class Meta:
        model = Product
        fields = (
            'main_ingredient',
        )


class ProductListCreateView(generics.ListCreateAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    # filter_fields = ('main_ingredient',)
    # DjangoFilterBackends에 multiple id를 사용하기 위해
    # filter_class와 ListFilter를 활용하여 Custom
    filter_class = ProductFilter

    ordering_fields = ('id', 'like_count', 'save_count',)
    ordering = ('-like_save_count', '-save_count', '-like_count',)
    search_fields = ('product_name__name',)

    def get_queryset(self):
        queryset = Product.objects.annotate(
            like_count=Count('product_liker', distinct=True),
            save_count=Count('product_saver', distinct=True),
            like_save_count=Count('product_liker', distinct=True) +
                            Count('product_saver', distinct=True),
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(product_maker=self.request.user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsProductMakerOrReadOnly,
    )
