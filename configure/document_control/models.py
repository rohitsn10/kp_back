from django.db import models
from project_module.models import *
from django.conf import settings


class DocumentManagementAttachments(models.Model):
    document_management_attachments = models.FileField(upload_to='document_management_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DocumentManagement(models.Model):
    CONFIDENTIAL_CHOICES = [
        ('Public', 'Public'),
        ('International', 'International'),
        ('Confidential', 'Confidential'),
    ]
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Archived', 'Archived'),
        ('Approved', 'Approved'),
    ]
    document_name = models.CharField(max_length=100, null=True, blank=True)
    document_number = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    revision_number = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    confidentiallevel = models.CharField(max_length=50, choices=CONFIDENTIAL_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    document_management_attachments = models.ManyToManyField(DocumentManagementAttachments)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assign_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_documents", blank=True)
    updated_at = models.DateTimeField(auto_now=True)
