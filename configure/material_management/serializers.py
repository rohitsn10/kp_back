from rest_framework import serializers
from material_management.models import *

class MaterialManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialManagement
        fields = ['id','sub_sub_activity','subactivity','projectactivity','user','project',
                  'vendor_name','material_name','uom','price','end_date','created_at','updated_at',
                  'PR_number','PO_number','quantity','status','payment_status']
        