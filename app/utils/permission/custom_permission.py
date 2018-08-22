import re

from django.contrib.auth import get_user_model
from rest_framework import permissions

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()


class IsOneselfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        path = request._request.path
        result = re.search(r'.+?(\d+).+?', path)
        pk = result.group(1)
        user = get_object_or_404_customed(User, pk=pk)
        # 1) obj.user == request.user
        #   BookmarkedRecipe를 한 user와 Authenticated user가 동일한지 비교
        # 2) user == request.user
        #   parameter에서 {{HOST}}/user/<user_num>/collection/<bookmarkedrecipe_num>/
        #   <user_num> 과 Authenticated user가 동일한지 비교
        return obj.user == request.user and user == request.user


class IsProductMakerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.inventor == request.user


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        superuser = User.objects.first()
        return superuser == request.user
