# WaterTrackerProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import landing_page
from django.shortcuts import redirect 

urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),
    
    # 1. ROOT PATH: (/) - Directs to the new, public landing page (name='home')
    path('', landing_page, name='home'),
    
    # 2. LOGIN PATH: Explicitly defines the 'login' path name
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 3. AUTH URLs: Includes everything else (password reset, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 4. App Includes
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('households/', include('households.urls', namespace='households')),
    path('data-tracker/', include('data_tracker.urls', namespace='data_tracker')),
]