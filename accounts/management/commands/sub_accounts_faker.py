from django.core.management.base import BaseCommand, CommandError
from accounts.models import SubAccount
from django.conf import settings


class Command(BaseCommand):
    help = "Create fake account groups"

    def handle(self, *args, **options):

        for key, name in settings.SUB_ACCOUNT_NAMES_CHOICES:
            try:
                SubAccount.objects.get_or_create(name=key)  # Use 'name' here
                self.stdout.write(self.style.SUCCESS(f"Created account group {name}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating account group: {str(e)}")
                )
