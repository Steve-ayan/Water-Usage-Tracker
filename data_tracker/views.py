from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from households.models import Household 
from .models import DailyUsage
from .forms import DailyUsageForm

@login_required
def log_usage(request):
    """
    Handles logging of daily water usage. On failure, it sets an error message 
    and redirects back to the dashboard, relying on the messages framework to 
    display the error without needing to re-render the entire dashboard context.
    """
    # 1. Check for Household existence
    try:
        household = request.user.household
    except Household.DoesNotExist:
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
            
            messages.success(request, f"Usage of {usage.liters_used} Liters logged successfully for {usage.date}.")
            return redirect('dashboard:main_dashboard') 
        else:
            # FAILURE PATH: Display general error message
            messages.error(request, "Failed to log usage. Please check the volume and date entered.")
            
            # Since the form is embedded in the dashboard (which is a different view), 
            # we must redirect and rely on the messages framework to display the error.
            # Field-specific errors may not appear here, but the general message will.
            return redirect('dashboard:main_dashboard')
            
    # If a GET request somehow hits this view (e.g., direct link), send them to the dashboard
    return redirect('dashboard:main_dashboard')


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
            # FIX: Display error on validation failure
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
        messages.success(request, f"Usage record for {usage_record.date} deleted successfully.")
        return redirect('dashboard:main_dashboard')

    context = {'usage_record': usage_record}
    return render(request, 'data_tracker/delete_usage.html', context)