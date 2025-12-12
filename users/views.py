# users/views.py (STABLE CODE with EDIT and DELETE functionality)

from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm # <-- CRITICAL: Added CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model # <-- CRITICAL: Added logout and get_user_model
from django.contrib.auth.decorators import login_required 
from households.models import Household 
from django.db.models import Q # <-- Added for robust queries

User = get_user_model() # Get the CustomUser model reference

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
            # Note: This handles errors on the form itself (e.g., password mismatch)
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
        
    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def view_profile(request):
    """Displays the current user's details and household affiliation."""
    # Find the household the user belongs to
    household = Household.objects.filter(members=request.user).first()
    
    context = {
        'user': request.user,
        'household': household,
    }
    return render(request, 'users/profile.html', context)

# ----------------------------------------------------------------------
# NEW ACCOUNT CONTROL VIEWS
# ----------------------------------------------------------------------

@login_required
def edit_profile(request):
    """
    Allows the user to edit their profile information (username, email).
    """
    if request.method == 'POST':
        # Pass request.FILES for potential avatar handling later, instance is CRITICAL
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
        
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def delete_account(request):
    """
    Handles account deletion confirmation and process.
    """
    if request.method == 'POST':
        # Safely get the user object before logging them out
        user_to_delete = request.user
        logout(request) # Log out the user immediately 
        
        # All household affiliations (owner/member) and related data (DailyUsage) 
        # will be handled by CASCADE deletion defined in the models.
        user_to_delete.delete() 
        
        messages.success(request, 'Your account has been permanently deleted. We are sorry to see you go.')
        return redirect('/') # Redirect to the homepage/landing page

    # For GET request, display the confirmation page
    return render(request, 'users/delete_account.html')