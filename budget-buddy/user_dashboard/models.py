from django.db import models
from django.db.models import Sum
from users.models import CustomUser

class UserDashboard(models.Model):
    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saving_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    spending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_budget(self):
        # Perform budget calculation based on salary, saving percentage, etc.
        if self.salary * (self.saving_percentage / 100) == 0:
            return 0
        budget = self.salary * (self.saving_percentage / 100)
        budget = self.salary - budget

        # You can add more calculations based on your specific requirements
        return budget

    def total_amount_for_user(self):
        total = 0
        transactions = Transaction.objects.filter(user=self.custom_user)
        for transaction in transactions:
            total += transaction.amount
        return total

    def save(self, *args, **kwargs):
        # Calculate and update spending when saving UserDashboard instance
        self.spending = self.calculate_budget()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.custom_user.username}'s Dashboard"


class Category(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    name = models.TextField(max_length=100)

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date_of = models.DateField()

    # category = models.TextField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-date_of"]

    def __str__(self):
        return f"{self.date_of} | {self.amount}"

    def get_amount(self):
        return float(self.amount)

    def get_category(self):
        return str(self.category.name)


