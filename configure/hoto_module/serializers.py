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