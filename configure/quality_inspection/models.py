from django.db import models
from project_module.models import *
from land_module.models import *


class ItemsProduct(models.Model):
    CATEGORY_CHOICES = [
        ('category_1', 'Category 1'),
        ('category_2', 'Category 2'),
        ('category_3', 'Category 3')
    ]
    project = models.ManyToManyField(Project, blank=True)
    item_number = models.CharField(max_length=255, null=True, blank=True)
    item_name = models.CharField(max_length=255, null=True, blank=True)
    item_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)
    cpp_ipp = models.CharField(max_length=255, null=True, blank=True)
    dicipline = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class Vendor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ForeignKey(ItemsProduct, on_delete=models.CASCADE, null=True, blank=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class MQAPUpload(models.Model):
    file = models.FileField(upload_to='mqap_files/', null=True, blank=True)
    mqap_revision_number = models.CharField(max_length=255, null=True, blank=True)
    mqap_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class QualityDossierUpload(models.Model):
    file = models.FileField(upload_to='quality_dossier_files/', null=True, blank=True)
    quality_dossier_revision_number = models.CharField(max_length=255, null=True, blank=True)
    quality_dossier_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class DrawingUpload(models.Model):
    file = models.FileField(upload_to='drawing_files/', null=True, blank=True)
    drawing_revision_number = models.CharField(max_length=255, null=True, blank=True)
    drawing_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class DataSheetUpload(models.Model):
    file = models.FileField(upload_to='data_sheet_files/', null=True, blank=True)
    data_sheet_revision_number = models.CharField(max_length=255, null=True, blank=True)
    data_sheet_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class SpecificationUpload(models.Model):
    file = models.FileField(upload_to='specification_files/', null=True, blank=True)
    specification_revision_number = models.CharField(max_length=255, null=True, blank=True)
    specification_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class MDCCUpload(models.Model):
    file = models.FileField(upload_to='mdcc_files/', null=True, blank=True)
    mdcc_revision_number = models.CharField(max_length=255, null=True, blank=True)
    mdcc_revision_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class QualityInspection(models.Model):
    INSPECTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ForeignKey(ItemsProduct, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    is_venodr_verified = models.BooleanField(default=False, null=True, blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    inspection_status = models.CharField(max_length=255, null=True, blank=True)
    mqap_upload = models.ManyToManyField(MQAPUpload, blank=True)
    quality_dossier_upload = models.ManyToManyField(QualityDossierUpload, blank=True)
    drawing_upload = models.ManyToManyField(DrawingUpload, blank=True)
    data_sheet_upload = models.ManyToManyField(DataSheetUpload, blank=True)
    specification_upload = models.ManyToManyField(SpecificationUpload, blank=True)
    mdcc_upload = models.ManyToManyField(MDCCUpload, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)












class RFIFieldActivity(models.Model):
    FIELD_CHOICES = [
        ('mechanical', 'Mechanical'),
        ('electrical', 'Electrical'),
        ('civil', 'Civil')
    ]
    CLASSIFICATION_CHOICES = [
        ('table_work', 'Table Work'),
        ('buildings', 'Buildings'),
        ('other', 'Other')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    rfi_activity = models.CharField(max_length=255,choices=FIELD_CHOICES, null=True, blank=True)
    rfi_number = models.CharField(max_length=255, null=True, blank=True)
    rfi_classification = models.CharField(max_length=255,choices=CLASSIFICATION_CHOICES, null=True, blank=True)
    rfi_other = models.TextField(null=True, blank=True)
    epc_name = models.CharField(max_length=255, null=True, blank=True)
    offered_date = models.DateTimeField(null=True, blank=True)
    # detail_of_work = models.TextField(null=True, blank=True)
    block_number = models.CharField(max_length=255, null=True, blank=True)
    table_number = models.CharField(max_length=255, null=True, blank=True)
    activity_description = models.TextField(null=True, blank=True)
    hold_details = models.TextField(null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    construction_activity = models.CharField(max_length=255, null=True, blank=True)
    documents = models.ManyToManyField('InspectionOutcomeDocument', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Observation(models.Model):
    observation = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class InspectionOutcome(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    rfi_field_activity = models.ForeignKey(RFIFieldActivity, on_delete=models.CASCADE, null=True, blank=True)
    offered_time = models.TimeField(null=True, blank=True)
    reaching_time = models.TimeField(null=True, blank=True)
    inspection_start_time = models.TimeField(null=True, blank=True)
    inspection_end_time = models.TimeField(null=True, blank=True)
    observation = models.ManyToManyField(Observation, blank=True)
    # epc_name = models.CharField(max_length=255, null=True, blank=True)
    # epc_signature = models.FileField(upload_to='rfi_inspection_signature/', null=True, blank=True)
    # supervisor_name = models.CharField(max_length=255, null=True, blank=True)
    # supervisor_signature = models.FileField(upload_to='rfi_inspection_signature/', null=True, blank=True)
    disposition_status = models.CharField(max_length=255, null=True, blank=True)
    actions = models.TextField(null=True, blank=True)
    responsibility = models.CharField(max_length=255, null=True, blank=True)
    timelines = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    # documents = models.ManyToManyField('InspectionOutcomeDocument', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class InspectionOutcomeDocument(models.Model):
    rfi = models.ForeignKey(RFIFieldActivity, on_delete=models.CASCADE, null=True, blank=True)
    inspection_outcome = models.ForeignKey(InspectionOutcome, on_delete=models.CASCADE, null=True, blank=True)
    document = models.FileField(upload_to='inspection_outcome_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)