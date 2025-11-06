from rest_framework import serializers
from .models import *
from hoto_module.models import Document

class DocumentsForHotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsForHoto
        fields = ['id', 'file', 'created_at', 'updated_at']

class PunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunchFile
        fields = ['id', 'file', 'created_at', 'updated_at']

class AcceptedRejectedPunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedRejectedPunchFile
        fields = ['id', 'file', 'created_at', 'file_status', 'updated_at']

class CompletedPunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedPunchFile
        fields = ['id', 'file', 'created_at','file_status', 'updated_at']


class VerifyPunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)

    class Meta:
        model = VerifyPunchPoints
        fields = [
            'id', 'verify_description', 'status',
            'created_by', 'created_by_name', 'created_at',
            'updated_by', 'updated_by_name', 'updated_at'
        ]


class AcceptedRejectedPunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    accepted_rejected_punch_files = AcceptedRejectedPunchFileSerializer(many=True, read_only=True)
    punch_file= PunchFileSerializer(many=True, read_only=True)
    class Meta:
        model = AcceptedRejectedPunchPoints
        fields = [
            'id', 'tentative_timeline', 'comments', 'status', 'punch_description','accepted_rejected_punch_files','punch_file',
            'created_by', 'created_by_name', 'created_at',
            'updated_by', 'updated_by_name', 'updated_at',
        ]
class CompletedPunchPointsSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_file = CompletedPunchFileSerializer(many=True, read_only=True)

    class Meta:
        model = CompletedPunchPoints
        fields = [
            'id', 'remarks', 'status', 'punch_file',
            'created_by', 'created_by_name', 'created_at',
            'updated_by', 'updated_by_name', 'updated_at'
        ]
class PunchPointsRaiseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_file = PunchFileSerializer(many=True, read_only=True)

    class Meta:
        model = PunchPointsRaise
        fields = [
            'id', 'project', 'punch_title', 'punch_description', 'status', 'is_verified', 'is_accepted', 'punch_file',
            'created_by', 'created_by_name', 'created_at',
            'updated_by', 'updated_by_name', 'updated_at',        ]
        


class HotoDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    documents = serializers.SerializerMethodField()
    document = DocumentsForHotoSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    project = serializers.IntegerField(source='project.id', read_only=True)
    
    class Meta:
        model = HotoDocument
        fields = [
            'id', 'project', 'documents',
            'category', 'remarks', 'status', 'verify_comment',
            'created_by', 'created_by_name', 'created_at', 'updated_by', 'updated_by_name', 'updated_at'
        ]

    def get_documents(self, obj):
        project_id = self.context.get('project_id')
        request = self.context.get('request')

        documents = obj.documents.all()
        doc_list = []
        for doc in documents:
            hoto_doc_exists = HotoDocument.objects.filter(
                document_name_id=doc.id, project_id=project_id
            ).first()

            doc_data = {
                'id': doc.id,
                'name': doc.name,
                'is_uploaded': hoto_doc_exists.is_uploaded if hoto_doc_exists else False,
                'is_verified': hoto_doc_exists.is_verified if hoto_doc_exists else False,
                'remarks': hoto_doc_exists.remarks if hoto_doc_exists else "",
                'file_ids': [],
                'files': []
            }

            if hoto_doc_exists and hoto_doc_exists.document.exists():
                doc_data['file_ids'] = [d.id for d in hoto_doc_exists.document.all()]
                doc_data['files'] = [
                    {
                        'id': d.id,
                        'file_url': request.build_absolute_uri(d.file.url)
                    } for d in hoto_doc_exists.document.all()
                ]

            doc_list.append(doc_data)

        return doc_list
    

