from django.db import models

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

    