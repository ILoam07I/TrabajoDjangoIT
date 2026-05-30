from .base import *

# Se mantiene el modo Debug activado para ver los errores en pantalla

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Configuración de base de datos por defecto (SQLite) para desarrollo rápido

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',
        
    }

}