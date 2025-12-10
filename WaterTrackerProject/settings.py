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
    
    # Custom Apps
    'users.apps.UsersConfig',
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

# Internationalization (unchanged)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES CONFIGURATION (The primary source of the error) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    # ENSURE THIS PATH IS CORRECT: BASE_DIR / 'static'
    BASE_DIR / 'static', 
]


# Default primary key field type (unchanged)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (unchanged)
AUTH_USER_MODEL = 'users.CustomUser'

# --- REDIRECTION URLS ---
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'