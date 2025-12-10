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
    # We use this to point to your custom template (registration/login.html)
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 3. PASSWORD RESET / AUTH FIX: Includes all standard Django authentication URLs
    # This specifically resolves the "password_reset" error you were seeing.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 4. LOGOUT PATH: Uses Django's redirect function to immediately send the user to the homepage ('/')
    # This uses the LOGOUT_REDIRECT_URL setting we fixed earlier.
    path('logout/', redirect('home'), name='logout'), 
    
    # 5. App Includes
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('households/', include('households.urls', namespace='households')),
    path('data-tracker/', include('data_tracker.urls', namespace='data_tracker')),
]