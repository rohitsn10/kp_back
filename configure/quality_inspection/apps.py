from django.apps import AppConfig


class QualityInspectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quality_inspection'

    def ready(self):
        import quality_inspection.signals