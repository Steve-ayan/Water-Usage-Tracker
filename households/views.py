# households/views.py (COMPLETE, STABLE CODE)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# NOTE: Ensure these imports are correct based on your local app names
from .forms import HouseholdCreationForm
from .models import Household
from users.models import CustomUser 
from django.db.models import Q 

@login_required
def create_household(request):
    # 1. Check if the user already owns a household (Owner check)
    if Household.objects.filter(owner=request.user).exists():
        messages.warning(request, "You already own a household.")
        return redirect('dashboard:main_dashboard')

    # 2. Check if the user is already a member of any household (Member check - secondary safety)
    # This check prevents a user from creating a household if they are already a member of another.
    if Household.objects.filter(members=request.user).exists():
        messages.warning(request, "You are already a member of an existing household.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        form = HouseholdCreationForm(request.POST)
        if form.is_valid():
            household = form.save(commit=False)
            household.owner = request.user 
            household.save()
            
            # CRITICAL FIX: Save M2M relationship immediately after saving the main object
            household.members.add(request.user) # Add the owner as the first member
            
            # Since M2M fields are saved after the initial save, using .add() is preferred
            # over .set() for initial creation, though both work.
            
            messages.success(request, f"Household '{household.name}' successfully created! You are now logged into your dashboard.")
            
            # CRITICAL: We redirect, relying on the clean code to load the dashboard.
            return redirect('dashboard:main_dashboard')
        else:
            # If form is invalid (e.g., empty name), re-render the template with errors.
            messages.error(request, "Failed to create household. Please check the form.")
    else:
        form = HouseholdCreationForm()
        
    context = {'form': form}
    # NOTE: Assumes the template name is 'households/create_household.html'
    return render(request, 'households/create_household.html', context)


@login_required
def invite_member(request):
    try:
        # Only the owner of a household can send invitations
        household = Household.objects.get(owner=request.user)
    except Household.DoesNotExist:
        # Redirect if the user is not the owner (regardless of membership status)
        messages.error(request, "You must own a household to invite members.")
        return redirect('dashboard:main_dashboard')

    context = {'household': household, 'found_user': None}

    if request.method == 'POST':
        username_or_email = request.POST.get('search_user', '').strip()
        
        if not username_or_email:
            messages.error(request, "Please enter a username or email to search.")
            return render(request, 'households/invite_member.html', context)
        
        try:
            # Try to find a user by email or username
            user_to_invite = CustomUser.objects.get(
                Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
            )
            
            # Self-check
            if user_to_invite == request.user:
                messages.warning(request, "You cannot invite yourself.")
            
            # Already a member of this household
            elif user_to_invite in household.members.all():
                messages.warning(request, f"{user_to_invite.username} is already a member of {household.name}.")
            
            # Already owns another household
            elif Household.objects.filter(owner=user_to_invite).exists():
                messages.error(request, f"{user_to_invite.username} already owns their own household and cannot be invited.")
            
            else:
                # Add the user directly to the household 
                household.members.add(user_to_invite)
                messages.success(request, f"User {user_to_invite.username} has been successfully added to {household.name}!")
                return redirect('dashboard:main_dashboard')

        except CustomUser.DoesNotExist:
            messages.error(request, f"User '{username_or_email}' not found.")
            
    return render(request, 'households/invite_member.html', context)