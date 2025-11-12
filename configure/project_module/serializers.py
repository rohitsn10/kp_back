from project_module.models import *
from rest_framework import serializers
from user_profile.function_call import *
from activity_module.serializers import *
from land_module.serializers import *
from django.conf import settings


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



class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Electricity
        fields = ['id', 'electricity_line', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    landbank_name = serializers.CharField(source='landbank.land_name', read_only=True)
    electricity_name = serializers.CharField(source='electricity_line.electricity_line', read_only=True)
    assigned_users = serializers.SerializerMethodField()
    land_location_name = serializers.CharField(source='location_name.land_bank_location_name', read_only=True)
    location_name_survey = LandBankLocationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'user', 'user_full_name', 'company', 'company_name', 'start_date', 'end_date', 'project_predicted_date',
            'cod_commission_date', 'total_area_of_project', 'capacity', 'project_name',
            'ci_or_utility', 'cpp_or_ipp', 'electricity_line', 'electricity_name', 'created_at',
            'available_land_area', 'alloted_land_area', 'landbank', 'landbank_name','assigned_users','location_name','land_location_name', 'location_name_survey'
        ]

    def get_assigned_users(self, obj):
        """Custom method to retrieve assigned users as a list of dicts"""
        assigned_users = obj.project_assigned_users.all()  # Ensure it's a QuerySet
        return [
            {
                'assigned_user_id': user.user.id,
                'assigned_user_name': user.user.full_name,
                'role': user.role
            }
            for user in assigned_users
        ] if assigned_users.exists() else []
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = int(representation['id'])  # Convert ID to int
        representation['user'] = int(representation['user'])  # Convert user ID to int
        representation['company'] = int(representation['company'])  # Convert company ID to int
        
        # Format assigned_users properly
        assigned_users = representation.pop('assigned_users', [])
        representation['assigned_users'] = [
            {
                'assigned_user_id': user['assigned_user_id'],
                'assigned_user_name': user['assigned_user_name'],
                'role': user['role']
            }
            for user in assigned_users if user
        ]
        return representation


class ClientDetailsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    msme_certificate_attachments = serializers.SerializerMethodField()
    adhar_card_attachments = serializers.SerializerMethodField()
    pan_card_attachments = serializers.SerializerMethodField()
    third_authority_adhar_card_attachments = serializers.SerializerMethodField()
    third_authority_pan_card_attachments = serializers.SerializerMethodField()

    class Meta:
        model = ClientDetails
        fields = ['id','user','user_full_name','project','project_name','client_name','contact_number','email','gst','pan_number',
                  'msme_certificate_attachments','adhar_card_attachments','pan_card_attachments','third_authority_adhar_card_attachments','third_authority_pan_card_attachments','captive_rec_nonrec_rpo',
                  'declaration_of_getco','undertaking_geda','authorization_to_epc','last_3_year_turn_over_details','factory_end','cin','moa_partnership',
                  'board_authority_signing','captive_rec_nonrec_rpo','is_client_created']
        

    def get_msme_certificate_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'msme_certificate_attachments')

    def get_adhar_card_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'adhar_card_attachments')
    
    def get_pan_card_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'pan_card_attachments')
    
    def get_third_authority_adhar_card_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'third_authority_adhar_card_attachments')
    
    def get_third_authority_pan_card_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'third_authority_pan_card_attachments')
    
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
        

class ProjectMilestoneSerializer(serializers.ModelSerializer):
    project_progress_details = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMilestone
        fields = [
            'id', 'project', 'start_date', 'end_date', 'project_progress_list',
            'project_progress_details', 'milestone_name', 'milestone_description',
            'completed_at', 'is_active', 'is_depended', 'milestone_status'
        ]

    def get_project_progress_details(self, obj):
        if obj.project_progress_list:
            progress_ids = obj.project_progress_list
            progress_objects = ProjectProgress.objects.filter(id__in=progress_ids)
            return ProjectProgressSerializer(progress_objects, many=True).data
        return []

class CommentedActionsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    drawing_and_design_name = serializers.CharField(source='drawing_and_design.name_of_drawing', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    class Meta:
        model = DrawingAndDesignCommentedActions
        fields = ['id','drawing_and_design','drawing_and_design_name','project','project_name','user','user_full_name','remarks', 'created_at', 'updated_at']

class ReSubmittedActionsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    drawing_and_design_name = serializers.CharField(source='drawing_and_design.name_of_drawing', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    class Meta:
        model = DrawingAndDesignReSubmittedActions
        fields = ['id','drawing_and_design','drawing_and_design_name','project','project_name','user','user_full_name','remarks','submitted_count','created_at', 'updated_at']

class ApprovedActionsSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    drawing_and_design_name = serializers.CharField(source='drawing_and_design.name_of_drawing', read_only=True)
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    class Meta:
        model = DrawingAndDesignApprovedActions
        fields = ['id','drawing_and_design','drawing_and_design_name','project','project_name','user','user_full_name','remarks', 'created_at', 'updated_at']   
class DrawingandDesignSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    drawing_and_design_attachments = serializers.SerializerMethodField()
    assign_to_user_full_name = serializers.CharField(source='assign_to_user.full_name', read_only=True)
    other_drawing_and_design_attachments = serializers.SerializerMethodField()
    # Nested serializers for the actions
    commented_actions = serializers.SerializerMethodField()
    resubmitted_actions = serializers.SerializerMethodField()
    approved_actions = serializers.SerializerMethodField()

    class Meta:
        model = DrawingAndDesignManagement
        fields = [
            'id', 'project', 'project_name', 'user', 'user_full_name','version_number',
            'drawing_and_design_attachments','other_drawing_and_design_attachments','assign_to_user', 'assign_to_user_full_name', 
            'discipline', 'block', 'drawing_number', 'auto_drawing_number', 'name_of_drawing', 
            'drawing_category', 'type_of_approval', 'approval_status', 'commented_count', 
            'submitted_count', 'is_approved', 'is_commented', 'is_submitted', 'updated_at',
            'commented_actions', 'resubmitted_actions', 'approved_actions',
        ]

    def get_drawing_and_design_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'drawing_and_design_attachments')

    def get_other_drawing_and_design_attachments(self, obj):
        return get_file_data(self.context.get('request'), obj, 'other_drawing_and_design_attachments')
    
    def get_commented_actions(self, obj):
        # Get related commented actions, or return an empty list if no related actions exist
        commented_actions = obj.drawinganddesigncommentedactions_set.all()
        if commented_actions.exists():
            return CommentedActionsSerializer(commented_actions, many=True, context=self.context).data
        return []

    # def get_resubmitted_actions(self, obj):
    #     # Get related resubmitted actions, or return an empty list if no related actions exist
    #     resubmitted_actions = DrawingAndDesignReSubmittedActions.objects.filter(drawing_and_design=obj)
    
    #     if resubmitted_actions.exists():
    #         data = []
    #         for action in resubmitted_actions:
    #             data.append({
    #                 "id": action.id,
    #                 "submitted_count": action.submitted_count,
    #                 "remarks": action.remarks,
    #                 "created_at": action.created_at,
    #                 "attachments": {
    #                     "drawing_and_design_attachments": get_file_data(self.context.get('request'), obj, 'drawing_and_design_attachments'),
    #                     "other_drawing_and_design_attachments": get_file_data(self.context.get('request'), obj, 'other_drawing_and_design_attachments')
    #                 }
    #             })
    #         return data
    #     return []
    

    def get_resubmitted_actions(self, obj):
        # Fetch all resubmitted actions related to this drawing and design object
        resubmitted_actions = DrawingAndDesignReSubmittedActions.objects.filter(drawing_and_design=obj)

        # Base URLs for constructing file URLs
        base_url = settings.MEDIA_URL.rstrip("/")
        site_url = getattr(settings, "SITE_URL", "").rstrip("/")

        # Prepare response structure
        response_data = []

        for action in resubmitted_actions:
            # Get the latest commented action that was created before or at the time of resubmission
            commented_action = DrawingAndDesignCommentedActions.objects.filter(
                drawing_and_design=obj,
                created_at__lte=action.created_at
            ).order_by('-created_at').first()

            # Fetch resubmission attachments
            drawing_attachments = [
                {
                    "id": str(attachment.id),
                    "url": f"{site_url}{base_url}/{attachment.drawing_and_design_resubmission_attachments.name}",
                    "created_at": attachment.created_at,
                    "updated_at": attachment.updated_at,
                }
                for attachment in action.drawing_and_design_attachments.all()
            ]

            # Fetch other resubmission attachments
            other_drawing_attachments = [
                {
                    "id": str(attachment.id),
                    "url": f"{site_url}{base_url}/{attachment.other_drawing_and_design_resubmission_attachments.name}",
                    "created_at": attachment.created_at,
                    "updated_at": attachment.updated_at,
                }
                for attachment in action.other_drawing_and_design_attachments.all()
            ]

            # Construct the response for each resubmitted action
            version_data = {
                "version_number": int(action.submitted_count) if action.submitted_count else None,
                "remarks": action.remarks,
                "created_at": action.created_at,
                "submitted_by": {
                    "id": action.user.id if action.user else None,
                    "name": action.user.full_name if action.user else None,
                },
                "documents": {
                    "drawing_and_design_attachments": drawing_attachments,
                    "other_drawing_and_design_attachments": other_drawing_attachments,
                } if drawing_attachments or other_drawing_attachments else {},  # Include only if attachments exist
                "commented_actions": {
                    "id": commented_action.id if commented_action else None,
                    "drawing_and_design": obj.id,
                    "drawing_and_design_name": obj.name_of_drawing,
                    "project": obj.project.id if obj.project else None,
                    "project_name": obj.project.project_name if obj.project else None,
                    "user": commented_action.user.id if commented_action and commented_action.user else None,
                    "user_full_name": commented_action.user.full_name if commented_action and commented_action.user else None,
                    "remarks": commented_action.remarks if commented_action else None,  
                    "created_at": commented_action.created_at if commented_action else None,
                    "updated_at": commented_action.updated_at if commented_action else None,
                },
            }

            response_data.append(version_data)

        return response_data

    def get_approved_actions(self, obj):
        # Get related approved actions, or return an empty list if no related actions exist
        approved_actions = obj.drawinganddesignapprovedactions_set.all()
        if approved_actions.exists():
            return ApprovedActionsSerializer(approved_actions, many=True, context=self.context).data
        return []
    
class InFlowPaymentOnMilestoneSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    milestone_name = serializers.CharField(source='milestone.milestone_name', read_only=True)
    class Meta:
        model = InFlowPaymentOnMilestone
        fields = ['id','project','project_name','milestone','milestone_name','party_name','invoice_number','total_amount','gst_amount','paid_amount','pending_amount','payment_date','notes','created_at','updated_at']
        
        
class ProjectIdWiseLandBankLocationSerializer(serializers.ModelSerializer):
    land_bank_location_name = serializers.CharField(source='location_name.land_bank_location_name', read_only=True)
    class Meta:
        model = Project
        fields = ['id','location_name','land_bank_location_name']


class ProjectProgressSerializer(serializers.ModelSerializer):
    from django.utils import timezone
  
    class Meta:
        model = ProjectProgress
        fields = [
            'id', 'particulars', 'status', 'category', 'uom',
            'qty', 'cumulative_completed',
            'scheduled_start_date', 'targeted_end_date',
            'actual_start_date', 'actual_completion_date','today_qty',
            'percent_completion', 'days_to_complete', 'remarks','days_to_deadline'
        ]
        extra_kwargs = {
            'status': {'required': False},
            'remarks': {'required': False}
        }

    def update(self, instance, validated_data):
        from django.utils import timezone
        
        # Get the changed_by from context (passed from the view)
        changed_by = self.context.get('changed_by')
        
        # Check if status is being changed to 'completed'
        new_status = validated_data.get('status')
        old_status = instance.status
        
        # Automatically set actual_completion_date when status changes to completed
        if new_status == 'completed' and old_status != 'completed':
            if not validated_data.get('actual_completion_date'):
                validated_data['actual_completion_date'] = timezone.now().date()  # Changed to .date()
        
        # Automatically set actual_start_date when status changes from pending to in_progress
        if new_status in ['in_progress', 'completed'] and old_status == 'pending':
            if not instance.actual_start_date and not validated_data.get('actual_start_date'):
                validated_data['actual_start_date'] = timezone.now().date()  # Changed to .date()
        
        # Update the instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Save with changed_by parameter
        instance.save(changed_by=changed_by)
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['days_to_complete'] = data.pop('days_to_complete')
        return data