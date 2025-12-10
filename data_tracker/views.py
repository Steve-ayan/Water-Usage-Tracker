from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from households.models import Household 
from .models import DailyUsage
from .forms import DailyUsageForm

# NOTE: The log_usage view has been moved/integrated into dashboard/views.py 
# to resolve the circular dependency and post handling issues.

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
            # Display error on validation failure
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