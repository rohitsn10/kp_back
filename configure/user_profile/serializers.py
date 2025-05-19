from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken


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

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','department_name','created_at']

class LoginUserSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name','group_id','group_name','user_permissions', 'groups','department','assignments']

    def get_group_name(self, obj):

        group = obj.groups.first() 
        return group.name if group else None

    def get_group_id(self, obj):

        group = obj.groups.first() 
        return str(group.id) if group else None
    
    def get_user_permissions(self, obj):
        group = obj.groups.first()  # Get the user's first group (or however you determine the relevant group)
        if not group:
            return None

        permissions = group.permissions.select_related('content_type').all()

        permission_list = []
        for permission in permissions:
            permission_list.append({
                "id": permission.id,
                "name": permission.codename
            })

        return {
            "group": {
                "id": group.id,
                "name": group.name,
            },
            "permissions": permission_list if permission_list else None
        }
    
    def get_groups(self, obj):
        assignments = UserAssign.objects.filter(user=obj).select_related('group')
        return list({
            a.group.name
            for a in assignments
            if a.group  # Ensure group is not None
        })

    def get_department(self, obj):
        assignments = UserAssign.objects.filter(user=obj).select_related('department')
        return list({
            a.department.department_name
            for a in assignments
            if a.department
        })

    def get_assignments(self, obj):
        assignments = UserAssign.objects.filter(user=obj).select_related('project', 'department', 'group')
        return [
            {
                "project": a.project.project_name if a.project else None,
                "department": a.department.department_name if a.department else None,
                "group": a.group.name if a.group else None
            }
            for a in assignments
        ]
    
    def to_representation(self, instance):
        """Override to ensure all IDs are strings."""
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])  # Convert the `id` to a string
        return representation
    
class CustomUserSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','full_name','email','dob','profile_image','phone','address','is_staff','is_active','is_superuser','group_name', 'group_id','designation','department','department_name']

    def get_group_name(self, obj):

        group = obj.groups.first() 
        return group.name if group else None

    def get_group_id(self, obj):

        group = obj.groups.first() 
        return group.id if group else None
    
    def get_profile_image(self, obj):
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None

class UserUpdateOwnProfileDataSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    profile_image = serializers.SerializerMethodField() 
    class Meta:
        model = CustomUser
        fields = ['id','full_name','email','dob','profile_image','phone','address','is_staff','is_active','is_superuser','group_name', 'group_id','designation','department','department_name']

    def get_group_name(self, obj):

        group = obj.groups.first() 
        return group.name if group else None

    def get_group_id(self, obj):

        group = obj.groups.first() 
        return group.id if group else None
    
    def get_profile_image(self, obj):
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    
    def to_representation(self, instance):
        """Override to ensure all IDs are strings."""
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['group_id'] = str(representation['group_id'])
        representation['department'] = str(representation['department'])
        representation['is_staff'] = str(representation['is_staff']).lower()
        representation['is_active'] = str(representation['is_active']).lower()
        representation['is_superuser'] = str(representation['is_superuser']).lower()

        return representation

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['privacypolicy_data', 'privacypolicy_key', 'created_at']

class GetDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'created_at']


from project_module.serializers import *
from user_profile.serializers import *

class UserAssignSerializer(serializers.ModelSerializer):
    assignments = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.full_name', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = UserAssign
        fields = ['username', 'user', 'project_name', 'project', 'department_name', 'department', 'group_name', 'group', 'assignments', 'created_at', 'updated_at']
        
    def get_assignments(self, obj):
        assignments = UserAssign.objects.filter(user=obj.user).select_related('project', 'department', 'group')
        return [
            {
                "project": a.project.project_name if a.project else None,
                "department": a.department.department_name if a.department else None,
                "group": a.group.name if a.group else None
            }
            for a in assignments
        ]