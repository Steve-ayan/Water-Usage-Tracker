from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm 
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # <-- CRITICAL FIX: Added import
from households.models import Household # <-- Required for view_profile

def register_user(request):
    """Handles user registration and immediate login."""
    if request.user.is_authenticated:
        return redirect('dashboard:main_dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            
            messages.success(request, f'Welcome, {user.username}! You are now registered and logged in.')
            return redirect('dashboard:main_dashboard') 
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def view_profile(request):
    """Displays the current user's details and household affiliation."""
    try:
        # Get the household the user belongs to
        household = Household.objects.filter(members=request.user).first()
    except Household.DoesNotExist:
        household = None
        
    context = {
        'user': request.user,
        'household': household,
    }
    return render(request, 'users/profile.html', context)