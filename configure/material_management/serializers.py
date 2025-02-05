from rest_framework import serializers
from material_management.models import *

class MaterialManagementSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    class Meta:
        model = MaterialManagement
        fields = ['id','sub_sub_activity','subactivity','projectactivity','user','project','project_name',
                  'vendor_name','material_name','uom','price','end_date','created_at','updated_at',
                  'PR_number','PO_number','quantity','status','payment_status']
        