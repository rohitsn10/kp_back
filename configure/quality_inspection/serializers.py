from rest_framework import serializers
from .models import *
from project_module.models import Project

class ItemsProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemsProduct
        fields = ['id', 'project', 'item_number', 'item_name', 'item_category', 'dicipline', 'is_active', 'created_at', 'updated_at']

class VendorSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Vendor
        fields = ['id', 'project', 'items', 'vendor_name', 'created_at', 'updated_at']

class MQAPUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = MQAPUpload
        fields = ['id', 'file','mqap_revision_number', 'mqap_revision_status', 'created_at', 'updated_at']

class QualityDossierUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = QualityDossierUpload
        fields = ['id', 'file','quality_dossier_revision_number', 'quality_dossier_revision_status', 'created_at', 'updated_at']

class DrawingUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = DrawingUpload
        fields = ['id', 'file','drawing_revision_number', 'drawing_revision_status', 'created_at', 'updated_at']

class DataSheetUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = DataSheetUpload
        fields = ['id', 'file','data_sheet_revision_number', 'data_sheet_revision_status', 'created_at', 'updated_at']

class SpecificationUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = SpecificationUpload
        fields = ['id', 'file','specification_revision_number', 'specification_revision_status', 'created_at', 'updated_at']

class MDCCUploadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = MDCCUpload
        fields = ['id', 'file','mdcc_revision_number', 'mdcc_revision_status', 'created_at', 'updated_at']

class QualityInspectionSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = QualityInspection
        fields = ['id', 'project', 'items', 'vendor','cpp_ipp', 'is_venodr_verified', 'mqap_upload', 'quality_dossier_upload', 'drawing_upload', 'data_sheet_upload', 
                'specification_upload', 'mdcc_upload', 'inspection_status', 'inspection_date', 'remarks',
                'created_at', 'updated_at']
        

class ObservationReportDocumentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = ObservationReportDocument
        fields = ['id','file', 'created_at', 'updated_at']

class ObservationReportSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = ObservationReport
        fields = ['id', 'project','quality_inspection', 'items', 'vendor','observation_title', 'observation_status', 'observation_text_report', 'observation_report_document',
                'created_by','created_at', 'updated_at']
        

class RFIFieldActivitySerializer(serializers.ModelSerializer):
    inspection_outcomes = serializers.SerializerMethodField()
        
    class Meta:
        model = RFIFieldActivity
        fields = ['id', 'project', 'rfi_activity', 'rfi_number','rfi_classification', 'rfi_other', 'epc_name', 'offered_date', 'block_number', 
                'table_number', 'activity_description', 'hold_details', 'location_name', 'construction_activity','documents',
                'inspection_outcomes','created_at', 'updated_at']
        
    def get_inspection_outcomes(self, obj):
        outcomes = InspectionOutcome.objects.filter(rfi_field_activity=obj.id)
        return InspectionOutcomeSerializer(outcomes, many=True).data
        
class InspectionOutcomeSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = InspectionOutcome
        fields = ['id', 'project', 'rfi_field_activity','offered_time','reaching_time','inspection_start_time','inspection_end_time', 'observation', 
                  'disposition_status','actions','responsibility','timelines','remarks', 'created_at', 'updated_at']
        
class InspectionOutcomeDocumentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = InspectionOutcomeDocument
        fields = ['id','rfi', 'inspection_outcome','document', 'created_at', 'updated_at']