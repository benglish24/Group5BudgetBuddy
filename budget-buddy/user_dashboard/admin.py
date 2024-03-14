from django.contrib import admin
from .models import UserDashboard, Transaction

# Register your models here.
admin.site.register(UserDashboard)
admin.site.register(Transaction)