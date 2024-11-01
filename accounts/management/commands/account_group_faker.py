# class AccountGroup(models.Model):
#     NAMES_CHOICES = (
#         ("CASH_IN_HAND", "CASH IN HAND"),
#         ("BANK", "BANK"),
#         ("TRADE_DEBTORS", "TRADE DEBTORS"),
#         ("TRADE_CREDITORS", "TRADE CREDITORS"),
#         ("DIRECT_EXPENSES", "DIRECT EXPENSES"),
#         ("INDIRECT_EXPENSES", "INDIRECT EXPENSES"),
#         ("INVENTORY", "INVENTORY"),
#         (
#             "MAINTENANCE_EXPENSES_HUNTING_VEHICLES",
#             "MAINTENANCE EXPENSES, HUNTING VEHICLES",
#         ),
#         ("INCOME_TAX", "INCOME TAX"),
#         ("ACCOUNTS_RECEIVABLES", "ACCOUNTS RECEIVABLES"),
#         ("PREPAID_EXPENSES", "PREPAID EXPENSES"),
#         (
#             "MAINTENANCE_EXPENSES_OTHER_VEHICLES_EQUIPMENT",
#             "MAINTENANCE EXPENSES, OTHER VEHICLES & EQUIPMENT",
#         ),
#         ("PAYROLL_EXPENSES", "PAYROLL EXPENSES"),
#         ("ADMINISTRATIVE_EXPENSES", "ADMINISTRATIVE EXPENSES"),
#         ("ACCOUNTS_PAYABLE", "ACCOUNTS PAYABLE"),
#     )
#     name = models.CharField(max_length=50, choices=NAMES_CHOICES)

from django.core.management.base import BaseCommand, CommandError
from accounts.models import AccountGroup
from django.conf import settings


class Command(BaseCommand):
    help = "Create fake account groups"

    def handle(self, *args, **options):

        for key, name in settings.NAMES_CHOICES:
            try:
                AccountGroup.objects.get_or_create(name=key)  # Use 'name' here
                self.stdout.write(self.style.SUCCESS(f"Created account group {name}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating account group: {str(e)}")
                )
