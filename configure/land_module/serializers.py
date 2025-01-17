from rest_framework import serializers
from land_module.models import *
from user_profile.models import *
import ipdb
from user_profile.function_call import *
class LandCategorySerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name',read_only=True)
    class Meta:
        model = LandCategory
        fields = ['id','user','user_full_name','category_name','created_at','updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        return representation

class ApprovedReportAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandApprovedReportAttachment
        fields = ['id', 'approved_report_file', 'created_at', 'updated_at']

    def to_representation(self, obj):
        # Manually define how the data should be represented
        representation = {
            "id": str(obj.id),  # Ensure the ID is returned as a string
            "url": self.context['request'].build_absolute_uri(obj.approved_report_file.url),  # Full URL of the file
            "created_at": obj.created_at.isoformat(),  # Format the created_at as ISO string with timezone
            "updated_at": obj.updated_at.isoformat()   # Format the updated_at as ISO string with timezone
        }
        return representation
    

class LandBankSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    land_location_file = serializers.SerializerMethodField()
    land_survey_number_file = serializers.SerializerMethodField()
    land_key_plan_file = serializers.SerializerMethodField()
    land_attach_approval_report_file = serializers.SerializerMethodField()
    land_approach_road_file = serializers.SerializerMethodField()
    land_co_ordinates_file = serializers.SerializerMethodField()
    land_proposed_gss_file = serializers.SerializerMethodField()
    land_transmission_line_file = serializers.SerializerMethodField()
    approved_report_file = ApprovedReportAttachmentSerializer(many=True)
    class Meta:
        model = LandBankMaster
        fields = [
            'id', 'user', 'user_full_name', 'created_at', 'updated_at',
            'land_location_file', 'land_survey_number_file', 'land_key_plan_file',
            'land_attach_approval_report_file', 'land_approach_road_file', 
            'land_co_ordinates_file', 'land_proposed_gss_file', 'land_transmission_line_file','land_bank_status','approved_report_file'
        ]

    def get_land_location_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_location_file')

    def get_land_survey_number_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_survey_number_file')

    def get_land_key_plan_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_key_plan_file')

    def get_land_attach_approval_report_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_attach_approval_report_file')

    def get_land_approach_road_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_approach_road_file')

    def get_land_co_ordinates_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_co_ordinates_file')

    def get_land_proposed_gss_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_proposed_gss_file')

    def get_land_transmission_line_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_transmission_line_file')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        return representation


class LandBankAfterApprovalSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    dilr_attachment_file = serializers.SerializerMethodField()
    na_65b_permission_attachment_file = serializers.SerializerMethodField()
    revenue_7_12_records_attachment = serializers.SerializerMethodField()
    noc_from_forest_and_amp_attachment_file = serializers.SerializerMethodField()
    noc_from_geology_and_mining_office_attachment_file = serializers.SerializerMethodField()
    approvals_required_for_transmission_attachment_file = serializers.SerializerMethodField()
    canal_crossing_attachment_file = serializers.SerializerMethodField()
    lease_deed_attachment_file = serializers.SerializerMethodField()
    railway_crossing_attachment_file = serializers.SerializerMethodField()
    any_gas_pipeline_crossing_attachment_file = serializers.SerializerMethodField()
    road_crossing_permission_attachment_file = serializers.SerializerMethodField()
    any_transmission_line_crossing_permission_attachment_file = serializers.SerializerMethodField()
    any_transmission_line_shifting_permission_attachment_file = serializers.SerializerMethodField()
    gram_panchayat_permission_attachment_file = serializers.SerializerMethodField()
    class Meta:
        model = LandBankAfterApprovedData
        fields = [
            'user','user_full_name','land_bank','dilr_attachment_file','na_65b_permission_attachment_file',
            'revenue_7_12_records_attachment','noc_from_forest_and_amp_attachment_file',
            'noc_from_geology_and_mining_office_attachment_file','approvals_required_for_transmission_attachment_file',
            'canal_crossing_attachment_file','lease_deed_attachment_file','railway_crossing_attachment_file',
            'any_gas_pipeline_crossing_attachment_file','road_crossing_permission_attachment_file',
            'any_transmission_line_crossing_permission_attachment_file','any_transmission_line_shifting_permission_attachment_file',
            'gram_panchayat_permission_attachment_file'
        ]
    

    def get_dilr_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'dilr_attachment_file')

    def get_na_65b_permission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'na_65b_permission_attachment_file')

    def get_revenue_7_12_records_attachment(self, obj):
        return get_file_data(self.context.get('request'), obj, 'revenue_7_12_records_attachment')

    def get_noc_from_forest_and_amp_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'noc_from_forest_and_amp_attachment_file')

    def get_noc_from_geology_and_mining_office_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'noc_from_geology_and_mining_office_attachment_file')

    def get_approvals_required_for_transmission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'approvals_required_for_transmission_attachment_file')

    def get_canal_crossing_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'canal_crossing_attachment_file')

    def get_lease_deed_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'lease_deed_attachment_file')

    def get_railway_crossing_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'railway_crossing_attachment_file')

    def get_any_gas_pipeline_crossing_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'any_gas_pipeline_crossing_attachment_file')

    def get_road_crossing_permission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'road_crossing_permission_attachment_file')

    def get_any_transmission_line_crossing_permission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'any_transmission_line_crossing_permission_attachment_file')

    def get_any_transmission_line_shifting_permission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'any_transmission_line_shifting_permission_attachment_file')

    def get_gram_panchayat_permission_attachment_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'gram_panchayat_permission_attachment_file')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        return representation