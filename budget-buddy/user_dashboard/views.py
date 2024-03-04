from django.shortcuts import render
from .models import UserDashboard
from .decorators import authenticated_user

@authenticated_user
def user_dashboard(request):
    # Get or create the UserDashboard object for the current user
    user_dashboard, created = UserDashboard.objects.get_or_create(custom_user=request.user)

    # If the object was just created, it means it's empty and you might want to set default values here

    return render(request, 'user_dash.html', {'user_dashboard': user_dashboard})