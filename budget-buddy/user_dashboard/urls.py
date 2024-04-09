from django.urls import path
from .views import *

# app_name = 'user_dashboard'

urlpatterns = [
    path('', user_dashboard, name='user_dash'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('update_transaction/<int:pk>', update_transaction, name='update_transaction'),
    path('delete_transaction/<int:pk>', delete_transaction, name='delete_transaction'),
    path('upload_transaction/', upload_transaction, name='upload_transaction'),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('delete_transactions/<int:category_id>/', delete_transactions, name='delete_transactions'),
    path('update_information/', update_information, name='update_information'),
    path('upload_receipt/', upload_receipt, name='upload_receipt'),
]
