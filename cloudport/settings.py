# Django settings for cloudport project.
from base_settings import * #imports the sensitive settings

DEBUG = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www-django/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

#FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
#
#FILEBROWSER_DIRECTORY = MEDIA_ROOT

STATICFILES_DIRS = (
    #"/var/www-django/cloudport/static",
    #"/home/polls.com/polls/static",
    #"/opt/webfiles/common",
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
)

STATIC_ROOT = "/var/www-django/media/static"
STATIC_URL = "/static/"

COMPRESS_ROOT = STATIC_ROOT
STATIC_URL = STATIC_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

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

ROOT_URLCONF = 'cloudport.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/var/www-django/cloudport/templates/",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    'grappelli', #install: "pip install django-grappelli", this is a skin for the admin interface.
    #'filebrowser', #install: "pip install django-filebrowser", needs grappelli and PIL, gives file browser in admin interface.
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.staticfiles', #only available since 1.3
    'djangorestframework', #i installed this library using "sudo pip install djangorestframework"
    #'less', #installed using "sudo pip install django-less"
    'compressor', #installed using "pip install django_compressor"
    'tastypie',
    #'cloudport.polls',
    'cloudport.job_manager',
    'cloudport.templates', #needed to do this to make the templatetags work...
    'django_socketio',
    #'django_socketio.templatetags',
)

LESS_EXECUTABLE = 'lessc'

COMPRESS_PRECOMPILERS = (
    #('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', LESS_EXECUTABLE+' {infile} > {outfile}'),
    #('text/x-sass', 'sass {infile} {outfile}'),
    #('text/x-scss', 'sass --scss {infile} {outfile}'),
)
COMPRESS_ENABLED = True

TASK_UPLOAD_FILE_EXTENSIONS = ['sce', 'py']
#TASK_UPLOAD_FILE_TYPES = ['pdf', 'vnd.oasis.opendocument.text','vnd.ms-excel','msword','application',]
TASK_UPLOAD_FILE_MAX_SIZE = "5242880"

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = '/tmp/django.log',
    filemode = 'w'
)

