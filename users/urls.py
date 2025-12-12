from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    # Core Authentication
    path('register/', views.register_user, name='register'),
    
    # Profile View
    path('profile/', views.view_profile, name='profile'), 
    
    # CRITICAL: NEW ACCOUNT CONTROL URLS
    path('profile/edit/', views.edit_profile, name='edit_profile'),        # Path for editing username/email
    path('profile/delete/', views.delete_account, name='delete_account'),  # Path for account deletion
]