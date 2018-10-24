from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    # if response is not None:
    #     response.data['status_code'] = response.status_code

    try:
        if exc.pk:
            response.data['pk'] = exc.pk
    # except AttributeError:
    #     return response
    finally:
        return response
