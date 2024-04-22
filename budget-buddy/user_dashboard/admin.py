from django.contrib import admin
from .models import UserDashboard, Transaction, Category

# Register your models here.
admin.site.register(UserDashboard)
admin.site.register(Transaction)
admin.site.register(Category)