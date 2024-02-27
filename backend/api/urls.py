from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("dashboard/", dashboard),
    path("transaction/", TransactionView.as_view()),
]