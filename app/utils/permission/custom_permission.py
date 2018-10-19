import re

from django.contrib.auth import get_user_model
from rest_framework import permissions

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()


class IsOneselfOrReadOnly(permissions.BasePermission):
    # UserRetrieveUpdateDestroyView
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    # BookmarkCollectionListCreateView
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # POST Method 인 경우 request.user 와 requst uri의 user의 동일 여부 확인
        path = request._request.path
        result = re.search(r'.+?(\d+).+?', path)
        pk = result.group(1)
        user = get_object_or_404_customed(User, pk=pk)
        return user == request.user

    # BookmarkCollectionRetrieveUpdateDestroyView
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsRecipeInventorOrReadOnly(permissions.BasePermission):
    # RecipeRetrieveUpdateDestroyView
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.inventor == request.user


class IsSuperUserOrReadOnly(permissions.BasePermission):
    # NoticeboardListCreateView
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        superuser = User.objects.first()
        return superuser == request.user


class IsRecipeNameMakerOrReadOnly(permissions.BasePermission):
    # RecipeNameRetrieveUpdateDestroyView
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user





