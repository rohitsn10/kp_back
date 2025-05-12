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
class PunchPointsRaiseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_file = PunchFileSerializer(many=True, read_only=True)
    class Meta:
        model = PunchPointsRaise
        fields = ['id', 'hoto', 'punch_title', 'punch_description', 'punch_point_raised', 'punch_point_balance', 'status', 'punch_file', 'closure_date',
                  'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']
        

class CompletedPunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedPunchFile
        fields = ['id', 'file', 'created_at', 'updated_at']

    
class CompletedPunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_file = CompletedPunchFileSerializer(many=True, read_only=True)
    verified = serializers.SerializerMethodField()
    class Meta:
        model = CompletedPunchPoints
        fields = ['id', 'raise_punch', 'punch_description', 'punch_point_completed', 'status', 'punch_file', 'verified',
                  'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']
        
    def get_verified(self, obj):
        try:
            verify_punch = VerifyPunchPoints.objects.get(completed_punch=obj)
            return VerifyPunchPointsSerializer(verify_punch).data
        except VerifyPunchPoints.DoesNotExist:
            return None
        
    
class VerifyPunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    class Meta:
        model = VerifyPunchPoints
        fields = ['id', 'completed_punch', 'verify_description', 'status', 'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']

