# users/urls.py (FULL CODE)
from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('profile/', views.view_profile, name='profile'), # <-- NEW PATH
]