from django.urls import path
from .views import user_dashboard

app_name = 'user_dashboard'

urlpatterns = [
    path('', user_dashboard, name='user_dash'),
]
