from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(' ')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

LOCAL_APPS = [
    'trainer_backend.core',
    'trainer_backend.user',
    'trainer_backend.trainer',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trainer_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', 'http://localhost'
).split(' ')

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'DELETE',
    'OPTIONS',
    'PATCH',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    # Main headers
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    # Extra headers
    'cache-control',
    'pragma',
    'expires',
    'x-frame-options',
    'x-forwarded-for',
    'x-forwarded-proto',
    'x-real-ip',
]

WSGI_APPLICATION = 'trainer_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
        'NAME': os.getenv('DB_NAME', ''),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASS', ''),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_RESET_URL = os.getenv('PASSWORD_RESET_URL', '')
CONFIRM_EMAIL_URL = os.getenv('CONFIRM_EMAIL_URL', '')

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'
TIME_ZONE = os.getenv('TZ', 'Asia/Vladivostok')
USE_I18N = True
USE_TZ = False

DATE_INPUT_FORMATS = [
    '%d.%m.%Y',  # '25-10-2006'
    '%Y-%m-%d',  # '2006-10-25'
]
DATETIME_INPUT_FORMATS = [
    '%d.%m.%Y %H:%M:%S',  # '25.10.2006 14:30:59'
    '%d.%m.%Y %H:%M:%S.%f',  # '25.10.2006 14:30:59.000200'
    '%d.%m.%Y %H:%M',  # '25.10.2006 14:30'
    '%d.%m.%y %H:%M:%S',  # '25.10.06 14:30:59'
    '%d.%m.%y %H:%M:%S.%f',  # '25.10.06 14:30:59.000200'
    '%d.%m.%y %H:%M',  # '25.10.06 14:30'
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR.parent.parent, 'static')
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, 'media')

DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME', '')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD', '')


DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '')

# Celery
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_SCAN_COUNT = os.getenv('REDIS_SCAN_COUNT', 999999999)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Celery
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
)
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/2'
)
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER', 'pickle')
CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER', 'pickle')
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE', TIME_ZONE)
CELERY_ENABLE_UTC = os.getenv('CELERY_ENABLE_UTC', 'False') == 'True'
CELERY_IMPORTS = []
CELERY_BEAT_SCHEDULE = {}