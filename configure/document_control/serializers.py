from document_control.models import *
from rest_framework import serializers

class DocumentAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentManagementAttachments
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    document_attachments = DocumentAttachmentsSerializer(many=True, required=False)
    class Meta:
        model = DocumentManagement
        fields = ['id','documentname', 'documentnumber','project','revision_number','keywords','confidentiallevel','status','comments','document_attachments','created_by','created_at','updated_at', 'assign_users']