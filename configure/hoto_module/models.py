from django.db import models
from project_module.models import *
from user_profile.models import *

class DocumentsForHoto(models.Model):
    file = models.FileField(upload_to='hoto_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class HotoDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    document = models.ManyToManyField(DocumentsForHoto, blank=True)
    document_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    verify_comment = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)