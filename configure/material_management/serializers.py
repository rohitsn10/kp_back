from rest_framework import serializers
from material_management.models import *

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
    
    # Serialize subactivity names
    subactivity_name = serializers.SerializerMethodField()
    
    # Serialize sub_sub_activity names
    sub_sub_activity_name = serializers.SerializerMethodField()

    class Meta:
        model = MaterialManagement
        fields = ['id', 'sub_sub_activity', 'subactivity', 'projectactivity', 'user', 'project', 'project_name',
                  'vendor_name', 'material_name', 'uom', 'price', 'end_date', 'created_at', 'updated_at',
                  'PR_number', 'PO_number', 'quantity', 'status', 'payment_status', 'subactivity_name', 'sub_sub_activity_name']

    def get_subactivity_name(self, obj):
        # Check if subactivity is not None before accessing related sub-activity
        if obj.subactivity and obj.subactivity.sub_activity.exists():
            subactivity = obj.subactivity.sub_activity.first()  # Get the first related sub-activity
            return subactivity.name if subactivity else None  # Return the name or None if no subactivity
        return None

    def get_sub_sub_activity_name(self, obj):
        # Check if sub_sub_activity is not None before accessing related sub-sub-activity
        if obj.sub_sub_activity and obj.sub_sub_activity.sub_sub_activity.exists():
            subsubactivity = obj.sub_sub_activity.sub_sub_activity.first()  # Get the first related sub-sub-activity
            return subsubactivity.name if subsubactivity else None  # Return the name or None if no sub-sub-activity
        return None
        