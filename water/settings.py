import os
from pathlib import Path
from datetime import timedelta
from django.conf import settings

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key (for production, consider using environment variables or Django's settings management tools)
SECRET_KEY = 'django-insecure-ze!gb-!-1wr1@xmm8kfxpg@(05a5*dqh(mg1rb7odc($e2#^=y'

DEBUG = True
# The line `# DATA_UPLOAD_MAX_NUMBER_FIELDS=1000` is a commented-out line in the Django settings file.
# In Django, `DATA_UPLOAD_MAX_NUMBER_FIELDS` is a setting that controls the maximum number of fields
# that will be processed in a form submitted via a POST request.
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.8.9', '*']
# ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # 'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    # 'django_admin_tools',  # Add this
    'setups',
    'periods',
    'customers',
    # 'crum',
    # 'reads',
    'reads.apps.ReadsConfig',
    'bills',
    'banks',
    'process',
    'reports',
    'employees',
    'loans',
    'stocks',
    'vaults',
    'challenge',
    'smart_selects',
    # 'django_celery_beat',
    # 'bill_upload',
    # 'hr',
]
LANGUAGE_CODE = 'am'
# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'EXCEPTION_HANDLER.rest_framework.views.exception_handler',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # For public access, adjust according to your needs
        'rest_framework.permissions.IsAuthenticated',  # Use for authentication-based access
    ],
}

# JWT Token configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Adjust as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token lifetime
}

# settings.py

# Middleware configuration
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# CORS (Cross-Origin Resource Sharing) settings
CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

CORS_ALLOWED_ORIGINS = ["http://192.168.8.9", "http://192.168.8.9:8081"]
CORS_ALLOW_ALL_ORIGINS = True  # Temporarily allow all origins for debugging

# URL configurations
ROOT_URLCONF = 'water.urls'

# Templates settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ensure templates are in the correct directory
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

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # or your preferred path
# MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL = '/media/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default auto field setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database configuration (For Oracle)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'NAME': 'xe',
#         'USER': 'system',
#         'PASSWORD': 'Life5591',
#         'HOST': 'localhost',
#         'PORT': '1521',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wbsdb',
        'USER': 'zemenu',
        'PASSWORD': 'Life5591',
        'HOST': 'localhost',  # Use '127.0.0.1' if localhost doesn't work
        'PORT': '3306',  # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Or your Redis URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }