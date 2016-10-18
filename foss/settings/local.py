'''
Local settings

- Run in Debug mode
'''

from .common import *

# Use DEBUG for local development
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

#EMAIL settings
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'fosslnmiit@gmail.com'
SERVER_EMAIL = 'fosslnmiit@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'fosslnmiit@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_KEY']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# read database.md file for configuring
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fosslnmiit',
        'USER': 'fosslnmiituser',
        'PASSWORD': os.environ['db_pass'],
        'HOST': 'localhost',
        'PORT': '',
    }
}
