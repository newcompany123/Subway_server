from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'CustomException',
)


class CustomException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    # default_detail = _('Invalid input.')
    detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail=None, status_code=None):

        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail