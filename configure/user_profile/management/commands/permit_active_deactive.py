import time
from django.utils import timezone
from django.core.management.base import BaseCommand
from annexures_module.models import PermitToWork

class Command(BaseCommand):
    help = 'Check if expiry_date has passed and update is_active to False for expired permits.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Permit expiry check service started...\n")

        while True:
            now = timezone.now()
            expired_permits = PermitToWork.objects.filter(expiry_date__lte=now, is_active=True)

            for permit in expired_permits:
                permit.is_active = False
                permit.save(update_fields=['is_active'])
                self.stdout.write(
                    f"Permit '{permit.permit_number}' expired and set to inactive.\n"
                )

            self.stdout.write("Waiting for the next check...\n")
            time.sleep(60)