"""
Django settings for arenberg_online project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

DEVELOPPING = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# You should clone 'https://github.com/tfiers/arenberg-secure' into a 
# 'arenberg-secure' subdirectory of the project folder
# (Next to for example the 'arenberg_online' and 'core' directories).
CONFIG_DIR = os.path.join(BASE_DIR, 'arenberg-secure')


# When deploying, check this list:
# https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

with open(os.path.join(CONFIG_DIR, 'django_secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOPPING
TEMPLATE_DEBUG = DEVELOPPING

# Only relevant when when you are in production.
ALLOWED_HOSTS = ['95.85.3.22', 'arenbergorkest.be']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms', # https://github.com/maraujop/django-crispy-forms
    'core', # Users, user profiles, instruments and groups.
    'django.contrib.formtools', # For multi-page forms.
    'ticketing', # Ordering tickets online, reporting tickets sold offline, 
                 # tracking ticket sales 
    'music_suggestions', # Suggest pieces to be played and vote for them.
    'polls', # Ask questions to orchestra members.
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'solid_i18n.middleware.SolidLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'arenberg_online.urls'

WSGI_APPLICATION = 'arenberg_online.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request", # Now the request will be available in each template.
)


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
# https://github.com/st4lk/django-solid-i18n-urls#django-solid_i18n-urls

# Default language, that will be used for requests without language prefix
LANGUAGE_CODE = 'nl'

# Supported languages
LANGUAGES = (
    ('nl', 'Nederlands'),
    ('en', 'English'),
)

# Enable Django translation.
# After you have introduced new translatable strings, run
# 'python manage.py makemessages', then edit the .po files
# in 'LOCALE_PATHS' (with Poedit e.g.) and finally run
# 'python manage.py compilemessges'.
USE_I18N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# If True, redirect from url without prefix (/...), to url with 
# non-default language prefix (/en/...) if user's language is not 
# equal to default. Otherwise url without language prefix will always
# render default language content (see behaviour section and notes for 
# details https://github.com/st4lk/django-solid-i18n-urls#behaviour);
SOLID_I18N_USE_REDIRECTS = True

# If True, redirect from url with default language prefix (/nl/...)
# to url without any prefix (/...).
SOLID_I18N_DEFAULT_PREFIX_REDIRECT = True

# If True, both urls /... and /nl/... will render default language 
# content (in this example 'nl' is default language). Otherwise, 
# /nl/... will return 404 status_code. // "Don't mix together settings 
# SOLID_I18N_HANDLE_DEFAULT_PREFIX and SOLID_I18N_DEFAULT_PREFIX_REDIRECT. 
# You should choose only one of them."
# SOLID_I18N_HANDLE_DEFAULT_PREFIX = True

TIME_ZONE = 'Europe/Brussels'

# Store dates in UTC, display them in TIME_ZONE by default.
USE_TZ = True

USE_L10N = True


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
    os.path.join(BASE_DIR, 'templates'),
)

# Use Bootstrap 3 for rendering forms with django-crispy-forms.
# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Email

if DEVELOPPING:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'tomas.fiers@gmail.com'
    with open(os.path.join(CONFIG_DIR, 'google_pass.txt')) as f:
        EMAIL_HOST_PASSWORD = f.read().strip()
else:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
