"""
Django settings for cmdb project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.isfile(os.path.join(BASE_DIR, 'config.ini')):
    print("Please create config.ini first")
    exit(1)
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.ini'))

if 'DJANGO' not in config:
    exit(1)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('DJANGO', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('DJANGO', 'DEBUG')

ALLOWED_HOSTS = list(filter(None, str.split(config.get('DJANGO', 'ALLOWED_HOSTS', fallback=''), ',')))
ALLOWED_HOSTS.append('127.0.0.1')

# Application definition

INSTALLED_APPS = [
    'reversion',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'utils',
    'asset',
    'audits',
    'certificate',
    'dns',
    'domain',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cmdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'cmdb'),
        ],
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

WSGI_APPLICATION = 'cmdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASE_DEFAULT = config.get('DJANGO', 'DATABASE_DEFAULT')
DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE:' + DATABASE_DEFAULT, 'ENGINE', fallback='django.db.backends.sqlite3'),
        'NAME': config.get('DATABASE:' + DATABASE_DEFAULT, 'NAME', fallback='db.sqlite3'),
        'USER': config.get('DATABASE:' + DATABASE_DEFAULT, 'USER', fallback=''),
        'PASSWORD': config.get('DATABASE:' + DATABASE_DEFAULT, 'PASSWORD', fallback=''),
        'HOST': config.get('DATABASE:' + DATABASE_DEFAULT, 'HOST', fallback=''),
        'PORT': config.get('DATABASE:' + DATABASE_DEFAULT, 'PORT', fallback=''),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

LANGUAGES = (
    ('zh-hans', '简体中文'),
    ('en', 'English')
)
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = '/admin/login'

DJANGO_TITLE = config.get('DJANGO', 'TITLE', fallback='JUMP')

SM4_VI = config.get('DJANGO', 'SM4_VI')

PASSWORD_HASHERS = [
    'utils.hashers.PBKDF2SM3PasswordHasher',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'utils.authentication.AccessKeyAuthentication',
        # 'utils.authentication.AccessTokenAuthentication',
        # 'utils.authentication.PrivateTokenAuthentication',
        # 'utils.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/tmp/cmdb.cache',
            'TIMEOUT': 60,  # 过期时间，单位为秒
            'OPTIONS': {
                'MAX_ENTRIES': 1000  # 最大缓存数，当缓存的数量超过后删除旧的缓存
            }
        }
    }
