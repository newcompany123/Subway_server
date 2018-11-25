from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsRecipeInventorOrReadOnly

from ..serializers.recipe import RecipeSerializer
from ..models import Recipe

User = get_user_model()

__all__ = (
    'RecipeListCreateView',
    'RecipeRetrieveUpdateDestroyView',
)


# class ListFilter(Filter):
#     def filter(self, qs, value):
#         if not value:
#             return qs
#
#         self.lookup_expr = 'in'
#         # value = urllib.parse.unquote_plus(value)
#         value = value.replace(', ', '_ ')
#         values_text = value.split(',')
#         values = []
#         for value in values_text:
#             value = value.replace('_ ', ', ')
#             obj = Sandwich.objects.get(name=value)
#             values.append(obj.id)
#         return super().filter(qs, values)
#
#
# class RecipeFilter(FilterSet):
#     sandwich = ListFilter()
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'sandwich',
#         )


# 2018.11.21
# Using FilterSet and Filter causes duplicates in queries
# -> BaseFilterBackend and filter_queryset
# Result : 145 qs -> 7 qs

class RecipeFilter(BaseFilterBackend):
    """
    Filter Recipe with category
    """
    def filter_queryset(self, request, queryset, view):
        params = request.query_params.get('sandwich')

        if params:
            params = params.replace(', ', '_ ')
            params_text = params.split(',')
            sandwich_list = [x.replace('_ ', ', ') for x in params_text]
            queryset = queryset.filter(sandwich__name__in=sandwich_list)
        return queryset


class RecipeListCreateView(generics.ListCreateAPIView):

    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # # filtering
    # # filter_fields = ('sandwich',)
    # # FilterSet & Filter used to allow DjangoFilterBackends get multiple fields.
    # # e.g.
    # # {{HOST}}/recipe/?sandwich=비엘티%2C블랙+포레스트햄+%26+에그%2C+치즈
    # filter_class = RecipeFilter

    # >> 2018.11.21
    # For the same reason above
    filter_backends = (RecipeFilter, OrderingFilter, SearchFilter,)

    # OrderingFilter
    ordering_fields = ('id', 'like_count', 'bookmark_count', 'created_date',)
    ordering = ('-like_bookmark_count', '-bookmark_count', '-like_count',)

    # SearchingFilter
    # 2018.11.15
    # Forgot to apply the change of name field to the search filter option
    #  and it raised an 500 error as below
    # "django.core.exceptions.FieldError: Unsupported lookup 'name' for
    #  CharField or join on the field not permitted."
    # search_fields = ('name__name',)
    search_fields = ('name',)

    def get_queryset(self):

        value = Recipe.objects \
            .select_related('sandwich', 'bread', 'cheese', 'toasting', 'inventor') \
            .prefetch_related('toppings', 'vegetables', 'sauces',
                              'sandwich__main_ingredient', 'sandwich__category',) \
            .annotate(
                    like_count=Count('liker', distinct=True),
                    bookmark_count=Count('bookmarker', distinct=True),
                    like_bookmark_count=Count('liker', distinct=True)
                                        + Count('bookmarker', distinct=True),
            )
        return value

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Testing the Recipe API response in the case of AnonymousUser
        # context['request'].user = AnonymousUser()
        return context

    def perform_create(self, serializer):
        serializer.save(inventor=self.request.user)


class RecipeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsRecipeInventorOrReadOnly,
    )

    def get_queryset(self):

        value = Recipe.objects \
            .select_related('sandwich', 'bread', 'cheese', 'toasting', 'inventor') \
            .prefetch_related('toppings', 'vegetables', 'sauces',
                              'sandwich__main_ingredient', 'sandwich__category',) \
            .annotate(
                    like_count=Count('liker', distinct=True),
                    bookmark_count=Count('bookmarker', distinct=True),
                    like_bookmark_count=Count('liker', distinct=True)
                                        + Count('bookmarker', distinct=True),
            )
        return value
