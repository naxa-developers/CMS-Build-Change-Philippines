from .settings import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'survey',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

INSTALLED_APPS += [

    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = '127.0.0.1'