import os
from pathlib import Path

from backend.secret import GOOGLE_SECRET, VK_SECRET

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-s%%s73c!d69xuove83bhgy4jlloypvutr2$p%zu&x_fb)3*4w)')

DEBUG = int(os.getenv("DEBUG", 1))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost,backend,localho.st").split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'rest_framework.authtoken',
    'backend_api.apps.BackendApiConfig',
    'authorization.apps.AuthorizationConfig',
    'goods.apps.GoodsConfig',
    'orders.apps.OrdersConfig',
    'retail.apps.RetailConfig',
    'reviews.apps.ReviewsConfig',
    'managers.apps.ManagersConfig',
]

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1,http://localhost,http://backend,http://localho.st"
).split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

GOOGLE_OAUTH = GOOGLE_SECRET

VK_OAUTH = VK_SECRET

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SHOW_REQUEST_HEADERS': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'backend.middleware.LoggingMiddleware',
]

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'crystal',
    #     'USER': 'postgres',
    #     'PASSWORD': "12345",
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }

    'default': {
        'ENGINE': os.getenv("DB_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.getenv("DB_NAME", BASE_DIR / 'db.sqlite3'),
        'PORT': os.getenv("DB_PORT", 5432),
        'USER': os.getenv("POSTGRES_USER", ""),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", ""),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'UPLOADED_FILES_USE_URL': True,
}

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

AUTH_USER_MODEL = 'authorization.CrystalUser'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
