# households/views.py (FULL, CORRECTED CODE)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HouseholdCreationForm
from .models import Household
from users.models import CustomUser # Import CustomUser
from django.db.models import Q      # Import Q object

@login_required
def create_household(request):
    # Check if the user already owns a household
    if Household.objects.filter(owner=request.user).exists():
        messages.warning(request, "You already own a household.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        form = HouseholdCreationForm(request.POST)
        if form.is_valid():
            household = form.save(commit=False)
            household.owner = request.user 
            household.save()
            
            # Use set() to explicitly set the user as the only initial member.
            household.members.set([request.user]) 
            
            messages.success(request, f"Household '{household.name}' successfully created!")
            return redirect('dashboard:main_dashboard')
    else:
        form = HouseholdCreationForm()
        
    context = {'form': form}
    return render(request, 'households/create_household.html', context)


@login_required
def invite_member(request):
    try:
        # Only the owner of a household can send invitations
        household = Household.objects.get(owner=request.user)
    except Household.DoesNotExist:
        # Check if they are a member, but not an owner (optional)
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
            
            # Prevent inviting yourself or someone already in the household
            if user_to_invite == request.user:
                messages.warning(request, "You cannot invite yourself.")
            
            elif user_to_invite in household.members.all():
                messages.warning(request, f"{user_to_invite.username} is already a member of {household.name}.")
            
            # Prevent inviting someone who already owns another household
            elif Household.objects.filter(owner=user_to_invite).exists():
                messages.error(request, f"{user_to_invite.username} already owns their own household and cannot be invited.")
            
            else:
                # Add the user directly to the household (Simple Join)
                household.members.add(user_to_invite)
                messages.success(request, f"User {user_to_invite.username} has been successfully added to {household.name}!")
                return redirect('dashboard:main_dashboard')

        except CustomUser.DoesNotExist:
            messages.error(request, f"User '{username_or_email}' not found.")
            
    return render(request, 'households/invite_member.html', context)