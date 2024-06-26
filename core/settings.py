from pathlib import Path
from django.conf import settings
import os
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

DEBUG = True


ALLOWED_HOSTS = ["localhost", "127.0.0.1", env("NGROK")]


INSTALLED_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.line",
    "django_celery_results",
    "accounts",
    "products",
    "django_htmx",
    "chats",
    "orders",
    "carts",
    "feedbacks",
    "storages",
    "django_seed",
    "managements",
    "coupons",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "carts.context_processors.cart",
                "products.context_processors.categories",
                "managements.context_processors.no_reply_count",
                "managements.context_processors.new_order_count",
            ],
        },
    },
]

ASGI_APPLICATION = "core.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "passfile": ".my_pgpass",
        },
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = "home"

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("CLIENT_ID"),
            "secret": env("SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "line": {
        "APP": {
            "client_id": env("LINE_LOGIN_CHANNEL_ID"),
            "secret": env("LINE_LOGIN_CHANNEL_SECRET"),
        },
        "SCOPE": ["profile", "openid", "email"],
    },
}


# 定義 SESSION 跟 cookie 的存活時間, 單位為秒
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"

# Related to reset email sender
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")


# Logs
# if settings.DEBUG:
#     LOGGING = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "handlers": {
#             "console": {
#                 "level": "DEBUG",
#                 "class": "rich.logging.RichHandler",
#                 "show_time": False,
#             },
#             "file": {
#                 "level": "DEBUG",
#                 "class": "logging.FileHandler",
#                 "filename": "logs/development.log",
#             },
#         },
#         "loggers": {
#             "django.db.backends": {
#                 "handlers": ["console", "file"],
#                 "level": "DEBUG",
#                 "propagate": False,
#             },
#         },
#     }

# AWS image-storage related
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "cakecapture"
AWS_S3_SIGNATURE_NAME = ("s3v4",)
AWS_S3_REGION_NAME = "ap-southeast-2"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Payment-related
CSRF_TRUSTED_ORIGINS = [env("DOMAIN")]

# LINE-chatbot related
LINE_CHANNEL_ACCESS_TOKEN = env("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = env("LINE_CHANNEL_SECRET")


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60
