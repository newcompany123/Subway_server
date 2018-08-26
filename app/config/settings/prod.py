from .base import *


DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    '.smallbee.kr',
    '.my-subway.com',
]
WSGI_APPLICATION = 'config.wsgi.prod.application'

INSTALLED_APPS += [
    'storages',
]

DEFAULT_FILE_STORAGE = 'config.storage.DefaultFilesStorage'
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://subway-redis.7xbhwi.ng.0001.apn2.cache.amazonaws.com:6379",
        "LOCATION": [
            "redis://subway-redis-001.7xbhwi.0001.apn2.cache.amazonaws.com",
            "redis://subway-redis-002.7xbhwi.0001.apn2.cache.amazonaws.com",
        ],
        "OPTIONS": {
            "DB": 1,
            "MASTER_CACHE": "redis://subway-redis-001.7xbhwi.0001.apn2.cache.amazonaws.com",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

import_secrets()
