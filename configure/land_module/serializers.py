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
    land_category_name = serializers.CharField(source='land_category.category_name', read_only=True)
    land_sfa_file = serializers.SerializerMethodField()
    sfa_for_transmission_line_gss_files = serializers.SerializerMethodField()
    land_location_file = serializers.SerializerMethodField()
    land_survey_number_file = serializers.SerializerMethodField()
    land_key_plan_file = serializers.SerializerMethodField()
    land_attach_approval_report_file = serializers.SerializerMethodField()
    land_approach_road_file = serializers.SerializerMethodField()
    land_co_ordinates_file = serializers.SerializerMethodField()
    land_lease_deed_file = serializers.SerializerMethodField()
    land_transmission_line_file = serializers.SerializerMethodField()
    approved_report_file = ApprovedReportAttachmentSerializer(many=True)
    sfa_approved_by_user_full_name = serializers.CharField(source='sfa_approved_by_user.full_name', read_only=True)
    sfa_rejected_by_user_full_name = serializers.CharField(source='sfa_rejected_by_user.full_name', read_only=True)
    class Meta:
        model = LandBankMaster
        fields = [
            'id', 'user', 'user_full_name','land_category','land_category_name','created_at', 'updated_at','solar_or_winds',
            'sfa_name','land_sfa_file','sfa_for_transmission_line_gss_files',
            'land_location_file', 'land_survey_number_file', 'land_key_plan_file',
            'land_attach_approval_report_file', 'land_approach_road_file', 
            'land_co_ordinates_file', 'land_lease_deed_file', 'land_transmission_line_file','land_bank_status',
            'approved_report_file','sfa_approved_by_user','sfa_rejected_by_user','sfa_approved_by_user_full_name',
            'sfa_rejected_by_user_full_name','land_name','timeline','status_of_site_visit','sfa_approved_by_user',
            'date_of_assessment','site_visit_date','sfa_checked_by_user','survey_number','village_name','taluka_name',
            'total_land_area','remaining_land_area','taluka_tahshil_name', 'old_block_number', 'new_block_number', 'sale_deed_date',
            'lease_deed_number', 'district_name', 'propose_gss_number', 'land_co_ordinates', 'land_status', 'area_meters', 
            'area_acres', 'industrial_jantri', 'jantri_value', 'mort_gaged', 'seller_name', 'buyer_name', 'actual_bucket',
            'remarks', 'index_number', 'tcr', 'advocate_name'
        ]

    def get_land_sfa_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_sfa_file')

    def get_sfa_for_transmission_line_gss_files(self, obj):
        return get_file_data(self.context.get('request'), obj, 'sfa_for_transmission_line_gss_files')
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

    def get_land_lease_deed_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'get_land_lease_deed_file')

    def get_land_transmission_line_file(self, obj):
        return get_file_data(self.context.get('request'), obj, 'land_transmission_line_file')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        return representation


class LandBankAfterApprovalSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    land_bank_name = serializers.CharField(source='land_bank.land_name', read_only=True)
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
    municipal_corporation_permission_file = serializers.SerializerMethodField()
    list_of_other_approvals_land_file = serializers.SerializerMethodField()
    title_search_report_file = serializers.SerializerMethodField()
    coordinate_verification_file = serializers.SerializerMethodField()
    encumbrance_noc_file = serializers.SerializerMethodField()
    developer_permission_file = serializers.SerializerMethodField()
    noc_from_ministry_of_defence_file = serializers.SerializerMethodField()
    list_of_approvals_required_for_transmission_line_file = serializers.SerializerMethodField()


    class Meta:
        model = LandBankAfterApprovedData
        fields = [
            'id', 'user', 'user_full_name', 'land_bank','land_bank_name',
            'dilr_attachment_file', 'na_65b_permission_attachment_file', 'revenue_7_12_records_attachment',
            'noc_from_forest_and_amp_attachment_file', 'noc_from_geology_and_mining_office_attachment_file',
            'approvals_required_for_transmission_attachment_file', 'canal_crossing_attachment_file',
            'lease_deed_attachment_file', 'railway_crossing_attachment_file',
            'any_gas_pipeline_crossing_attachment_file', 'road_crossing_permission_attachment_file',
            'any_transmission_line_crossing_permission_attachment_file', 'any_transmission_line_shifting_permission_attachment_file',
            'gram_panchayat_permission_attachment_file',
            'municipal_corporation_permission_file', 'list_of_other_approvals_land_file', 'title_search_report_file',
            'coordinate_verification_file', 'encumbrance_noc_file', 'developer_permission_file',
            'noc_from_ministry_of_defence_file','list_of_approvals_required_for_transmission_line_file','is_filled_22_forms'
        ]

    def get_file_data(self, obj, field_name):
        return get_file_data(self.context.get('request'), obj, field_name)

    def get_dilr_attachment_file(self, obj):
        return self.get_file_data(obj, 'dilr_attachment_file')
    
    def get_na_65b_permission_attachment_file(self, obj):
        return self.get_file_data(obj, 'na_65b_permission_attachment_file')
    
    def get_revenue_7_12_records_attachment(self, obj):
        return self.get_file_data(obj, 'revenue_7_12_records_attachment')
    
    def get_noc_from_forest_and_amp_attachment_file(self, obj):
        return self.get_file_data(obj, 'noc_from_forest_and_amp_attachment_file')
    
    def get_noc_from_geology_and_mining_office_attachment_file(self, obj):
        return self.get_file_data(obj, 'noc_from_geology_and_mining_office_attachment_file')
    
    def get_approvals_required_for_transmission_attachment_file(self, obj):
        return self.get_file_data(obj, 'approvals_required_for_transmission_attachment_file')
    
    def get_canal_crossing_attachment_file(self, obj):
        return self.get_file_data(obj, 'canal_crossing_attachment_file')
    
    def get_lease_deed_attachment_file(self, obj):
        return self.get_file_data(obj, 'lease_deed_attachment_file')
    
    def get_railway_crossing_attachment_file(self, obj):
        return self.get_file_data(obj, 'railway_crossing_attachment_file')
    
    def get_any_gas_pipeline_crossing_attachment_file(self, obj):
        return self.get_file_data(obj, 'any_gas_pipeline_crossing_attachment_file')
    
    def get_road_crossing_permission_attachment_file(self, obj):
        return self.get_file_data(obj, 'road_crossing_permission_attachment_file')
    
    def get_any_transmission_line_crossing_permission_attachment_file(self, obj):
        return self.get_file_data(obj, 'any_transmission_line_crossing_permission_attachment_file')
    
    def get_any_transmission_line_shifting_permission_attachment_file(self, obj):
        return self.get_file_data(obj, 'any_transmission_line_shifting_permission_attachment_file')
    
    def get_gram_panchayat_permission_attachment_file(self, obj):
        return self.get_file_data(obj, 'gram_panchayat_permission_attachment_file')
    
    def get_list_of_approvals_required_for_transmission_line_file(self, obj):
        return self.get_file_data(obj, 'list_of_approvals_required_for_transmission_line_file')
    
    def get_municipal_corporation_permission_file(self, obj):
        return self.get_file_data(obj, 'municipal_corporation_permission_file')
    
    def get_list_of_other_approvals_land_file(self, obj):
        return self.get_file_data(obj, 'list_of_other_approvals_land_file')
    
    def get_title_search_report_file(self, obj):
        return self.get_file_data(obj, 'title_search_report_file')
    
    def get_coordinate_verification_file(self, obj):
        return self.get_file_data(obj, 'coordinate_verification_file')
    
    def get_encumbrance_noc_file(self, obj):
        return self.get_file_data(obj, 'encumbrance_noc_file')
    
    def get_developer_permission_file(self, obj):
        return self.get_file_data(obj, 'developer_permission_file')
    
    def get_noc_from_ministry_of_defence_file(self, obj):
        return self.get_file_data(obj, 'noc_from_ministry_of_defence_file')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        return representation
    
class LandSurveyNumberSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    land_bank_name = serializers.CharField(source='land_bank.land_name', read_only=True)
    land_location_name = serializers.CharField(source='location_name.land_bank_location_name', read_only=True)
    land_survey_number_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = LandSurveyNumber
        fields = [
            'land_survey_number_id', 'user', 'user_full_name', 'land_bank', 'land_bank_name',
            'location_name','land_location_name','land_survey_number', 'created_at', 'updated_at'
        ]

class LandBankLocationSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    land_bank_name = serializers.CharField(source='land_bank.land_name', read_only=True)
    land_survey_number_data = serializers.SerializerMethodField()

    class Meta:
        model = LandBankLocation
        fields = [
            'id', 'user', 'user_full_name', 'land_bank', 'land_bank_name',
            'land_bank_location_name', 'created_at', 'updated_at', 'land_survey_number_data', 'total_land_area', 'near_by_area'
        ]
    def get_land_survey_number_data(self, obj):
        land_survey_numbers = LandSurveyNumber.objects.filter(location_name=obj)
        return LandSurveyNumberSerializer(land_survey_numbers, many=True).data



