
# from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, Filter
from rest_framework.filters import OrderingFilter
from rest_framework import generics, permissions

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers.recipe import SandwichSerializer
from ..models import Sandwich, Category


class CustomFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        uppercase_value = value.upper()
        obj = get_object_or_404_customed(Category, name=uppercase_value)
        return super().filter(qs, obj)


class SandwichFilter(FilterSet):
    category = CustomFilter()

    class Meta:
        model = Sandwich
        fields = (
            'category',
        )


class SandwichListCreateView(generics.ListCreateAPIView):
    queryset = Sandwich.objects.all()
    serializer_class = SandwichSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    # filtering
    # filter_fields = ('category',)
    filter_class = SandwichFilter

    # ordering
    ordering_fields = ('id', 'category_new', 'category_event',)
