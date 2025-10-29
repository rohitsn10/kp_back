from rest_framework import serializers
from .models import *
from hoto_module.models import Document

class DocumentsForHotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsForHoto
        fields = ['id', 'file', 'created_at', 'updated_at']


class HotoDocumentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.full_name', read_only=True)
    document = DocumentsForHotoSerializer(many=True, read_only=True)
    uploaded_documents = serializers.SerializerMethodField()  # To include uploaded documents
    not_uploaded_documents = serializers.SerializerMethodField()  # To include not-uploaded documents
    punch_point_balance = serializers.SerializerMethodField()
    punch_status = serializers.SerializerMethodField()

    class Meta:
        model = HotoDocument
        fields = [
            'id', 'project', 'document', 'document_name', 'uploaded_documents', 'not_uploaded_documents',
            'punch_point_balance', 'punch_status', 'category', 'remarks', 'status', 'verify_comment',
            'created_by', 'created_by_name', 'created_at', 'updated_by', 'updated_by_name', 'updated_at'
        ]

    def get_uploaded_documents(self, obj):
        """
        Returns the list of uploaded documents for the HotoDocument.
        """
        uploaded_docs = obj.document.all()  # Fetch all linked documents
        return DocumentsForHotoSerializer(uploaded_docs, many=True).data

    def get_not_uploaded_documents(self, obj):
        """
        Returns the list of documents that are not uploaded for the HotoDocument.
        """
        # Fetch all documents for the category and project
        all_documents = Document.objects.filter(category=obj.category)
        uploaded_document_ids = obj.document.values_list('id', flat=True)

        # Filter documents that are not uploaded
        not_uploaded_docs = all_documents.exclude(id__in=uploaded_document_ids)
        return [{'id': doc.id, 'name': doc.name} for doc in not_uploaded_docs]

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



class DocumentStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_uploaded = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    remarks = serializers.CharField(allow_blank=True, allow_null=True)
    document = DocumentsForHotoSerializer(many=True, read_only=True)

class CategoryWithDocumentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category = serializers.CharField()
    documents = DocumentStatusSerializer(many=True)