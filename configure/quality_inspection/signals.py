from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import ItemsProduct
from project_module.models import Project

@receiver(m2m_changed, sender=ItemsProduct.project.through)
def update_item_cpp_ipp(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        active_projects = instance.project.filter(is_active=True)

        if active_projects.exists():
            cpp_or_ipp_values = list(active_projects.values_list('cpp_or_ipp', flat=True))
            if 'cpp' in cpp_or_ipp_values:
                instance.cpp_ipp = 'cpp'
            elif 'ipp' in cpp_or_ipp_values:
                instance.cpp_ipp = 'ipp'
        else:
            instance.cpp_ipp = None

        instance.save(update_fields=["cpp_or_ipp"])
