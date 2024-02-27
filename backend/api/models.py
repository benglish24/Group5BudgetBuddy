from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    category = models.TextField(max_length=100, default="Misc.")
    date_of = models.DateField()

    def __str__(self):
        return f"{self.user}: {self.amount}"