from django.db import models
from user_profile.models import *

class ProjectActivity(models.Model):
    SOLAR_OR_WIND_CHOICES = [
        ('Solar', 'Solar'),
        ('Wind', 'Wind')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    solar_or_wind = models.CharField(max_length=10, choices=SOLAR_OR_WIND_CHOICES, null=True, blank=True)
    activity_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

class SubActivity(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    
    
class SubActivityName(models.Model):
    project_main_activity = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE, related_name='activities_sub', null=True, blank=True)
    sub_activity = models.ManyToManyField(SubActivity)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    
class SubsubActivity(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    
    
class SubSubActivityName(models.Model):
    project_activity_id = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE, related_name='project_activity_data', null=True, blank=True)
    sub_activity_id = models.ForeignKey(SubActivityName, on_delete=models.CASCADE, related_name='activities_sub_data', null=True, blank=True)
    sub_sub_activity = models.ManyToManyField(SubsubActivity)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)




