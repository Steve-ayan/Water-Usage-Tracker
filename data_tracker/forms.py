from django import forms
from .models import DailyUsage

class DailyUsageForm(forms.ModelForm):
    # Optional: Use a DateInput widget for better usability in the browser
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DailyUsage
        # We only ask the user for the date and volume. 
        # The 'household' field will be set by the view function.
        fields = ['date', 'volume_liters']