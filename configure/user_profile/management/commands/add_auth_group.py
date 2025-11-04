from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

GROUPS = [
    (1, "Admin"),
    (2, "Viewer"),
    (3, "Quality Viewer"),
    (4, "Supervisor1"),
    (6, "TestUser"),
    (7, "LAND_HOD_FULL"),
    (8, "LAND_EXECUTIVE_FULL"),
    (9, "LAND_MANAGER_FULL"),
    (10, "ADMIN"),
    (11, "PROJECT_HOD_FULL"),
    (12, "PROJECT_ENGINEER_FULL"),
    (15, "PROJECT_ENGINEER"),
    (16, "PROJECT_MANAGER_FULL"),
]

class Command(BaseCommand):
    help = "Add groups to auth_group table with specific IDs"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE(f"Adding {len(GROUPS)} groups with specific IDs..."))
        for group_id, group_name in GROUPS:
            group = Group.objects.filter(id=group_id).first()
            if group:
                if group.name != group_name:
                    group.name = group_name
                    group.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated group id={group_id} to name: {group_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Group already exists: {group_name} (id={group_id})"))
            else:
                # Check if a group with this name exists with a different id
                existing = Group.objects.filter(name=group_name).first()
                if existing:
                    self.stdout.write(self.style.WARNING(
                        f"Group name '{group_name}' exists with id={existing.id}, not creating id={group_id}"
                    ))
                else:
                    Group.objects.create(id=group_id, name=group_name)
                    self.stdout.write(self.style.SUCCESS(f"Created group: {group_name} (id={group_id})"))
        self.stdout.write(self.style.SUCCESS("Group creation completed."))