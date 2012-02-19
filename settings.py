import os
import django
#
# Django settings for routemaster project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
   #  ('chopper', 'dev@nuclearblender.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'django_routemaster',                      # Or path to database file if using sqlite3.
#        'USER': 'chiditarod',                      # Not used with sqlite3.
#        'PASSWORD': 'mush08',                  # Not used with sqlite3.
#        'HOST': 'mysql.nuclearblender.com',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# calculated paths for django and the site
# used as starting points for various other paths
# from: http://morethanseven.net/2009/02/11/django-settings-tip-setting-relative-paths.html
# and http://www.ramavadakattu.com/top-10-tips-to-a-new-django-developer
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'appmedia')
TEMPLATE_DIRS = ( os.path.join(SITE_ROOT, 'templates'),)

DEFAULT_CAPACITY_COMFORTABLE = 1000000
DEFAULT_CAPACITY_MAXIMUM = 1000000

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/Applications/DjangoStack/apps/django/django_projects/routemaster/routemaster.sqlite',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_routemaster',
        #'HOST': '/Applications/DjangoStack/mysql/tmp/mysql.sock',
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
        'PORT': '3306',
        #'PORT': '8889',
        'USER': 'root',
        'PASSWORD': 'root'
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/trumpcar/www/routemaster.chiditarod.org/public/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '13=2(_0&emtco33n5m97=q^&_7^g85_h0@zsdi52kjy9_n^^&)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'routemaster.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'routemaster.races',
    #'south',

)
