from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import landing_page
from django.shortcuts import redirect 
from django.views.generic import RedirectView

urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),
    
    # 1. ROOT PATH: (/) - Directs to the new, public landing page (name='home')
    path('', landing_page, name='home'),
    
    # 2. LOGIN PATH: Explicitly defines the 'login' path name
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 3. PASSWORD RESET / AUTH FIX: Includes all standard Django authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('logout/', include('django.contrib.auth.urls')),
    
    # 5. App Includes
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('households/', include('households.urls', namespace='households')),
    path('data-tracker/', include('data_tracker.urls', namespace='data_tracker')),
]
urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),
    
    # 1. ROOT PATH: (/) - Directs to the new, public landing page (name='home')
    path('', landing_page, name='home'),
    
    # 2. LOGIN PATH: Explicitly defines the 'login' path name
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 3. AUTH URLs: Includes everything else (password reset, logout, etc.)
    # The logout path will be /accounts/logout/ but the redirect URL will still be '/' (home).
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 4. App Includes (Same as before)
    path('users/', include('users.urls', namespace='users')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('households/', include('households.urls', namespace='households')),
    path('data-tracker/', include('data_tracker.urls', namespace='data_tracker')),
]