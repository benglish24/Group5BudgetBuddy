from django.db import models
from users.models import CustomUser

class UserDashboard(models.Model):
    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saving_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    spending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        # return self.custom_user.username + f"'s Dashboard"
        return f"{self.custom_user.username}'s Dashboard"

class Transaction(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default="")
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date_of = models.DateField()
    category = models.CharField(max_length=100, default="MISCELLANEOUS")

    # if limiting category choice to predefined:
    # class Catgories(models.IntegerChoices):
    #     GROCERIES = 0
    #     ENTERTAINMENT = 1
    #     UTILITIES = 2
    #     MISCELLANEOUS = 3

    # category = models.IntegerField(choices=Categories, default=Categories.MISCELLANEOUS)

    class Meta:
        ordering = ["-date_of"]

    def __str__(self):
        return f"{self.date_of} | {self.user} | {self.amount}"


