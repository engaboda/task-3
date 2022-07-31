"""
Django settings for keycloak_drf project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging
import environ
from pathlib import Path

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables
    # defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    CONFIG_DIR = environ.Path(__file__) - 2
    env_file = str(CONFIG_DIR.path('.env'))
    logger.debug('Loading : {}'.format(env_file))
    env.read_env(env_file)
    logger.info('The .env file has been loaded. See base.py for more information')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'django-insecure-vxh+rhy)&23mx!b-v6^wqo=kq9igp6c#l2f*$te5fdz5!z%^&$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'integeration.apps.IntegerationConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'keycloak_drf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'keycloak_drf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}

############################################################################
LOGGING = {

    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        # Our application code
        'montymobile': {
            'level': 'INFO',
            'handlers': ['console'],
            # Avoid double logging because of root logger
            'propagate': False,
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

AUTH_USER_MODEL = 'integeration.User'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


KEYCLOAK_CLIENT_SECRECT = env('KEYCLOAK_CLIENT_SECRECT', default='c9Rwr3gHHs8jDgnOcRmKZmOt7dG2kUBQ')
KEYCLOAK_CLIENT_ID = env('KEYCLOAK_CLIENT_ID', default='aboda-client')  # admin-cli
KEYCLOAK_GRANT_TYPE = env('KEYCLOAK_GRANT_TYPE', default='client_credentials')  # client_credentials
KEYCLOAK_MASTER_REALM = env('KEYCLOAK_MASTER_REALM', default='master')  # master
KEYCLOAK_CREATE_RETRIEVE_USER_API = env(
    'KEYCLOAK_CREATE_RETRIEVE_USER_API', default='http://localhost:8080/admin/realms/montymobile/users')
KEYCLOAK_ADMIN_TOKEN_API = env(
    'KEYCLOAK_ADMIN_TOKEN_API', default='http://localhost:8080/admin/realms/master/protocol/openid-connect/token')
KEYCLOAK_USER_TOKEN_API = env(
    'KEYCLOAK_USER_TOKEN_API', default='http://localhost:8080/admin/realms/master/protocol/openid-connect/token')
KEYCLOAK_USER_INFO_API = env(
    'KEYCLOAK_USER_INFO_API', default='http://localhost:8080/realms/master/protocol/openid-connect/userinfo')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'integeration.authentication.KeycloakAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
