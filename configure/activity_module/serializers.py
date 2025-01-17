from rest_framework import serializers
from user_profile.models import *
from activity_module.models import *

class ProjectMainActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectActivity
        fields = ['id','solar_or_wind','activity_name','created_at']

class SubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubActivity
        fields = ['id', 'name']

class SubActivityNameSerializer(serializers.ModelSerializer):
    sub_activity = SubActivitySerializer(many=True)

    class Meta:
        model = SubActivityName
        fields = ['id', 'sub_activity']
        
class SubsubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsubActivity
        fields = ['id', 'name']
        
class SubSubActivityNameSerializer(serializers.ModelSerializer):
    sub_sub_activity = SubActivitySerializer(many=True)

    class Meta:
        model = SubSubActivityName
        fields = ['id', 'sub_sub_activity']
