"""
Django settings for WaterTrackerProject project.
"""

from pathlib import Path
import os
import dj_database_url # For connecting to production database (PostgreSQL on Render)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*975d%w^ti4&uv*+g!7@^xj@9ako$lh@hi&8xv@0-wu^-+5y-n'

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG to False by default, but allow Render environment variable to override
DEBUG = os.environ.get('DEBUG', 'False') == 'True' 

# IMPORTANT: Render provides the environment variable RENDER_EXTERNAL_HOSTNAME
# ALLOWED_HOSTS is now configured to handle production domain/IP
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'users.apps.UsersConfig',
    'households.apps.HouseholdsConfig',
    'data_tracker.apps.DataTrackerConfig',
    'dashboard.apps.DashboardConfig',
    
    # Third-party Apps (for Bootstrap styling and Production)
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # NEW: WhiteNoise must be listed directly after SecurityMiddleware for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WaterTrackerProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'WaterTrackerProject.wsgi.application'


# Database Configuration (for Production/Render)
# Uses the DATABASE_URL environment variable provided by Render (for PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3'),
        conn_max_age=600
    )
}


# Password Validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) Configuration for Production
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# NEW: Directory where Django collects all static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles' 
# NEW: Tell Django to look for global static files in our project's static/ folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Authentication Redirect URLs
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/accounts/login/' 

# Optionally set this to True to compress static files (Nginx/Render optimization)
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }