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
class PunchPointsRaiseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    punch_file = PunchFileSerializer(many=True, read_only=True)
    punch_point_balance = serializers.SerializerMethodField()
    class Meta:
        model = PunchPointsRaise
        fields = ['id', 'hoto', 'punch_point_balance', 'punch_title', 'punch_description', 'punch_point_raised', 'punch_point_balance', 'status', 'punch_file', 'closure_date',
                  'created_by','created_by_name', 'created_at', 'updated_by','updated_by_name', 'updated_at']
        
    def get_punch_point_balance(self, obj):
        def safe_int(val):
            try:
                return int(val)
            except (ValueError, TypeError):
                return 0

        try:
            # Use the direct value from the object
            total_punch_points = safe_int(obj.punch_point_raised)

            # Get Verified Completed Punches for this PunchPointsRaise
            verified_completed_ids = VerifyPunchPoints.objects.filter(
                completed_punch__raise_punch=obj,
                status='Completed'
            ).values_list('completed_punch_id', flat=True).distinct()

            completed_punch_points = CompletedPunchPoints.objects.filter(
                id__in=verified_completed_ids,
                raise_punch=obj
            )

            total_completed_points = sum(safe_int(p.punch_point_completed) for p in completed_punch_points)

            return total_punch_points - total_completed_points
        except Exception:
            return 0
        

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



class HotoDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    documents = serializers.SerializerMethodField()
    document = DocumentsForHotoSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    project = serializers.IntegerField(source='project.id', read_only=True)

    punch_point_balance = serializers.SerializerMethodField()
    punch_status = serializers.SerializerMethodField()

    class Meta:
        model = HotoDocument
        fields = [
            'id', 'project', 'documents',
            'punch_point_balance', 'punch_status', 'category', 'remarks', 'status', 'verify_comment',
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
    
    def get_punch_point_balance(self, obj):
        try:
            raised_punch_points = PunchPointsRaise.objects.filter(hoto=obj)
            verified_completed_ids = VerifyPunchPoints.objects.filter(completed_punch__raise_punch__hoto=obj,status='Completed').values_list('completed_punch_id', flat=True).distinct()
            completed_punch_points = CompletedPunchPoints.objects.filter(id__in=verified_completed_ids)
            total_punch_points = sum(int(p.punch_point_raised or 0) for p in raised_punch_points)
            total_completed_points = sum(int(p.punch_point_completed or 0) for p in completed_punch_points)
            return total_punch_points - total_completed_points
        except Exception as e:
            return 0
        
    def get_punch_status(self, obj):
        try:
            raised_punch_points = PunchPointsRaise.objects.filter(hoto=obj)
            completed_punch_points = CompletedPunchPoints.objects.filter(raise_punch__hoto=obj)
            total_punch_points = sum(int(p.punch_point_raised or 0) for p in raised_punch_points)
            total_completed_points = sum(int(p.punch_point_completed or 0) for p in completed_punch_points)
            if total_completed_points == 0 or None:
                return "Pending"
            elif total_completed_points < total_punch_points:
                return "In Progress"
            elif total_completed_points == total_punch_points:
                return "Completed"
            else:
                return "Unknown"
        except Exception as e:
            return "Unknown"