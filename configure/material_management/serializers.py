from rest_framework import serializers
from material_management.models import *
from user_profile.function_call import *

class SubActivityNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = SubActivity
        fields = ['name']


# Serializer to handle SubSubActivity (Many-to-Many relationship)
class SubSubActivityNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = SubsubActivity
        fields = ['name']


class MaterialManagementSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    # project_activity_name = serializers.CharField(source='projectactivity.activity_name', read_only=True)
    # # Serialize subactivity names
    # subactivity_name = serializers.SerializerMethodField()
    
    # # Serialize sub_sub_activity names
    # sub_sub_activity_name = serializers.SerializerMethodField()

    class Meta:
        model = MaterialManagement
        fields = ['id','user','client_vendor_choices','project', 'project_name','client_name',
                  'vendor_name','material_number','material_name', 'uom', 'price', 'created_at', 'updated_at',
                  'PR_number','pr_date','PO_number','po_date','material_required_date','delivered_date','number_of_delay','quantity', 'status', 'payment_status']

    # def get_subactivity_name(self, obj):
    #     # Check if subactivity is not None before accessing related sub-activity
    #     if obj.subactivity and obj.subactivity.sub_activity.exists():
    #         subactivity = obj.subactivity.sub_activity.first()  # Get the first related sub-activity
    #         return subactivity.name if subactivity else None  # Return the name or None if no subactivity
    #     return None

    # def get_sub_sub_activity_name(self, obj):
    #     # Check if sub_sub_activity is not None before accessing related sub-sub-activity
    #     if obj.sub_sub_activity and obj.sub_sub_activity.sub_sub_activity.exists():
    #         subsubactivity = obj.sub_sub_activity.sub_sub_activity.first()  # Get the first related sub-sub-activity
    #         return subsubactivity.name if subsubactivity else None  # Return the name or None if no sub-sub-activity
    #     return None


class InspectionMaterialSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    is_approved_by_full_name = serializers.CharField(source='is_approved_by.full_name', read_only=True)
    inspection_quality_report_attachments = serializers.SerializerMethodField()
    
    
    class Meta:
        model = InspectionOfMaterial
        fields = ['id', 'material_management', 'user','user_full_name','inspection_date','inspection_quality_report','inspection_quality_report_attachments','is_inspection','is_approved','is_approved_by','is_approved_by_full_name','is_approved_date','is_approved_remarks','remarks','created_at','updated_at']
        
    def get_inspection_quality_report_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'inspection_quality_report_attachments')

