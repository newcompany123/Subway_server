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

DEFAULT_FILE_STORAGE = 'config.storage.DefaultFilesStorage'
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'

import_secrets()
