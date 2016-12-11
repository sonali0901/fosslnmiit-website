'''
Production settings

- Set secret key from environment variable
'''

from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','52.66.136.79', 'localhost','fosslnmiit.xyz','www.fosslnmiit.xyz']

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'fosslnmiit@gmail.com'
SERVER_EMAIL = 'fosslnmiit@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'fosslnmiit@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_KEY']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fosslnmiit8postgres8',
        'USER': 'fosslnmiit_8',
        'PASSWORD': os.environ['db_pass'],
        'HOST': os.environ['db_host'], 
        'PORT': '5432',
    }
}
