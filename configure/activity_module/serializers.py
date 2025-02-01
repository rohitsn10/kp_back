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

# class SubActivityNameSerializer(serializers.ModelSerializer):
#     project_main_activity = ProjectMainActivitySerializer()
#     sub_activity = SubActivitySerializer(many=True)

#     class Meta:
#         model = SubActivityName
#         fields = ['project_main_activity','sub_activity', 'created_at']

class SubActivityNameSerializer(serializers.ModelSerializer):
    project_main_activity = ProjectMainActivitySerializer()
    sub_activity = serializers.SerializerMethodField()

    class Meta:
        model = SubActivityName
        fields = ['project_main_activity', 'sub_activity', 'created_at']

    def get_sub_activity(self, obj):
        # Here you can return the relevant sub_activity data from the SubActivityName model
        return [
            {'id': sub.id, 'name': sub.name} 
            for sub in obj.sub_activity.all()
        ]

        
class SubsubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubsubActivity
        fields = ['id', 'name']
        
class SubSubActivityNameSerializer(serializers.ModelSerializer):
    sub_sub_activity_name = serializers.SerializerMethodField()

    class Meta:
        model = SubSubActivityName
        fields = ['id', 'project_activity_id', 'sub_sub_activity_name', 'created_at']  # Include created_at if needed

    def get_sub_sub_activity_name(self, obj):
        # Return a list of sub-sub activity names
        return [sub.name for sub in obj.sub_sub_activity.all()]


