"""
django settings for arenberg_online project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
# If this file exists on the file system, we are in production,
# on the Ulyssis server, and we shouldn't be displaying debug
# pages for errors for example. If this file is not found, we 
# are on a developper's machine, and we can safely be in DEVELOPPING mode.
if os.path.isfile("/home/org/arenbergorkest/we_are_in_production"):
    DEVELOPPING = False
else:
    DEVELOPPING = True
DEVELOPPING = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
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
ALLOWED_HOSTS = ['95.85.3.22', '.arenbergorkest.be']




# Application definition

INSTALLED_APPS = (
    'grappelli', # A jazzy skin for the admin-interface - www.grappelliproject.com
    'django.contrib.admin',
    'import_export',
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
    'postermap', # See where posters have been hung in the city.
    # 'debug_toolbar', # http://stackoverflow.com/questions/2361985/profiling-django
    'loginas', # https://github.com/stochastic-technologies/django-loginas
    'vinaigrette', # For translation of database values. See https://github.com/ecometrica/django-vinaigrette
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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

#commands (in root directory project):
#python manage.py makemessages -all
#python manage.py compilemessages
#that's it

#if you want to change fullcalendar default paths for css and such
# FULLCALENDAR = {
#     'css_url': <path_or_url_to_css_file>,
#     'print_css_url': <path_or_url_to_print_css_file>,
#     'javascript_url': <path_or_url_to_javascript_file>,
#     'jquery_url': <path_or_url_to_jquery_file>,
#     'jquery_ui_url': <path_or_url_to_jquery_ui_file>,
# }

#specifies the current production
#included for future automatisation of ticketing, needed for poster
CURRENT_PRODUCTION = "lente2016"

# Default language, that will be used for requests without language prefix
LANGUAGE_CODE = 'nl'

LANGUAGE_BIDI = False #all left to right languages.

# Supported languages
ugettext = lambda s: s
LANGUAGES = (
    ('nl', 'Nederlands'),
    ('en', 'English'),
)

# Enable django translation.
# After you have introduced new translatable strings, run
# 'python manage.py makemessages', then edit the .po files
# in 'LOCALE_PATHS' (with Poedit e.g.) and finally run
# 'python manage.py compilemessges'.
USE_I18N = True

#this also determines the order of day month year in date widgets
DATE_FORMAT = "j N, Y"

TIME_INPUT_FORMATS = ('%H:%M',)

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

#on false so date_time works
USE_L10N = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

FILEBROWSER_DIRECTORY = os.path.join(BASE_DIR, 'core/media')

#absolute filepath to media, change when on server
MEDIA_ROOT = '/home/lennart/Documents/arenbergvenv/arenberg-online/core/media'

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Only relevant when DEBUG = False (-> when you are in production).
STATIC_ROOT = '/home/org/arenbergorkest/www/static'


# Change django's default user model (defined in the django.contrib.auth app)
# to use the email address of a user as its identifier instead of a custom username.
# Except for this modification, this user model is a clone of the 
# django.contrib.auth user model.
AUTH_USER_MODEL = 'core.User'

LOGIN_URL = 'login' # Defined in urls.py
LOGIN_REDIRECT_URL = 'ticketing:snow_landing' # Defined in urls.py

TEMPLATE_DIRS = (
    # Location for general templates not specific to an app:
    os.path.join(BASE_DIR, 'core/templates'),
)


# Write errors encountered by django 
# or raised from our source code to a file.
# See the official documentation at https://docs.djangoproject.com/en/1.7/topics/logging/
# and this blogpost: http://ianalexandr.com/blog/getting-started-with-django-logging-in-5-minutes.html
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'handlers': {
        # Set up a rotating log that can get 15 MB in size and keep 10 historical versions.
        # From http://stackoverflow.com/a/19257221
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/log.txt'),
            'maxBytes': 15*1024*1024, # 15 MB
            'backupCount': 10,
        },
    },
    'loggers': {
        # Catch all logger of errors encountered by django.
        # (https://docs.djangoproject.com/en/1.8/topics/logging/#django)
        # 5xx responses are raised as ERROR messages,
        # 4xx responses as WARNING messages,
        # database queries as DEBUG messages.
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
            'formatter': 'verbose',
        },
        # To debug the code via printouts for example.
        # Usage:
        # import logging
        # logger = logging.getLogger('developper_log')
        # logger.debug('Variable x is {}'.format(x))
        'developper_log': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'formatter': 'simple',
        },
    }
}



# Use Bootstrap 3 for rendering forms with django-crispy-forms.
# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Email
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.mailgun.org'
# EMAIL_HOST_USER = 'postmaster@arenbergorkest.be'
# with open(os.path.join(CONFIG_DIR, 'mailgun_password')) as f:
#     EMAIL_HOST_PASSWORD = f.read().strip()


if DEVELOPPING:
    POSTFIX_VIRTUAL_ALIAS_FILE = 'generated_for_postfix.txt'
else:
    POSTFIX_VIRTUAL_ALIAS_FILE = '/etc/postfix/virtual'

# To what email address should emails sent to 
# [undefined.string]@arenbergorkest.be be forwarded?
CATCHALL_EMAIL = 'bestuur@arenbergorkest'

# Migrating users from drupal site.
with open(os.path.join(CONFIG_DIR, 'default_new_password.txt')) as f:
    DEFAULT_NEW_PASSWORD = f.read().strip()
