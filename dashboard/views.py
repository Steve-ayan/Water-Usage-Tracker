from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from households.models import Household
from data_tracker.forms import DailyUsageForm
from data_tracker.models import DailyUsage 
from django.contrib import messages
import json
from django.db.models import Sum, Count # NEW IMPORT: for database aggregation
from datetime import timedelta

@login_required
def dashboard_view(request):
    if not Household.objects.filter(owner=request.user).exists():
        return redirect('households:create') 
    
    household = Household.objects.get(owner=request.user) 

    if request.method == 'POST':
        form = DailyUsageForm(request.POST)
        if form.is_valid():
            usage_record = form.save(commit=False)
            usage_record.household = household 
            
            try:
                usage_record.save()
                messages.success(request, f"Usage of {usage_record.volume_liters}L logged for {usage_record.date}.")
            except Exception:
                messages.error(request, f"Error: Usage for {usage_record.date} already exists. Please edit the existing entry.")
            
            return redirect('dashboard:main_dashboard')

    else:
        form = DailyUsageForm()

    # --- METRICS & CHART DATA PREPARATION (UPDATED) ---
    
    # 1. Fetch data
    all_usage = DailyUsage.objects.filter(household=household).order_by('date')
    
    # 2. Calculate Totals and Averages
    total_usage_sum = all_usage.aggregate(Sum('volume_liters'))['volume_liters__sum'] or 0.0
    unique_days_count = all_usage.values('date').distinct().count()
    member_count = household.members.count() # Get the number of members (1 for now)
    
    # Calculate Averages
    if unique_days_count > 0:
        # Average Daily Usage (Total Liters / Number of Unique Days Tracked)
        avg_daily_usage = total_usage_sum / unique_days_count
        
        # Average Daily Usage PER MEMBER
        avg_daily_per_member = avg_daily_usage / member_count if member_count > 0 else 0.0
    else:
        avg_daily_usage = 0.0
        avg_daily_per_member = 0.0
        
    # 3. Chart Data Preparation
    dates = [entry.date.strftime("%b %d") for entry in all_usage]
    volumes = [float(entry.volume_liters) for entry in all_usage]
    
    dates_json = json.dumps(dates)
    volumes_json = json.dumps(volumes)

    # 4. Fetch Recent Records
    recent_usage = all_usage.order_by('-date')[:10]
    
    context = {
        'household': household,
        'form': form,
        'recent_usage': recent_usage,
        'chart_dates': dates_json,
        'chart_volumes': volumes_json,
        
        # NEW METRICS
        'total_usage_sum': round(total_usage_sum, 2),
        'avg_daily_usage': round(avg_daily_usage, 2),
        'avg_daily_per_member': round(avg_daily_per_member, 2),
        'member_count': member_count,
        'days_tracked': unique_days_count,
    }
    return render(request, 'dashboard/main_dashboard.html', context)