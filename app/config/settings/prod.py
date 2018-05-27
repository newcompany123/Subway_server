from .base import *


DEBUG = True
ALLOWED_HOSTS = [
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    '.smallbee.kr'
]
WSGI_APPLICATION = 'config.wsgi.prod.application'

INSTALLED_APPS += [
    'storages',
]

import_secrets()
