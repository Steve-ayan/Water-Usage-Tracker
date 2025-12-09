"""
Django settings for WaterTrackerProject project.
"""

from pathlib import Path
import os
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-*975d%w^ti4&uv*+g!7@^xj@9ako$lh@hi&8xv@0-wu^-+5y-n'

# SECURITY WARNING: Setting DEBUG to False for production environment.
DEBUG = os.environ.get('DEBUG', 'False') == 'True' 


# --- CRITICAL FIX: ALLOWED_HOSTS ---
# This ensures the Render domain is accepted when DEBUG=False, solving the 400 error.
ALLOWED_HOSTS = ['water-usage-tracker.onrender.com'] # <-- YOUR LIVE DOMAIN ADDED EXPLICITLY

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# --- END ALLOWED_HOSTS FIX ---


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


# Database Configuration (for Production/Render)
# We prioritize the DATABASE_URL environment variable provided by Render.
DATABASES = {
    'default': dj_database_url.config(
        # We explicitly provide the full internal URL as the default to ensure connection robustness
        default=os.environ.get(
            'DATABASE_URL', 
            'postgresql://water_tracker_app_user:lpGJe0OOINqDBtHBT99DzdhhnNb03fnV@dpg-d4s25oje5dus73atuub0-a/water_tracker_app'
        ),
        conn_max_age=600
    )
}


# Password Validation (unchanged)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization (unchanged)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images) Configuration
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Default primary key field type (unchanged)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (unchanged)
AUTH_USER_MODEL = 'users.CustomUser'

# Authentication Redirect URLs (unchanged)
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/accounts/login/'