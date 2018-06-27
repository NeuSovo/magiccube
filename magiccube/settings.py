"""
Django settings for magiccube project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j95hufw$g)i%b$ylac_iar*-a1o-l+d3+sx&a%y_9h0z_#gs5e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#Email设置

ADMINS = (
    ('Admins','*'),
)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.exmail.qq.com'
EMAIL_PORT= 465        
EMAIL_HOST_USER = 'i@zxh326.cn'  
EMAIL_HOST_PASSWORD = 'Zxh326//' 
EMAIL_SUBJECT_PREFIX = 'website' 
EMAIL_USE_SSL = True 
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER 

SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "cms",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'magiccube.urls'

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

WSGI_APPLICATION = 'magiccube.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# Proposed other projects are set to True,
# this project is for groups so special No need to set
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/img')
MEDIA_URL = '/media/'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
 
#celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json',]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
 
#celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE


# SIMDITOR_UPLOAD_PATH = 'uploads/'
# SIMDITOR_IMAGE_BACKEND = 'pillow'

# SIMDITOR_TOOLBAR = [
#     'title', 'bold', 'italic', 'underline', 'strikethrough', 'fontScale',
#     'color', '|', 'ol', 'ul', 'blockquote', '|', 'link',
#     'image', 'hr', '|', 'indent', 'outdent', 'alignment', 'fullscreen',
# ]

# SIMDITOR_CONFIGS = {
#     'toolbar': SIMDITOR_TOOLBAR,
#     'upload': {
#         'url': '/simditor/upload/',
#         'fileKey': 'upload'
#     },
#     'emoji': {
#         'imagePath': '/static/simditor/images/emoji/'
#     }
# }