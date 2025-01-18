from project_module.models import *
from rest_framework import serializers
from user_profile.function_call import *


class ExpenseTrackingSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    expense_document_attachments = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseTracking
        fields = [
            'id', 'user', 'user_full_name', 'project', 'project_name',
            'expense_name', 'expense_amount', 'notes', 'expense_document_attachments'
        ]

    def get_expense_document_attachments(self, obj):
        return get_expense_project_attachments_file_data(self.context.get('request'), obj, 'expense_document_attachments')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        representation['project'] = str(representation['project'])

        return representation


    
class ProjectSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = Project
        fields = ['id','user','user_full_name','project_name']


class ClientDetailsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    msme_certificate = serializers.SerializerMethodField()
    adhar_card = serializers.SerializerMethodField()
    pan_card = serializers.SerializerMethodField()
    third_authority_adhar_card_attachments = serializers.SerializerMethodField()
    third_authortity_pan_card_attachments = serializers.SerializerMethodField()

    class Meta:
        model = ClientDetails
        fields = ['id','user','user_full_name','project','project_name','client_name','contact_number','email','gst','pan_number',
                  'msme_certificate','adhar_card','pan_card','third_authority_adhar_card_attachments','third_authortity_pan_card_attachments','captive_rec_nonrec_rpo',
                  'declaration_of_getco','undertaking_geda','authorization_to_epc','last_3_year_turn_over_details','factory_end','cin','moa_partnership',
                  'board_authority_signing','captive_rec_nonrec_rpo']
        

    def get_msme_certificate(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'msme_certificate_attachments')

    def get_adhar_card(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'adhar_card_attachments')
    
    def get_pan_card(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'pan_card_attachments')
    
    def get_third_authority_adhar_card_attachments(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'third_authority_adhar_card_attachments')
    
    def get_third_authortity_pan_card_attachments(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'third_authority_pan_card_attachments')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['user'] = str(representation['user'])
        representation['project'] = str(representation['project'])

        return representation
    

class Wo_PoSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    loi_attachments = serializers.SerializerMethodField()
    loa_po_attachments = serializers.SerializerMethodField()
    epc_contract = serializers.SerializerMethodField()
    omm_contact = serializers.SerializerMethodField()

    class Meta:
        model = WO_PO
        fields = ['id','project','project_name','user','user_full_name','loi_attachments','loa_po_attachments','epc_contract','omm_contact']

    def get_loi_attachments(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'loi_attachments')

    def get_loa_po_attachments(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'loa_po_attachments')
    
    def get_epc_contract(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'epc_contract_attachments')
    
    def get_omm_contact(self, obj):
        return get_client_details_file_data(self.context.get('request'), obj, 'omm_contact_attachments')
    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['user','company_name', 'id', 'created_at', 'updated_at']