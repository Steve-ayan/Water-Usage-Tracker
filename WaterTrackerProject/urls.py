# WaterTrackerProject/urls.py (ULTIMATE STATIC FILE FIX)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth.views import LoginView
# Assuming 'landing_page' is not used since you are using TemplateView
# from .views import landing_page 

urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),
    
    # User authentication paths (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # App Includes
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('households/', include('households.urls')),
    path('data-tracker/', include('data_tracker.urls')),

    # Landing Page URL (Root)
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
]

# CRITICAL FIX: This code ensures your logo (and other static assets) are served locally.
# It uses the STATICFILES_DIRS[0] which explicitly points to your root static folder.
if settings.DEBUG:
    # Use the static files configuration to explicitly point to the static folder.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])