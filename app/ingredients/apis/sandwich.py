from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers import SandwichSerializer
from ..models import Sandwich


# class CustomFilter(Filter):
#     def filter(self, qs, value):
#         # qs = distinct(qs, qs)
#         qs = qs.distinct()
#
#         if not value:
#             return qs
#         # uppercase_value = value.upper()
#         obj = get_object_or_404_customed(Category, name=value)
#         return super().filter(qs, obj)
#
#
# class SandwichFilter(FilterSet):
#     category = CustomFilter()
#
#     class Meta:
#         model = Sandwich
#         fields = (
#             'category',
#         )


# 2018.11.21
# Using FilterSet and Filter causes duplicates in queries
# -> BaseFilterBackend and filter_queryset
# Result : 22 qs -> 4 qs

class SandwichFilter(BaseFilterBackend):
    """
    Filter Sandwich with category
    """
    def filter_queryset(self, request, queryset, view):
        params = request.query_params.get('category')

        if params:
            queryset = queryset.filter(category__name=params)
        return queryset


class SandwichListCreateView(generics.ListCreateAPIView):

    queryset = Sandwich.objects.prefetch_related(
        'main_ingredient',
        'category',
    )
    serializer_class = SandwichSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )

    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    # filtering
    # filter_fields = ('category',)
    # filter_class = SandwichFilter

    # >> 2018.11.21
    filter_backends = (SandwichFilter, OrderingFilter)

    # OrderingFilter
    ordering_fields = ('id', 'ordering_num', 'category_new', 'category_event',)
    ordering = ('ordering_num',)
