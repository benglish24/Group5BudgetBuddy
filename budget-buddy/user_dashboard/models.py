from django.db import models

class FinancialData(models.Model):
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    saving_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    fixed_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    spending = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Financial Data for Salary: {self.salary}"
