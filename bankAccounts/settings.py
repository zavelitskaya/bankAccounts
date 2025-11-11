import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-spih8sy365m$g%6&&^p$a9$#ya3qw6i6!6d9$!1m955u$@*vip'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bmstu_lab',  # ваше приложение
    'storages',   # для MinIO
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

ROOT_URLCONF = 'bankAccounts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "bmstu_lab/templates"],
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

WSGI_APPLICATION = 'bankAccounts.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bmstu_lab/static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ВРЕМЕННО отключаем MinIO настройки - закомментируйте эти строки:
# AWS_ACCESS_KEY_ID = 'admin'
# AWS_SECRET_ACCESS_KEY = 'password123'
# AWS_STORAGE_BUCKET_NAME = 'bankaccounts'
# AWS_S3_ENDPOINT_URL = 'http://172.18.0.2:9000'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_USE_SSL = False
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# MinIO S3 settings
AWS_ACCESS_KEY_ID = 'minioadmin'
AWS_SECRET_ACCESS_KEY = 'minioadmin'
AWS_STORAGE_BUCKET_NAME = 'bankaccounts'  # имя вашего бакета
AWS_S3_ENDPOINT_URL = 'http://minio:9000'  # ВАЖНО: 'minio' вместо localhost
AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}'

# Настройки для работы с файлами
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_USE_SSL = False  # Для HTTP

# Используем S3 для медиа файлов
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL для доступа к медиа файлам
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'