from django.contrib.auth.forms import UserCreationForm, UserChangeForm # CRITICAL: Added UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser instances (Registration).
    Inherits from Django's base UserCreationForm.
    """
    class Meta:
        model = CustomUser
        # We only ask for email and username during creation
        fields = ('email', 'username',) 

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing CustomUser instances (Edit Profile).
    Inherits from Django's base UserChangeForm.
    """
    class Meta:
        model = CustomUser
        # Fields user is allowed to change on their profile
        fields = ('email', 'username',) 
        # We exclude the password fields from the profile edit form
        
    # CRITICAL FIX: We need to override the clean method to ensure 'password'
    # and 'last_login' are not required during a profile edit, as is standard
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password field and date/time fields which are not editable
        if 'password' in self.fields:
            del self.fields['password']
        if 'last_login' in self.fields:
            del self.fields['last_login']
        if 'date_joined' in self.fields:
            del self.fields['date_joined']