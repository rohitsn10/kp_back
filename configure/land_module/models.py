from django.db import models
from user_profile.models import *

class LandCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandLocationAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_location_file = models.FileField(upload_to='land_location', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandSurveyNumbeAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_survey_number_file = models.FileField(upload_to='land_survey_number', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandKeyPlanAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_key_plan_file = models.FileField(upload_to='land_key_plan', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandAttachApprovalReportAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_attach_approval_report_file = models.FileField(upload_to='land_attach_approval_report', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandApproachRoadAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_approach_road_file = models.FileField(upload_to='land_approach_road', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandCoOrdinatesAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_co_ordinates_file = models.FileField(upload_to='land_co_ordinates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandProposedGssAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_proposed_gss_file = models.FileField(upload_to='land_proposed_gss', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandTransmissionLineAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_transmission_line_file = models.FileField(upload_to='land_transmission_line', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandBankMaster(models.Model):
    SOLAR_WIND_CHOICES = (
        ('Solar', 'Solar'),
        ('Wind', 'Wind'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_category = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    land_name = models.TextField()
    land_location_file = models.ManyToManyField(LandLocationAttachment)
    land_survey_number_file = models.ManyToManyField(LandSurveyNumbeAttachment)
    land_key_plan_file = models.ManyToManyField(LandKeyPlanAttachment)
    land_attach_approval_report_file = models.ManyToManyField(LandAttachApprovalReportAttachment)
    land_approach_road_file = models.ManyToManyField(LandApproachRoadAttachment)
    land_co_ordinates_file = models.ManyToManyField(LandCoOrdinatesAttachment)
    land_proposed_gss_file = models.ManyToManyField(LandProposedGssAttachment)
    land_transmission_line_file = models.ManyToManyField(LandTransmissionLineAttachment)
    solar_or_winds = models.CharField(max_length=10, choices=SOLAR_WIND_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
