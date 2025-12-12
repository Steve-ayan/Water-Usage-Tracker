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

# CRITICAL FOR LOCAL STABILITY: Ensure DEBUG is True
DEBUG = True 

# CRITICAL FOR LOCAL STABILITY: Only allow local hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# NOTE: The RENDER_EXTERNAL_HOSTNAME logic has been removed here for pure local testing.


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

# ... (MIDDLEWARE remains the same) ...
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # We leave whitenoise here as it is harmless for local development, 
    # but the static files configuration is simpler.
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

# CRITICAL FOR LOCAL STABILITY: Use SQLite directly
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


# --- STATIC FILES CONFIGURATION ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]

# REMOVE/COMMENT OUT FOR LOCAL TESTING: Production setting
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser' 

# --- REDIRECTION URLS ---
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'