from django.db import models
from project_module.models import *
from user_profile.models import *


class DocumentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Category name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=255)  # Document name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class DocumentsForHoto(models.Model):
    file = models.FileField(upload_to='hoto_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Document File: {self.file.name if self.file else 'No File'}"


class HotoDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    document = models.ManyToManyField(DocumentsForHoto, blank=True)  # Stores uploaded files
    document_name = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)  # Links to the Document model
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, null=True, blank=True)  # Links to the DocumentCategory model
    is_uploaded = models.BooleanField(default=False)  # Indicates if the document is uploaded
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    verify_comment = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.document_name.name if self.document_name else 'Unnamed Document'} - {self.project.name if self.project else 'No Project'}"

class PunchFile(models.Model):
    file = models.FileField(upload_to='punch_files/', null=True, blank=True)
    file_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class AcceptedRejectedPunchFile(models.Model):
    file = models.FileField(upload_to='accepted_rejected_punch_files/', null=True, blank=True)
    file_status = models.CharField(max_length=255, null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class PunchPointsRaise(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    punch_title = models.CharField(max_length=255, null=True, blank=True)
    punch_description = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=None, null=True, blank=True)  # Accepted or Rejected
    status = models.CharField(max_length=255, null=True, blank=True)
    punch_file = models.ManyToManyField(PunchFile, blank=True)
    accepted_rejected_points = models.ManyToManyField(AcceptedRejectedPunchFile, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class CompletedPunchFile(models.Model):
    file = models.FileField(upload_to='completed_punch_files/', null=True, blank=True)
    file_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class AcceptedRejectedPunchPoints(models.Model):
    raise_punch = models.ForeignKey(PunchPointsRaise, on_delete=models.CASCADE, null=True, blank=True)
    punch_description = models.TextField(null=True, blank=True)
    tentative_timeline = models.DateTimeField(null=True, blank=True)  # Tentative timeline for acceptance/rejection
    comments = models.TextField(null=True, blank=True)  # Comments from the Project Team
    status = models.CharField(max_length=255, null=True, blank=True)
    punch_file = models.ManyToManyField(AcceptedRejectedPunchFile, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='completed_punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class CompletedPunchPoints(models.Model):
    accepted_rejected_punch = models.ForeignKey(AcceptedRejectedPunchPoints, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    punch_file = models.ManyToManyField(CompletedPunchFile, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='completion_punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class VerifyPunchPoints(models.Model):
    completed_punch = models.ForeignKey(CompletedPunchPoints, on_delete=models.CASCADE, null=True, blank=True)
    verify_description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='verify_punch_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)