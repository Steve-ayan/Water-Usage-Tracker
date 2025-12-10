from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# You may need to import your Household model if it's not available via request.user
from households.models import Household 
from .models import DailyUsage
from .forms import DailyUsageForm

@login_required
def log_usage(request):
    """
    Handles logging of daily water usage and implements Django Messages for feedback.
    """
    # 1. Check for Household existence
    try:
        # Assuming your CustomUser model has a 'household' attribute
        household = request.user.household
    except Household.DoesNotExist:
        # CRITICAL ERROR HANDLING: If user has no household
        messages.warning(request, "Please create or join a household before logging usage.")
        return redirect('households:create_household')

    if request.method == 'POST':
        # Ensure we pass the household instance to the form for context-aware validation
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
            # ERROR MESSAGE
            # Using 'error' tag for general validation failure
            messages.error(request, "Failed to log usage. Please check the form details and try again.")
            
    else:
        # GET request: Render the empty form
        form = DailyUsageForm(household=household)

    context = {'form': form}
    return render(request, 'data_tracker/log_usage.html', context)


@login_required
def edit_usage(request, pk):
    """
    Allows editing of a usage record with security checks and messages.
    """
    usage_record = get_object_or_404(DailyUsage, pk=pk)
    
    # SECURITY CHECK: Ensure the user belongs to the household associated with this record
    if request.user.household != usage_record.household: # Cleaner security check
        messages.error(request, "You do not have permission to edit this record.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        # Pass the existing instance to the form for editing
        form = DailyUsageForm(request.POST, instance=usage_record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usage record for {usage_record.date} updated successfully.")
            return redirect('dashboard:main_dashboard')
        else:
            # ERROR MESSAGE for validation failure during edit
            messages.error(request, "Failed to update record. Please correct the errors below.")
            
    else:
        # Pre-fill the form with existing data
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