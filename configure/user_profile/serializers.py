from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate

class GroupSerializer(serializers.ModelSerializer):
    # permission_list = serializers.SerializerMethodField()
    permission_list = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id','name','permission_list']   # add 'permissions' if you want to see the permissions in the group

    def get_permission_list(self, obj):
        # Filter permissions that are assigned to the group
        permissions = obj.permissions.all().select_related('content_type')
        grouped_permissions = {}
        for permission in permissions:
            content_type = permission.content_type.model
            if content_type not in grouped_permissions:
                grouped_permissions[content_type] = {}
            action = permission.codename.split('_')[0]
            grouped_permissions[content_type][action] = permission.id
        
        permission_list = [{model: perms} for model, perms in grouped_permissions.items()]
        return permission_list

class LoginUserSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'group_name', 'group_id']

    def get_group_name(self, obj):

        group = obj.groups.first() 
        return group.name if group else None

    def get_group_id(self, obj):

        group = obj.groups.first() 
        return str(group.id) if group else None
    
    def to_representation(self, instance):
        """Override to ensure all IDs are strings."""
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])  # Convert the `id` to a string
        return representation
