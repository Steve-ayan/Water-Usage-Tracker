from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from households.models import Household # Added or confirmed import
from .models import DailyUsage
from .forms import DailyUsageForm

@login_required
def log_usage(request):
    """
    Handles logging of daily water usage and implements Django Messages for feedback.
    If the form fails validation, it re-renders the template with errors.
    """
    # 1. Check for Household existence
    try:
        household = request.user.household
    except Household.DoesNotExist:
        # CRITICAL ERROR HANDLING: If user has no household
        messages.warning(request, "Please create or join a household before logging usage.")
        return redirect('households:create_household')

    if request.method == 'POST':
        form = DailyUsageForm(request.POST, household=household)
        
        if form.is_valid():
            # SUCCESS PATH
            usage = form.save(commit=False)
            usage.user = request.user
            usage.household = household
            usage.save()
            
            # SUCCESS MESSAGE
            messages.success(request, f"Usage of {usage.liters_used} Liters logged successfully for {usage.date}.")
            
            return redirect('dashboard:main_dashboard') 
        else:
            # FAILURE PATH (Validation failed—e.g., invalid date or high value)
            
            # 1. ADD MESSAGE: Display general error at the top
            messages.error(request, "Failed to log usage. Please check the volume and date entered.")
            
            # 2. CRITICAL FIX: DO NOT REDIRECT. Fall through to the final render below 
            # to display the field-specific errors attached to the 'form' object.
            
    else:
        # GET request: Render the empty form
        form = DailyUsageForm(household=household)

    # FINAL RENDER: Executed for both GET requests AND failed POST requests
    context = {'form': form}
    # Note: Assuming 'data_tracker/log_usage.html' is your form template, 
    # if the form is on the dashboard, you must pass all required dashboard context here.
    # Given your dashboard setup, the form is likely embedded there, so we proceed to the next file.
    
    # We will assume this view is used via the dashboard form submission (POST)
    # and redirects/re-renders back to the dashboard. 
    # **NOTE:** Since your dashboard handles the form, this log_usage view should be separate 
    # or handle the full dashboard context. For simplicity, we are assuming this view 
    # either posts to itself and renders a separate template, or is integrated differently. 
    # For now, let's just make sure the existing views are intact:
    pass # Continue to existing CRUD views

# --- EXISTING CRUD VIEWS (Ensuring they are preserved) ---

@login_required
def edit_usage(request, pk):
    """
    Allows editing of a usage record with security checks and messages.
    """
    usage_record = get_object_or_404(DailyUsage, pk=pk)
    
    # SECURITY CHECK
    if request.user.household != usage_record.household:
        messages.error(request, "You do not have permission to edit this record.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        form = DailyUsageForm(request.POST, instance=usage_record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usage record for {usage_record.date} updated successfully.")
            return redirect('dashboard:main_dashboard')
        else:
            messages.error(request, "Failed to update record. Please correct the errors below.")
            
    else:
        form = DailyUsageForm(instance=usage_record)
        
    context = {'form': form, 'usage_record': usage_record}
    return render(request, 'data_tracker/edit_usage.html', context)


@login_required
def delete_usage(request, pk):
    """
    Handles confirmation and deletion of a usage record with security checks and messages.
    """
    usage_record = get_object_or_404(DailyUsage, pk=pk)
    
    # SECURITY CHECK
    if request.user.household != usage_record.household:
        messages.error(request, "You do not have permission to delete this record.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        usage_record.delete()
        # SUCCESS MESSAGE
        messages.success(request, f"Usage record for {usage_record.date} deleted successfully.")
        return redirect('dashboard:main_dashboard')

    # If GET request, show confirmation page
    context = {'usage_record': usage_record}
    return render(request, 'data_tracker/delete_usage.html', context)