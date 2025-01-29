from django.db import models
from project_module.models import *


class DocumentManagementAttachments(models.Model):
    document_attachments = models.FileField(upload_to='document_management_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentManagement(models.Model):
    CONFIDENTIAL_CHOICES = [
        ('public', 'Public'),
        ('international', 'International'),
        ('confidential', 'Confidential'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('archived', 'Archived'),
        ('approved', 'Approved'),
    ]
    documentname = models.CharField(max_length=100, null=True, blank=True)
    documentnumber = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    revision_number = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    confidentiallevel = models.CharField(max_length=50, choices=CONFIDENTIAL_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    document_attachments = models.ManyToManyField(DocumentManagementAttachments)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assign_users = models.ManyToManyField(CustomUser, related_name="assigned_documents", blank=True)