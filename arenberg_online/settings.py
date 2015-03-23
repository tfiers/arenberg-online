"""
Django settings for arenberg_online project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# You should clone 'https://github.com/tfiers/arenberg-secure' into a 
# 'arenberg-secure' subdirectory of the project folder.
# (Next to for example the 'arenberg_online' and 'core' directories).
CONFIG_DIR = os.path.join(BASE_DIR, 'arenberg-secure')


# When deploying, check this list:
# https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

with open(os.path.join(CONFIG_DIR, 'django_secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [] # Only relevant when DEBUG = False (-> when you are in production).


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # Users, user profiles, instruments and groups.
    'ticketing', # Ordering tickets online, reporting tickets sold offline, 
                 # tracking ticket sales 
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'arenberg_online.urls'

WSGI_APPLICATION = 'arenberg_online.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

# Store dates in UTC, display them in TIME_ZONE by default.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Only relevant when DEBUG = False (-> when you are in production).
STATIC_ROOT = '/home/django/arenberg_online/static/'


# Change Django's default user model (defined in the django.contrib.auth app)
# to use the email address of a user as its identifier instead of a custom username.
# Except for this modification, this user model is a clone of the 
# django.contrib.auth user model.
AUTH_USER_MODEL = 'core.User'

TEMPLATE_DIRS = (
    # Location for general templates not specific to an app:
    os.path.join(BASE_DIR, 'templates/'),
)

# http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'