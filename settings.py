import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append('%s/applications' % BASE_DIR)
sys.path.append('%s/contrib-applications' % BASE_DIR)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

THUMBNAIL_COLORSPACE = 'RGB'
THUMBNAIL_EXTENSION = 'PNG'
THUMBNAIL_FORMAT = 'PNG'

ADMINS = (
	('Enoch Carter', 'mrenoch@gmail.com'),
)

ALLOWED_HOSTS = ("192.168.20.149",".ultimatescouttracker.com")

MANAGERS = ADMINS
FORMAT_MODULE_PATH = 'locales'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scouts2',                      # Or path to database file if using sqlite3.
        'USER': 'web',                      # Not used with sqlite3.
        'PASSWORD': 'web',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
    'utils.funcs.CaseInsensitiveBackend',  
    'utils.funcs.FacebookModelBackend',  
    'utils.funcs.GoogleOauthModelBackend',            
)



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '%s/static/images/' % BASE_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/images/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/static/' % BASE_DIR

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w3xmd22l_zbgwip0q@x=jl%&jo9do+n_=5p*ozzn#t!dpg10va'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.request",
	#"django.core.context_processors.tz",
	#"django.contrib.messages.context_processors.messages"
    'utils.funcs.baseProcessor'
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	BASE_DIR + '/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_extensions', 
    'sorl.thumbnail',
    
    'taglibrary',
    'position',
	'userprofile',
	'unit',
	'rank',
	'requirement',
	'userrequirement',
	'taglib',
	'userrank',
	'council',
	'award',
	'auth',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s  %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d --- %(message)s'
        },
        'more_verbose':{
            'format':'[%(asctime)s] %(levelname)-5s %(name)s @ %(module)s:%(funcName)s(), line %(lineno)d --- %(message)s'
        }
    },
    'handlers': {
		'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
		'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
		
    'loggers': {
		'django': {
            'handlers': ['console', 'null'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/'
    
GOOGLE_CLIENT_ID = "448849120100.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "XZDzn3t_ajXgEqp-g-MZJKGZ"
GOOGLE_API_KEY = "AIzaSyChYYhFzxdAJr8XReiymLBxAkzimu7etHk"

FACEBOOK_APPID = "572689142780250"


try:
    from local_settings import *
except ImportError:
    print 'No local settings file'
