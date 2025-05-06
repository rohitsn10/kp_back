from django.db import models
from project_module.models import *
from activity_module.models import *
from django.conf import settings

class MaterialManagement(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered')
    ]
    
    # CLIENT_VENDOR_CHOICES = [
    #     ('client', 'client'),
    #     ('vendor', 'vendor'),
    # ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    # projectactivity = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE,null=True, blank=True)
    # subactivity = models.ForeignKey(SubActivityName, on_delete=models.CASCADE,null=True, blank=True)
    # sub_sub_activity = models.ForeignKey(SubSubActivityName, on_delete=models.CASCADE,null=True, blank=True)
    # client_vendor_choices = models.CharField(max_length=20, choices=CLIENT_VENDOR_CHOICES, null=True, blank=True)
    # client_name = models.CharField(max_length=500,null=True, blank=True)
    vendor_code = models.CharField(max_length=500,null=True, blank=True)
    material_code = models.CharField(max_length=500,null=True, blank=True)
    # material_name = models.CharField(max_length=100,null=True, blank=True)
    uom = models.CharField(max_length=80,null=True, blank=True)
    price = models.CharField(max_length=100,null=True, blank=True)
    PR_number = models.CharField(max_length=100,null=True, blank=True)
    pr_date = models.DateTimeField(null=True, blank=True)
    PO_number = models.CharField(max_length=100,null=True, blank=True)
    po_date = models.DateTimeField(null=True, blank=True)
    material_required_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    number_of_delay = models.CharField(max_length=100,null=True, blank=True)
    quantity = models.CharField(max_length=100,null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, null=True, blank=True,default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, null=True, blank=True,default='pending')
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_approved = models.BooleanField(default=False, null=True, blank=True)
    is_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='is_approved_by_material',null=True, blank=True)
    is_approved_date = models.DateTimeField(null=True, blank=True)
    is_approved_remarks = models.TextField(null=True, blank=True)

class MaterialApprovalAction(models.Model):
    material = models.ForeignKey(MaterialManagement, on_delete=models.CASCADE,null=True, blank=True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
class MaterialQualityReportAttacchments(models.Model):
    material_management = models.ForeignKey(MaterialManagement, on_delete=models.CASCADE,null=True, blank=True)
    inspection_quality_report_attachments = models.FileField(upload_to='inspection_quality_report_attachments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class MaterialGTPAttachment(models.Model):
    material_management = models.ForeignKey(MaterialManagement, on_delete=models.CASCADE,null=True, blank=True)
    gtp_attachments = models.FileField(upload_to='gtp_attachments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class MaterialQAPAttachment(models.Model):
    material_management = models.ForeignKey(MaterialManagement, on_delete=models.CASCADE,null=True, blank=True)
    qap_attachments = models.FileField(upload_to='qap_attachments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
class InspectionOfMaterial(models.Model):
    material_management = models.ForeignKey(MaterialManagement, on_delete=models.CASCADE,null=True, blank=True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='is_inspection_by',null=True, blank=True)
    gtp = models.CharField(max_length=500,null=True, blank=True)
    qap = models.CharField(max_length=500,null=True, blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)
    inspection_quality_report = models.TextField(null=True, blank=True)
    inspection_quality_report_attachments = models.ManyToManyField(MaterialQualityReportAttacchments)
    inspection_gtp_attachments = models.ManyToManyField(MaterialGTPAttachment)
    inspection_qap_attachments = models.ManyToManyField(MaterialQAPAttachment)
    is_inspection = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='is_approved_by',null=True, blank=True)
    is_approved_date = models.DateTimeField(null=True, blank=True)
    is_approved_remarks = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
class InseptionOfMaterialApprovalAction(models.Model):
    inspection_of_material = models.ForeignKey(InspectionOfMaterial, on_delete=models.CASCADE,null=True, blank=True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)