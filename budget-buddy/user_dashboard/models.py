from django.db import models
from users.models import CustomUser

class UserDashboard(models.Model):
    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saving_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    spending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.custom_user.username + "'s Dashboard"
