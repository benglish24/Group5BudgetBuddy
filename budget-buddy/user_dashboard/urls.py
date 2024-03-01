from django.urls import path
from . import views

urlpatterns = [
    path('user-dash/', views.user_dash_view, name='user_dash'),
]
