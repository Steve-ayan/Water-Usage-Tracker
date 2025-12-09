from django.contrib import admin
from .models import Household

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('name', 'owner', 'get_member_count')
    
    # Use a filter for easy searching
    list_filter = ('owner',)
    
    # Helper method to display the number of members
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Members'