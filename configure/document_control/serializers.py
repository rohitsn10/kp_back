from document_control.models import *
from rest_framework import serializers
from user_profile.function_call import *

# class DocumentAttachmentsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocumentManagementAttachments
#         fields = ['id', 'document_management_attachments', 'created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    document_management_attachments = serializers.SerializerMethodField()
    class Meta:
        model = DocumentManagement
        fields = ['id','document_name', 'document_number','project','revision_number','keywords','confidentiallevel','status','comments','document_management_attachments','created_by','created_at','updated_at', 'assign_users']
    
    def get_document_management_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'document_management_attachments')