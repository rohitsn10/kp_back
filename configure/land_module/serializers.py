from rest_framework import serializers
from land_module.models import *
from user_profile.models import *


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
    user_full_name = serializers.CharField(source='user.full_name',read_only=True)
    land_location_file = serializers.CharField(source='land_location_file.land_location_file',read_only=True)
    land_survey_number_file = serializers.CharField(source='land_survey_number_file.land_survey_number_file',read_only=True)
    land_key_plan_file = serializers.CharField(source='land_key_plan_file.land_key_plan_file',read_only=True)
    land_attach_approval_report_file = serializers.CharField(source='land_attach_approval_report_file.land_attach_approval_report_file',read_only=True)
    land_approach_road_file = serializers.CharField(source='land_approach_road_file.land_approach_road_file',read_only=True)
    land_co_ordinates_file = serializers.CharField(source='land_co_ordinates_file.land_co_ordinates_file',read_only=True)
    land_proposed_gss_file = serializers.CharField(source='land_proposed_gss_file.land_proposed_gss_file',read_only=True)
    land_transmission_line_file = serializers.CharField(source='land_transmission_line_file.land_transmission_line_file',read_only=True)
    class Meta:
        model = LandBankMaster
        fields = ['id','user','user_full_name','created_at','updated_at','land_location_file','land_survey_number_file','land_key_plan_file','land_attach_approval_report_file','land_approach_road_file','land_co_ordinates_file','land_proposed_gss_file','land_transmission_line_file']
    def get_land_location_file(self, obj):
        if obj.land_location_file and hasattr(obj.land_location_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_location_file.url)
        return None
    
    def get_land_survey_number_file(self, obj):
        if obj.land_survey_number_file and hasattr(obj.land_survey_number_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_survey_number_file.url)
        return None
    
    def get_land_key_plan_file(self, obj):
        if obj.land_key_plan_file and hasattr(obj.land_key_plan_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_key_plan_file.url)
        return None
    
    def get_land_attach_approval_report_file(self, obj):
        if obj.land_attach_approval_report_file and hasattr(obj.land_attach_approval_report_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_attach_approval_report_file.url)
        return None
    
    def get_land_approach_road_file(self, obj):
        if obj.land_approach_road_file and hasattr(obj.land_approach_road_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_approach_road_file.url)
        return None
    
    def get_land_co_ordinates_file(self, obj):
        if obj.land_co_ordinates_file and hasattr(obj.land_co_ordinates_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_co_ordinates_file.url)
        return None
    
    def get_land_proposed_gss_file(self, obj):
        if obj.land_proposed_gss_file and hasattr(obj.land_proposed_gss_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_proposed_gss_file.url)
        return None
    
    def get_land_transmission_line_file(self, obj):
        if obj.land_transmission_line_file and hasattr(obj.land_transmission_line_file, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.land_transmission_line_file.url)
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])