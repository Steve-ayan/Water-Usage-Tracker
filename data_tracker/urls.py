from django.urls import path
from . import views

app_name = 'data_tracker'

urlpatterns = [
    # NOTE: The core logging functionality remains in dashboard/views.py for simplicity
    path('edit/<int:pk>/', views.edit_usage, name='edit_usage'), # <-- NEW
    path('delete/<int:pk>/', views.delete_usage, name='delete_usage'), # <-- NEW
]