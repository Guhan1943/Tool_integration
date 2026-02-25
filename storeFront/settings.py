"""
Django settings for storeFront project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# -----------------------
# Base Directory
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------
# GitHub OAuth Credentials
# -----------------------
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# -----------------------
# GitHub App Credentials
# -----------------------
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")

PRIVATE_KEY_FILENAME = os.getenv("GITHUB_APP_PRIVATE_KEY_PATH")

if not PRIVATE_KEY_FILENAME:
    raise Exception("GITHUB_APP_PRIVATE_KEY_PATH not set in .env")

GITHUB_APP_PRIVATE_KEY_PATH = BASE_DIR / PRIVATE_KEY_FILENAME

if not GITHUB_APP_ID:
    raise Exception("GITHUB_APP_ID not set in .env")


# -----------------------
# Security
# -----------------------
SECRET_KEY = 'django-insecure-bq7g$d0ztdz9f@273frvky^yr*vf+lmku=we8n1hu_ydgn6ss%'

DEBUG = True

ALLOWED_HOSTS = []


# -----------------------
# Applications
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "tool_integration",
]


# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'storeFront.urls'


# -----------------------
# Templates
# -----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'storeFront.wsgi.application'


# -----------------------
# Database
# -----------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------
# Password Validation
# -----------------------
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


# -----------------------
# Internationalization
# -----------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# -----------------------
# Static Files
# -----------------------
STATIC_URL = 'static/'