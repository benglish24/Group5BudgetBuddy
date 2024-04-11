from django.db import models
from django.db.models import Sum
from users.models import CustomUser
from datetime import date, timedelta


class UserDashboard(models.Model):
    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saving_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fixed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    spending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequency_choices = [
        ('Weekly', 'Weekly'),
        ('Bi-weekly', 'Bi-weekly'),
        ('Monthly', 'Monthly')
    ]
    frequency = models.CharField(max_length=10, choices=frequency_choices, default='Weekly')  # New field for frequency choice

    def calculate_budget(self):
        # Perform budget calculation based on salary, saving percentage, etc.
        if self.salary * (self.saving_percentage / 100) == 0:
            return 0
        budget = self.salary * (self.saving_percentage / 100)
        budget = self.salary - budget - self.total_amount
        return budget

    def total_amount_for_user(self):
        total = Transaction.objects.filter(
                    user=self.custom_user,
                    date_of__range=[self.start_date, self.end_date]
                ).aggregate(total_amount=Sum('amount'))['total_amount']
        return total or 0


    def save(self, *args, **kwargs):
        # Calculate and update different values when saving UserDashboard instance
        self.end_date = self.calculate_end_date()
        self.total_amount = self.total_amount_for_user()
        self.spending = self.calculate_budget()
        super().save(*args, **kwargs)

    def calculate_end_date(self):
        if self.start_date and self.frequency:
            if self.frequency == 'Weekly':
                return self.start_date + timedelta(days=7)
            elif self.frequency == 'Bi-weekly':
                return self.start_date + timedelta(days=14)
            elif self.frequency == 'Monthly':
                # Calculate end of month
                next_month = self.start_date.replace(day=28) + timedelta(days=4)  # Move to end of month
                return next_month - timedelta(days=next_month.day)
            else:
                raise ValueError("Invalid frequency")
        return None  # Return None if start_date or frequency is not set

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


