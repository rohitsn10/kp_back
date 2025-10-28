import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Assign permissions to groups from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                group_id = int(row['group_id'])
                permission_id = int(row['permission_id'])
                try:
                    group = Group.objects.get(id=group_id)
                    permission = Permission.objects.get(id=permission_id)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(
                        f"Added permission {permission.codename} to group {group.name}"
                    ))
                except Group.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Group ID {group_id} does not exist"))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Permission ID {permission_id} does not exist"))