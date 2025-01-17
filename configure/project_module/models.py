from django.db import models
from user_profile.models import *
from land_module.models import *

class Company(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="companies",verbose_name="User")
    company_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project(models.Model):
    CI_UTILITY_CHOICES = [
        ('ci', 'CI'),
        ('utility', 'Utility'),
    ]

    CPP_IPP_CHOICES = [
        ('cpp', 'CPP'),
        ('ipp', 'IPP'),
    ]

    PROJECT_ACTIVITY_CHOICES = [
        ('wind', 'Wind'),
        ('solar', 'Solar'),
        ('hybrid_solar', 'Hybrid Solar'),
        ('hybrid_wind', 'Hybrid Wind'),
    ]

    ELECTRICITY_LINE_CHOICES = [
        ('11kv', '11KV'),
        ('33kv', '33KV'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_projects')
    project_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    location_name = models.ForeignKey(LandBankLocation, on_delete=models.CASCADE, related_name='projects_location')
    location_survey = models.ManyToManyField(LandSurveyNumber, related_name='projects_survey')
    cod_commission_date = models.DateTimeField(null=True, blank=True)
    total_area_of_project = models.TextField(null=True, blank=True)
    capacity = models.TextField(null=True, blank=True)
    ci_or_utility = models.CharField(max_length=10, choices=CI_UTILITY_CHOICES)
    cpp_or_ipp = models.CharField(max_length=10, choices=CPP_IPP_CHOICES)
    project_choice_activity = models.CharField(max_length=20, choices=PROJECT_ACTIVITY_CHOICES)
    electricity_line = models.CharField(max_length=5, choices=ELECTRICITY_LINE_CHOICES)
    spoc_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='spoc_projects')
    project_predication_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
