from django.contrib import admin
from .models import DailyUsage

@admin.register(DailyUsage)
class DailyUsageAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('household', 'date', 'volume_liters')
    
    # Enable filtering by household and date
    list_filter = ('household', 'date')
    
    # Enable searching by volume
    search_fields = ('volume_liters',)