import os

from .base import *

DEBUG = False # Seguridad obligatoria en producción

ALLOWED_HOSTS = ['*'] # En un entorno real, aquí iría el dominio (ej. 'midominio.com')

# Configuración de PostgreSQL leyendo del SO (Inyectado por Docker)

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.getenv('POSTGRES_DB_BLOG'),

        'USER': os.getenv('POSTGRES_USER_BLOG'),

        'PASSWORD': os.getenv('POSTGRES_PASSWORD_BLOG'),

        'HOST': os.getenv('POSTGRES_HOST_BLOG'),

        'PORT': os.getenv('POSTGRES_PORT_BLOG'),

    }

}

STATIC_ROOT = BASE_DIR / 'staticfiles'