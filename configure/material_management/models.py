from django.db import models
from project_module.models import *
from activity_module.models import *

class MaterialManagement(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    STATUS = [
        ('in_progress', 'in_progress'),
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    
    CLIENT_VENDOR_CHOICES = [
        ('client', 'client'),
        ('vendor', 'vendor'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    # projectactivity = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE,null=True, blank=True)
    # subactivity = models.ForeignKey(SubActivityName, on_delete=models.CASCADE,null=True, blank=True)
    # sub_sub_activity = models.ForeignKey(SubSubActivityName, on_delete=models.CASCADE,null=True, blank=True)
    client_vendor_choices = models.CharField(max_length=20, choices=CLIENT_VENDOR_CHOICES, null=True, blank=True)
    client_name = models.CharField(max_length=500,null=True, blank=True)
    vendor_name = models.CharField(max_length=500,null=True, blank=True)
    material_number = models.CharField(max_length=500,null=True, blank=True)
    material_name = models.CharField(max_length=100,null=True, blank=True)
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
    
