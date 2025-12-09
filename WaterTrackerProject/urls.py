from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('dashboard.urls')), 
    
    path('users/', include('users.urls')),
    
    path('households/', include('households.urls')),
    
    path('data/', include('data_tracker.urls')), 
]