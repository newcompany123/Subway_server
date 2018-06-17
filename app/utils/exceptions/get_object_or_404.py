from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework import status

from utils.exceptions.custom_exception import CustomException


def get_object_or_404_customed(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404
    except Http404 as e:
        # print(e)
        # print(type(e))
        raise CustomException(
            detail=f"{queryset.__name__}'s object is not found!",
            status_code=status.HTTP_404_NOT_FOUND
        )
