from rest_framework import serializers
from land_module.models import *
from user_profile.models import *
import ipdb

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

    class Meta:
        model = LandBankMaster
        fields = [
            'id', 'user', 'user_full_name', 'created_at', 'updated_at',
            'land_location_file', 'land_survey_number_file', 'land_key_plan_file',
            'land_attach_approval_report_file', 'land_approach_road_file', 
            'land_co_ordinates_file', 'land_proposed_gss_file', 'land_transmission_line_file','land_bank_status'
        ]

    def get_land_location_file(self, obj):
        return self.get_file_data(obj, 'land_location_file')

    def get_land_survey_number_file(self, obj):
        return self.get_file_data(obj, 'land_survey_number_file')

    def get_land_key_plan_file(self, obj):
        return self.get_file_data(obj, 'land_key_plan_file')

    def get_land_attach_approval_report_file(self, obj):
        return self.get_file_data(obj, 'land_attach_approval_report_file')

    def get_land_approach_road_file(self, obj):
        return self.get_file_data(obj, 'land_approach_road_file')

    def get_land_co_ordinates_file(self, obj):
        return self.get_file_data(obj, 'land_co_ordinates_file')

    def get_land_proposed_gss_file(self, obj):
        return self.get_file_data(obj, 'land_proposed_gss_file')

    def get_land_transmission_line_file(self, obj):
        return self.get_file_data(obj, 'land_transmission_line_file')

    def get_file_data(self, obj, field_name):
        # Get the related ManyToMany field (e.g., land_location_file, land_survey_number_file, etc.)
        field = getattr(obj, field_name, None)
        if field:
            request = self.context.get('request')
            # Here, directly access the correct file field (e.g., land_location_file for LandLocationAttachment)
            file_field_name = field_name  # Correctly reference the file field without adding '_file' at the end
            return [
                {
                    "id": str(item.id),  # Return the file ID
                    "url": request.build_absolute_uri(getattr(item, file_field_name).url)  # Return the file URL
                }
                for item in field.all()
            ]
        return None

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
    
    def get_file_data(self, obj, field_name):
        # Get the related ManyToMany field (e.g., land_location_file, land_survey_number_file, etc.)
        field = getattr(obj, field_name, None)
        if field:
            request = self.context.get('request')
            # Here, directly access the correct file field (e.g., land_location_file for LandLocationAttachment)
            file_field_name = field_name  # Correctly reference the file field without adding '_file' at the end
            return [
                {
                    "id": str(item.id),  # Return the file ID
                    "url": request.build_absolute_uri(getattr(item, file_field_name).url)  # Return the file URL
                }
                for item in field.all()
            ]
        return None

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])

        return representation