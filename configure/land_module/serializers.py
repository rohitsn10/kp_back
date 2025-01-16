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
            'land_co_ordinates_file', 'land_proposed_gss_file', 'land_transmission_line_file'
        ]

    def get_land_location_file(self, obj):
        return self.get_file_urls(obj, 'land_location_file', 'land_location_file')

    def get_land_survey_number_file(self, obj):
        return self.get_file_urls(obj, 'land_survey_number_file', 'land_survey_number_file')

    def get_land_key_plan_file(self, obj):
        return self.get_file_urls(obj, 'land_key_plan_file', 'land_key_plan_file')

    def get_land_attach_approval_report_file(self, obj):
        return self.get_file_urls(obj, 'land_attach_approval_report_file', 'land_attach_approval_report_file')

    def get_land_approach_road_file(self, obj):
        return self.get_file_urls(obj, 'land_approach_road_file', 'land_approach_road_file')

    def get_land_co_ordinates_file(self, obj):
        return self.get_file_urls(obj, 'land_co_ordinates_file', 'land_co_ordinates_file')

    def get_land_proposed_gss_file(self, obj):
        return self.get_file_urls(obj, 'land_proposed_gss_file', 'land_proposed_gss_file')

    def get_land_transmission_line_file(self, obj):
        return self.get_file_urls(obj, 'land_transmission_line_file', 'land_transmission_line_file')

    def get_file_urls(self, obj, field_name, file_field):
        # Check if the attribute exists in the instance (obj) and if it's a ManyToManyField with related objects
        field = getattr(obj, field_name, None)
        if field:
            request = self.context.get('request')
            # Dynamically access the correct file field on the related objects
            return [request.build_absolute_uri(getattr(item, file_field).url) for item in field.all()]
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])

        return representation

