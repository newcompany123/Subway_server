from .base import *


DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.local.application'

INSTALLED_APPS += [
    'django_extensions',
]

import_secrets()
