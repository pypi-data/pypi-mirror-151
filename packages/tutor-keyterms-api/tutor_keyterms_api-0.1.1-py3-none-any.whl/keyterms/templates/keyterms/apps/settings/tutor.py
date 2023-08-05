from .common import *

ALLOWED_HOSTS = [
    "keytermsapi",
    "keyterms",
    "{{ KEYTERMS_HOST }}",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": {{MYSQL_PORT}},
        "NAME": "{{ KEYTERMS_MYSQL_DATABASE }}",
        "USER": "{{ KEYTERMS_MYSQL_USERNAME }}",
        "PASSWORD": "",
    }
}

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{{ REDIS_HOST }}:{{ REDIS_PORT }}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

ELASTICSEARCH_DSL = {'default': {'hosts': '{{ ELASTICSEARCH_HOST }}:{{ ELASTICSEARCH_PORT }}'}}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

{{ patch("keyterms-settings") }}
