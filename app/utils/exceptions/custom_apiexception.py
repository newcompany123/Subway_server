from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'CustomAPIException',
)


class CustomAPIException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    # default_detail = _('Invalid input.')
    detail = 'Invalid input.'
    default_code = 'invalid'

    # custom
    # pk = None

    def __init__(self, status_code=None, detail=None, **kwargs):

        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail

        # custom
        # if pk is not None:
        #     self.pk = pk

        # custom (2) - Any word, number can be passed to custom excepion handler
        # if kwargs is not None:
        if kwargs:
            self.key = list(kwargs.keys())[0]
            self.value = kwargs[self.key]
