# dashboard/views.py (Ultimate Safe Version)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
import json

@login_required
def dashboard_view(request):
    # CRITICAL FIX: All model/form/db dependencies are moved inside the function
    from households.models import Household
    from data_tracker.forms import DailyUsageForm
    from data_tracker.models import DailyUsage 
    from django.db.models import Sum
    
    # 1. Safely retrieve the user's household
    household = Household.objects.filter(members=request.user).first()

    if not household:
        # If no household is found, redirect to the creation page.
        messages.warning(request, "Please create or join a household to view your dashboard.")
        return redirect('households:create') 

    # 2. Initialize the form variable (Empty for GET/Pre-filled with POST errors for POST failure)
    form = DailyUsageForm()

    # 3. POST Handling
    if request.method == 'POST':
        form = DailyUsageForm(request.POST) 
        if form.is_valid():
            usage_record = form.save(commit=False)
            usage_record.household = household 
            
            try:
                usage_record.save()
                messages.success(request, f"Usage of {usage_record.volume_liters}L logged successfully!")
            except Exception:
                messages.error(request, "Error: Usage for this date already exists. Please edit the existing entry.")
            
            return redirect('dashboard:main_dashboard')
        else:
            messages.error(request, "Failed to log usage. Please check the form details for errors.")
            # The 'form' variable now holds the errors and is used in the final render below.

    # 4. Metrics & Chart Data Preparation 
    all_usage = DailyUsage.objects.filter(household=household).order_by('date')
    
    total_usage_sum = all_usage.aggregate(Sum('volume_liters'))['volume_liters__sum'] or 0.0
    unique_days_count = all_usage.values('date').distinct().count()
    member_count = household.members.count()
    
    if unique_days_count > 0:
        avg_daily_usage = total_usage_sum / unique_days_count
        avg_daily_per_member = avg_daily_usage / member_count if member_count > 0 else 0.0
    else:
        avg_daily_usage = 0.0
        avg_daily_per_member = 0.0
        
    dates = [entry.date.strftime("%b %d") for entry in all_usage]
    volumes = [float(entry.volume_liters) for entry in all_usage]
    
    dates_json = json.dumps(dates)
    volumes_json = json.dumps(volumes)

    recent_usage = all_usage.order_by('-date')[:10]
    
    context = {
        'household': household,
        'form': form, 
        'recent_usage': recent_usage,
        'chart_dates': dates_json,
        'chart_volumes': volumes_json,
        
        # METRICS
        'total_usage_sum': round(total_usage_sum, 2),
        'avg_daily_usage': round(avg_daily_usage, 2),
        'avg_daily_per_member': round(avg_daily_per_member, 2),
        'member_count': member_count,
        'days_tracked': unique_days_count,
    }
    return render(request, 'dashboard/main_dashboard.html', context)