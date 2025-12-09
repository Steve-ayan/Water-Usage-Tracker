from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DailyUsage
from .forms import DailyUsageForm

@login_required
def edit_usage(request, pk):
    # Retrieve the specific DailyUsage record, or return 404
    usage_record = get_object_or_404(DailyUsage, pk=pk)
    
    # SECURITY CHECK: Ensure the user belongs to the household associated with this record
    if request.user not in usage_record.household.members.all():
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
        # Pre-fill the form with existing data
        form = DailyUsageForm(instance=usage_record)
        
    context = {'form': form, 'usage_record': usage_record}
    return render(request, 'data_tracker/edit_usage.html', context)


@login_required
def delete_usage(request, pk):
    usage_record = get_object_or_404(DailyUsage, pk=pk)
    
    # SECURITY CHECK: Ensure the user belongs to the household associated with this record
    if request.user not in usage_record.household.members.all():
        messages.error(request, "You do not have permission to delete this record.")
        return redirect('dashboard:main_dashboard')

    if request.method == 'POST':
        usage_record.delete()
        messages.success(request, f"Usage record for {usage_record.date} deleted successfully.")
        return redirect('dashboard:main_dashboard')

    # If GET request, show confirmation page
    context = {'usage_record': usage_record}
    return render(request, 'data_tracker/delete_usage.html', context)