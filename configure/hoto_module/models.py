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

class PunchFile(models.Model):
    file = models.FileField(upload_to='punch_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
class PunchPointsRaise(models.Model):
    hoto = models.ForeignKey(HotoDocument, on_delete=models.CASCADE, null=True, blank=True)
    punch_title = models.CharField(max_length=255, null=True, blank=True)
    punch_description = models.TextField(null=True, blank=True)
    punch_point_raised = models.TextField(null=True, blank=True)
    closure_date = models.DateField(null=True, blank=True)
    # punch_point_completed = models.TextField(null=True, blank=True)
    punch_point_balance = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    punch_file = models.ManyToManyField(PunchFile, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class CompletedPunchFile(models.Model):
    file = models.FileField(upload_to='completed_punch_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
class CompletedPunchPoints(models.Model):
    raise_punch = models.ForeignKey(PunchPointsRaise, on_delete=models.CASCADE, null=True, blank=True)
    punch_description = models.TextField(null=True, blank=True)
    # punch_point_raised = models.TextField(null=True, blank=True)
    punch_point_completed = models.TextField(null=True, blank=True)
    # punch_point_balance = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    punch_file = models.ManyToManyField(CompletedPunchFile, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='completed_punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class VerifyPunchPoints(models.Model):
    completed_punch = models.ForeignKey(CompletedPunchPoints, on_delete=models.CASCADE, null=True, blank=True)
    verify_description = models.TextField(null=True, blank=True)
    # punch_point_completed = models.TextField(null=True, blank=True)
    # punch_point_balance = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='verify_punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)