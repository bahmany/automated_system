"""
Django settings for bmps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils import timezone
from mongoengine import connect

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jp20ia%=42cm@4%f7(2!ppwkg^c6sovc2y9j=-a($8$i(46g+t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ws4redis',
    'fcm_django',
    "sslserver",

    'httpproxy',
    # 'compressor',
    # 'revproxy',
    'corsheaders',
    'captcha',
    'rest_framework',
    'rest_framework_mongoengine',
    # 'djcelery',
    # 'django_windows_tools',
    'amspApp.publicViews',
    'amspApp.Infrustructures',
    'amspApp',
    'amspApp.amspUser',
    'amspApp.MyProfile',
    'amspApp.CompaniesManagment',
    'amspApp.CompaniesManagment.Charts',
    'amspApp.CompaniesManagment.Positions',
    'amspApp.CompaniesManagment.Secretariat',
    'amspApp.Contacts',
    'amspApp.FileServer',
    'amspApp.Friends',
    'amspApp.UserSettings',
    'amspApp.Administrator.Customers',
    'amspApp.Administrator.Billings',
    'amspApp.Calendar',
    'amspApp.News',
    'amspApp.ControlProject',
    'amspApp.SpecialApps.****Cashflow',
    'amspApp.middlewares.defender',
    'amspApp.RequestGoods'

)

# dubug
# CURRENT_DOMAIN_WEB = 'localhost'
REDIS_IP_PASSWORD = 'localhost'
MYSQL_IP_PASSWORD = 'localhost'
MONGO_IP_PASSWORD = 'localhost'
# ELASTIC_IP_PASSWORD = 'localhost'
ELASTIC_IP_PASSWORD = '172.16.5.46'

# CURRENT_DOMAIN_WEB = 'localhost'
# REDIS_IP_PASSWORD = 'localhost'
# MYSQL_IP_PASSWORD = 'localhost'
# MONGO_IP_PASSWORD = 'localhost'
# ELASTIC_IP_PASSWORD = 'localhost'

FCM_DJANGO_SETTINGS = {
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}

WEBSOCKET_URL = '/ws/'

WS4REDIS_CONNECTION = {
    'host': REDIS_IP_PASSWORD,
    # 'port': 16379,
    # 'db': 17,
    # 'password': 'verysecret',
}
WS4REDIS_EXPIRE = 7200
WS4REDIS_PREFIX = 'ws'

WSGI_APPLICATION = 'ws4redis.django_runserver.application'
WS4REDIS_SUBSCRIBER = 'amspApp.redis_store.RedisSubscriber.RahsoonRedisSubscriber'
WS4REDIS_HEARTBEAT = '#'

SESSION_REDIS_HOST = REDIS_IP_PASSWORD



CSRF_COOKIE_NAME = "rahsoon-CSRF-TOKEN"
CSRF_HEADER_NAME = "rahsoon-csrftoken"

# INSTALLED_APPS += PUPUT_APPS

AUTH_USER_MODEL = 'amspUser.MyUser'

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = False
USE_TZ = False

LANGUAGES = (
    ('fa', 'Farsi'),
    ('en', 'English')
)

Temp_Path = os.path.realpath('.')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
APP_PATH = os.path.join(BASE_DIR, 'amspApp/')
FILE_PATH = "/home/mohammad/amspfiles/"
if os.name == 'nt':
    FILE_PATH = "d:/amspfiles/"
FILE_PATH_URL = "/api/v1/file/upload?q="

ABSOLUTE_PATH = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/www/amsPlusCache',
#         'TIMEOUT': 3600,

#         'ALIAS': "default",
#         'KEY_PREFIX': "default",
#         'OPTIONS': {
#             'MAX_ENTRIES': 5000
#         }
#     }
# }


CACHE_MIDDLEWARE_ALIAS = "default"

# ---------------------------
# ---------------------------
# activiti
# ACTIVITI_AUTH_URL = 'http://activiti.rahsoon.com:8080/activiti-app/app/authentication'
# ACTIVITI_HTTP_HOST = 'activiti.rahsoon.com:8080'
# ACTIVITI_HTTP_REFERER = 'http://activiti.rahsoon.com:8080/activiti-app'
# ACTIVITI_SERVER_PORT = '8080'
# ACTIVITI_SERVER_ORIGIN = 'http://activiti.rahsoon.com:8080'
# ---------------------------
# ---------------------------


MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'amspApp.Infrustructures.Classes.UrlDispacher.UrlAppCheck',

    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'amspApp.middlewares.MyCsrf.MyCsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'amspApp.Authentication.AnonymouseChecker.LoginRequiredMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'amspApp.middlewares.TimezoneMiddleware.TimezoneMiddleware',
    # 'amspApp.middlewares.XFrameOptionMiddleware.TFXFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'amspApp.middlewares.SessionTranslator.SessionTranslator',
    'amspApp.middlewares.SubDomainHandle.SubdomainHandle',
    'amspApp.middlewares.ForbiddenView.ForbiddenMiddleware',
    'amspApp.middlewares.onlineUsersMiddleware.ActiveUserMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'amspApp.middlewares.proxyMiddle.ProxyMiddleware',
    # 'amspApp.middlewares.onlineUsersMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',

)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
}
# CAPTCHA_OUTPUT_FORMAT = 'image'

WAGTAIL_SITE_NAME = 'Puput blog'

# it is temporary
# this line is for calling from old automation
# ----------------------------------------------------
X_FRAME_OPTIONS = 'ALLOWALL'
# ----------------------------------------------------
REST_FRAMEWORK = {
    'UNICODE_JSON': True,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # this bit makes the magic.
    'DEFAULT_RENDERER_CLASSES': (
        'amspApp.Infrustructures.render.myRenderer.myJSONRenderer',
        #         # 'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
    ,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)

}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin_mapraan',
        'USER': 'root',
        'HOST': 'localhost',
        'OPTIONS': {'charset': 'utf8'},
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'admin_mapraan',
#         'USER': 'admin_rahsoon',
#         'HOST': '172.16.5.42',
#         'PASSWORD': '****',
#         'OPTIONS': {'charset': 'utf8'},
#     }
# }

ELASTIC_INBOX_INDEXING_NAME = "inbox___"
ELASTIC_SEC_INDEXING_NAME = "sec___"
# ELASTIC_HOST = "172.16.0.40"
ELASTIC_HOST = ELASTIC_IP_PASSWORD
ELASTIC_USERNAME = "rahsoon"
ELASTIC_PASSWORD = "****"

# from mongengine import connect


connect("amsPlus")
# connect(db="amsPlus", host="172.16.5.41", username="rahsoon", password="****", authentication_source="amsPlus")

ROOT_URLCONF = 'amsp.urls'

# SUBDOMAIN_URLCONFS = {
# None: 'amsp.urls',  # no subdomain, e.g. ``example.com``
# 'www': 'amsp.urls',
#     'api': 'amsp.urls.api',
# }


LOGIN_URL = "/#/login"
LOGIN_EXEMPT_URLS = (
    r'^about\.html$',
    r'^legal/',  # allow the entire /legal/* subsection
)

MEDIA_ROOT = APP_PATH + 'static' + "/images"
MEDIA_URL = '/static/images/'
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


SESSION_COOKIE_AGE = 1209600
# SESSION_COOKIE_NAME = 'morabaaPlus'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(APP_PATH, 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                'django.core.context_processors.request',
            ],
            # 'builtins':
            #     ['amspApp.templatetags']

        }
    }
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'ws4redis.context_processors.default',
)

CORS_SERVERS = [
    "http://localhost",
    "http://rahsoon.com",
    "http://rahsoon.com:8001",
    "http://app.rahsoon.com",
    "http://app.rahsoon.com:8001",
    "http://localhost:8001",
    "http://127.0.0.1",
    "http://127.0.0.1:8001",
    "http://****.135.151:81",
    "http://****.135.151",
    "http://****.135.131",
    "http://****.135.131:81",
    "http://****.135.131:8001",
    "http://****.135.131:8888",
    "http://****.135.138:81",
    "http://****.135.138:8001",
    "http://****.135.138:8888",
    "http://morabaa.ir",
    "http://morabaa.ir:81",
    "http://morabaa.ir:8001",
    "http://morabaa.ir:8888",
    "http://****.ir",
    "http://rah.ir",
    "http://****.ir:81",
    "http://****.ir:8001",
    "http://rah.com:8001",
    "http://****.ir:8888",
    "http://app.morabaa.ir",
    "http://app.morabaa.ir:81",
    "http://app.morabaa.ir:8001",
    "http://app.morabaa.ir:8888",
    "http://app.****.ir",
    "http://app.****.ir:81",
    "http://app.****.ir:8001",
    "http://app.****.ir:8888",
]

USE_EMAIL_VERIFICATION_FOR_REGISTRATION = True

CURRENT_HOST = "rahsoon.com"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'rahsoon.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'noreplay@rahsoon.com'
EMAIL_HOST_PASSWORD = 'pClcBXQ3Kb'

# ACTIVITI_HTTP_HOST = 'activiti.rahsoon.com:8080'
# ACTIVITI_HTTP_REFERER = 'http://activiti.rahsoon.com:8080/activiti-app'


PASSWORD_USERNAME = "bahmanymb@gmail.com"
PASSWORD_PASS = "****"
PASSWORD_DBNAME = "morekhasi"

# ODOO_HTTP_REFERER = "http://127.0.0.1:8069"
# ODOO_HTTP_HOST = "127.0.0.1:8069"
# ODOO_DBNAME = "odoo12"
# ODOO_ADMIN = "bahmanymb@gmail.com"
# ODOO_PASSWORD = "****"
# ODOO_NET = "/web#action=117&model=maintenance.team&view_type=kanban&menu_id=82"
#
#
#
ODOO_Platform = "https://erp.****.com"

ODOO_HTTP_REFERER = "https://erp.****.com"
ODOO_HTTP_HOST = "erp.****.com"
ODOO_DBNAME = "net_test"
ODOO_ADMIN = "bahmanymb@gmail.com"
ODOO_PASSWORD = "****"
ODOO_NET = "/web#action=133&model=maintenance.team&view_type=kanban&menu_id=95"

#
# GOTIFY_AGENT = "http://"
# GOTIFY_SERVER = "192.168.0.151"
# GOTIFY_CLIENT_TOKEN_PASSWORD = "Cl5EK_v9syWr7Z5"
#


# ODOO_Platform = "https://****.com"
# import djcelery
# djcelery.setup_loader()
#
# # Redis configuration
# REDIS_PORT=6379
# REDIS_HOST = "127.0.0.1"
# REDIS_DB = 0
# REDIS_CONNECT_RETRY = True
#
# # Broker configuration
# BROKER_HOST = "127.0.0.1"
# BROKER_BACKEND="redis"
# BROKER_USER = ""
# BROKER_PASSWORD =""
# BROKER_VHOST = "0"
#
# # Celery Redis configuration
# CELERY_SEND_EVENTS=True
# CELERY_RESULT_BACKEND='redis'
# CELERY_REDIS_HOST='127.0.0.1'
# CELERY_REDIS_PORT=6379
# CELERY_REDIS_DB = 0
# CELERY_TASK_RESULT_EXPIRES = 10
# CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
# CELERY_ALWAYS_EAGER=False
#


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': 'd://rahsoon_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'CRITICAL',
            'propagate': True,
        },
    },
}


