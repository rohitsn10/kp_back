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
    # Serialize the project_main_activity field normally
    project_main_activity = ProjectMainActivitySerializer()
    
    # Directly serialize the sub_activity data from the SubActivityName model
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
    sub_sub_activity = SubActivitySerializer(many=True)

    class Meta:
        model = SubSubActivityName
        fields = ['id', 'project_activity_id', 'sub_sub_activity']
