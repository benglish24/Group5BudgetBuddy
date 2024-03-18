from django.core.management.base import BaseCommand
from user_dashboard.models import Transaction

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Transaction.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all entries in Transaction table.'))