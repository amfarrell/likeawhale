# Django settings for likeawhale project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'decodering',                              # Or path to database file if using sqlite3.
        'USER': 'decodering',                                     # Not used with sqlite3.
        'PASSWORD': 'sekkrit',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
SECRET_KEY = 'tbc%om=uj34e93_%*fp!7x+rdg+hu12-8618ei1z$m&amp;*71fjgx'

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
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'articles',
    'learning',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'south',
)

#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.request",
  "allauth.account.context_processors.account",
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.csrf",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.contrib.messages.context_processors.messages",
  "allauth.socialaccount.context_processors.socialaccount",
)

SOUTH_MIGRATION_MODULES = {
  'allauth.account'       : 'decodering.external_migrations.account',
  'allauth.socialaccount' : 'decodering.external_migrations.socialaccount',
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#GOOGLE_TRANSLATE_API_KEY = 'AIzaSyDrgCi2QfzE_JeBeuWYFBjnxp-9JARhUho'
GOOGLE_TRANSLATE_API_KEY = 'AIzaSyCTwFR8WQJ-jMV2BivXa6tfJobS-YZFKrQ'
LOGIN_URL = '/accounts/login/'

##############################################################
### Specific to https://github.com/pennersr/django-allauth ###
### The user authentication plugin.                        ###
##############################################################
LOGIN_REDIRECT_URL = '/en/'
ACCOUNT_ADAPTER ="allauth.account.adapter.DefaultAccountAdapter"
#Specifies the adapter class to use, allowing you to alter certain default behaviour.
ACCOUNT_AUTHENTICATION_METHOD ="email"
#Specifies the login method to use - whether the user logs in by entering his username, e-mail address, or either one of both.
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
#The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
#The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user. Set to None to use settings.LOGIN_REDIRECT_URL.
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 9
#Determines the expiration date of email confirmation mails (# of days).
ACCOUNT_EMAIL_REQUIRED = True
#The user is required to hand over an e-mail address when signing up.
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
#Determines the e-mail verification method during signup. When set to "mandatory" the user is blocked from logging in until the email address is verified. Choose "optional" or "none" to allow logins with an unverified e-mail address. In case of "optional", the e-mail verification mail is still sent, whereas in case of "none" no e-mail verification mails are sent.
ACCOUNT_EMAIL_SUBJECT_PREFIX ="[afarrell-uap]"
#Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.
ACCOUNT_SIGNUP_FORM_CLASS = None
#A string pointing to a custom form class (e.g. 'myapp.forms.SignupForm') that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date). This class should implement a 'save' method, accepting the newly signed up user as its only parameter.
#TODO: make this a form which asks the user what langauges they know.
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
#When signing up, let the user type in his password twice to avoid typ-o's.
ACCOUNT_UNIQUE_EMAIL = True
#Enforce uniqueness of e-mail addresses.
ACCOUNT_USER_DISPLAY = lambda user: user.username
#A callable (or string of the form 'some.module.callable_name') that takes a user as its only argument and returns the display name of the user. The default implementation returns user.username.
ACCOUNT_USERNAME_MIN_LENGTH = 1
#An integer specifying the minimum allowed length of a username.
ACCOUNT_USERNAME_BLACKLIST = []
#A list of usernames that can't be used by user.
ACCOUNT_USERNAME_REQUIRED = False
#The user is required to enter a username when signing up. Note that the user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set to email. Set to False when you do not wish to prompt the user to enter a username.
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
#render_value parameter as passed to PasswordInput fields.
ACCOUNT_PASSWORD_MIN_LENGTH = 6
#An integer specifying the minimum password length.

