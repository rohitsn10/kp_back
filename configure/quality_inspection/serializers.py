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