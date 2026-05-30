import os

from .base import *

DEBUG = True # Seguridad obligatoria en producción

ALLOWED_HOSTS = ['*'] # En un entorno real, aquí iría el dominio (ej. 'midominio.com')

# Configuración de PostgreSQL leyendo del SO (Inyectado por Docker)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8001',
]

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.getenv('POSTGRES_DB_BEATEMPLATE'),

        'USER': os.getenv('POSTGRES_USER_BEATEMPLATE'),

        'PASSWORD': os.getenv('POSTGRES_PASSWORD_BEATEMPLATE'),

        'HOST': os.getenv('POSTGRES_HOST_BEATEMPLATE'),

        'PORT': os.getenv('POSTGRES_PORT_BEATEMPLATE'),

    }

}

STATIC_ROOT = BASE_DIR / 'staticfiles'