from rest_framework import serializers
from .models import *
from project_module.models import Project
from user_profile.models import CustomUser

class DocumentsForHotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsForHoto
        fields = ['id', 'file', 'created_at', 'updated_at']

class HotoDocumentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    document = DocumentsForHotoSerializer(many=True, read_only=True)
    class Meta:
        model = HotoDocument
        fields = ['id', 'project', 'document', 'document_name', 'category', 'remarks', 'status', 'verify_comment',
                  'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']
        
    
class PunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunchFile
        fields = ['id', 'file', 'created_at', 'updated_at']
class PunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_point_balance = serializers.SerializerMethodField()
    punch_file = PunchFileSerializer(many=True, read_only=True)
    class Meta:
        model = PunchPoints
        fields = ['id', 'hoto', 'punch_title', 'punch_description', 'punch_point_raised', 'punch_point_completed', 'punch_point_balance', 'status', 'punch_file',
                  'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']
        
    def get_punch_point_balance(self, obj):
        try:
            return int(obj.punch_point_raised or 0) - int(obj.punch_point_completed or 0)
        except (ValueError, TypeError):
            return None
