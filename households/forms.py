from django import forms
from .models import Household

class HouseholdCreationForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['name']