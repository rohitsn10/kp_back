import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, ContentType

class Command(BaseCommand):
    help = 'Add permissions from a CSV file (with explicit IDs)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                content_type_id = int(row['content_type_id'])
                try:
                    content_type = ContentType.objects.get(id=content_type_id)
                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"ContentType with id={content_type_id} does not exist. Skipping permission '{row['codename']}'."
                    ))
                    continue
                perm, created = Permission.objects.update_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'codename': row['codename'],
                        'content_type': content_type,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added permission: {perm.codename} (id={perm.id})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated permission: {perm.codename} (id={perm.id})"))