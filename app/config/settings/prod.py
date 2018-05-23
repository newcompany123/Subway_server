from .base import *


DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.prod.application'

INSTALLED_APPS += [
    'storages',
]

import_secrets()
