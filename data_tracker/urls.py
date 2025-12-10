# data_tracker/urls.py

from django.urls import path
from . import views

app_name = 'data_tracker'

urlpatterns = [
    # The log_usage path is REMOVED as the dashboard view handles the POST
    
    path('edit/<int:pk>/', views.edit_usage, name='edit_usage'), 
    path('delete/<int:pk>/', views.delete_usage, name='delete_usage'),
]