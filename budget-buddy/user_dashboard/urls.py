from django.urls import path
from .views import *

# app_name = 'user_dashboard'

urlpatterns = [
    path('', user_dashboard, name='user_dash'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('update_transaction/<int:pk>', update_transaction, name='update_transaction'),
    path('delete_transaction/<int:pk>', delete_transaction, name='delete_transaction'),
]
