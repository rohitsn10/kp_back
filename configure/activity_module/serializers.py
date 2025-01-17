from rest_framework import serializers
from user_profile.models import *
from activity_module.models import *

class ProjectMainActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectActivity
        fields = ['id','solar_or_wind','activity_name','created_at']
