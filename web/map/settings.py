"""
Django settings for map project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, locale

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECRET_KEY = "k769%g32gq++w+yq-z9ac+!aeydo(nazzit=8r=tlkw"

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('PRODUCTION_SETTING', None):
    DEBUG = False
else:
    DEBUG = True

if os.getenv('PRODUCTION_SETTING', None):
    ALLOWED_HOSTS = ['*','tasador.dataurbana.io']
else:
    ALLOWED_HOSTS = ['127.0.0.1','localhost','tasador.dataurbana.io']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'reset_migrations',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'imagekit',
    'user',
    'realestate',
    'reversion',
    'home',
    'list',
    'create',
    'appraisal',
    'house',
    'store',
    'building',
    'apartmentbuilding',
    'apartment',
    'neighborhood',
    'region',
    'terrain',
    'province',
    'commune',
    'square',
    'vis',
    'viz',
    'evaluation',
    'accounting',
    'mathfilters',
    'archive',
    'logbook',
    'bootstrap_datepicker_plus'#,
    #'debug_toolbar'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'map.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'map.wsgi.application'

# Database
if os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': '/cloudsql/proyectoinmobiliario-212003:southamerica-east1:protasa',
            'PORT': '5432',
            'NAME': 'data',
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': '127.0.0.1',
            'PORT': '5432',
            'NAME': 'data',
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD')
        }
    }

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = PROJECT_ROOT + '/../uploads'
MEDIA_URL = '/uploads/'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Chile/Continental'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# Google App Engine: set static root for local static files
STATIC_URL = 'http://storage.googleapis.com/tasador/static/'
#STATIC_URL = '/static/'

# https://cloud.google.com/appengine/docs/flexible/python/serving-static-files
STATIC_ROOT = 'static/'

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

LOGIN_REDIRECT_URL = '/login/'

LOGOUT_REDIRECT_URL = '/'

INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "nicolasrivas@dataurbana.io"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
