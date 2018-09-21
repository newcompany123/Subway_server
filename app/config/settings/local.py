from .base import *


DEBUG = True
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.local.application'

INSTALLED_APPS += [
    'django_extensions',
    'storages',
]

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1", # 1번 DB
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# django_debug_toorbar config
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

import_secrets()
