from django.urls import path
from . import views

app_name = 'households'

urlpatterns = [
    path('create/', views.create_household, name='create'),
    path('invite/', views.invite_member, name='invite'),
]