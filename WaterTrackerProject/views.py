from django.shortcuts import render, redirect # <-- CORRECTED: Added 'redirect'
from django.contrib.auth.decorators import login_required

# The new view for the public landing page
def landing_page(request):
    """
    Renders the public landing page. 
    If the user is logged in, redirects them to the main dashboard.
    """
    if request.user.is_authenticated:
        # If logged in, send them straight to the main dashboard
        return redirect('dashboard:main_dashboard')
        
    # If not logged in, show the introductory landing page
    return render(request, 'landing.html')


# You may have other view functions here, but this is the primary one we updated.
# If you have other view functions, make sure they are included below this line.