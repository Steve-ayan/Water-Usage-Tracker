"""
Django settings for WaterTrackerProject project.
"""

from pathlib import Path
import os
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-*975d%w^ti4&uv*+g!7@^xj@9ako$lh@hi&8xv@0-wu^-+5y-n' # Local fallback key
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True' 

ALLOWED_HOSTS = [] 
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('water-usage-tracker.onrender.com') 
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps (CRITICAL: Order is essential for model relationships)
    'users.apps.UsersConfig',         # MUST be first as others depend on CustomUser
    'households.apps.HouseholdsConfig',
    'data_tracker.apps.DataTrackerConfig',
    'dashboard.apps.DashboardConfig',
    
    # Third-party Apps
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Internationalization 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES CONFIGURATION (CRITICAL FIXES HERE) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]

# CRITICAL FIX: Ensure WhiteNoise is configured for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser' # This is already correct

# --- REDIRECTION URLS ---
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'