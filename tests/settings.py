"""Django settings for tests."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_email_user',
    'caronte',
    'tests',
]

MEDIA_URL = '/media/'   # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tests.urls'

STATIC_ROOT = os.path.join(BASE_DIR, 'tests', 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tests', 'additional_static'),
    ("prefix", os.path.join(BASE_DIR, 'tests', 'additional_static')),
]

# Cache and database
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-caronte'
    }
}

# Authentication
AUTH_USER_MODEL = 'custom_email_user.EmailUser'

# Debug Toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    # Django's test client sets wsgi.multiprocess to True inappropriately
    'RENDER_PANELS': False,
}
