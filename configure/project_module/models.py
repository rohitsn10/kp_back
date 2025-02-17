from django.db import models
from land_module.models import *
from user_profile.models import *
from activity_module.models import *
from land_module.models import *

class Company(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="companies",verbose_name="User")
    company_name = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class Electricity(models.Model):
    electricity_line = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
class Project(models.Model):
    CI_UTILITY_CHOICES = [
        ('ci', 'CI'),
        ('utility', 'Utility'),
    ]

    CPP_IPP_CHOICES = [
        ('cpp', 'CPP'),
        ('ipp', 'IPP'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    landbank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE, related_name='landbank_data',null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_projects',null=True, blank=True)
    electricity_line = models.ForeignKey(Electricity, on_delete=models.CASCADE, related_name='electricity_line_name',null=True, blank=True)
    project_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    project_predicted_date = models.DateTimeField(null=True, blank=True)
    location_name = models.ForeignKey(LandBankLocation, on_delete=models.CASCADE, related_name='projects_location',null=True, blank=True)
    location_survey = models.ManyToManyField(LandSurveyNumber, related_name='projects_survey')
    cod_commission_date = models.DateTimeField(null=True, blank=True)
    total_area_of_project = models.TextField(null=True, blank=True)
    capacity = models.TextField(null=True, blank=True)
    ci_or_utility = models.CharField(max_length=10, choices=CI_UTILITY_CHOICES, null=True, blank=True)
    cpp_or_ipp = models.CharField(max_length=10, choices=CPP_IPP_CHOICES, null=True, blank=True)
    project_activity = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE, null=True, blank=True)
    project_sub_activity = models.ManyToManyField(SubActivityName)
    project_sub_sub_activity = models.ManyToManyField(SubSubActivityName)
    spoc_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='spoc_projects',blank=True,null=True)
    # project_predication_date = models.DateTimeField(null=True, blank=True)
    available_land_area = models.CharField(null=True, blank=True)
    alloted_land_area = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)


class ExpenseProjectAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    expense_project_attachments = models.FileField(upload_to='expense_project_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseTracking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    category = models.ForeignKey(LandCategory, on_delete=models.CASCADE,null=True, blank=True)
    expense_name = models.CharField(max_length=100,null=True, blank=True)
    expense_amount = models.CharField(max_length=100,null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    expense_document_attachments = models.ManyToManyField(ExpenseProjectAttachments)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MsMeCertificateAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    msme_certificate_attachments = models.FileField(upload_to='msme_certificate_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AdharCardAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    adhar_card_attachments = models.FileField(upload_to='adhar_card_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PanCardAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    pan_card_attachments = models.FileField(upload_to='pan_card_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ThirdAuthorityAdharCardAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    third_authority_adhar_card_attachments = models.FileField(upload_to='third_authority_adhar_card_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ThirdAuthorityPanCardAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    third_authority_pan_card_attachments = models.FileField(upload_to='third_authority_pan_card_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ClientDetails(models.Model):
    CAPTIVE_REC_NONREC_RPO_CHOICES = (
        ('Captive', 'Captive'),
        ('Rec', 'Rec'),
        ('Non-Rec', 'Non-Rec'),
        ('RPO', 'RPO'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    client_name = models.CharField(max_length=100,null=True, blank=True)
    contact_number = models.CharField(max_length=100,null=True, blank=True)
    email = models.CharField(max_length=100,null=True, blank=True)
    gst = models.CharField(max_length=100,null=True, blank=True)
    pan_number = models.CharField(max_length=100,null=True, blank=True)

    msme_certificate_attachments = models.ManyToManyField(MsMeCertificateAttachments)
    adhar_card_attachments = models.ManyToManyField(AdharCardAttachments)
    pan_card_attachments = models.ManyToManyField(PanCardAttachments)
    third_authority_adhar_card_attachments = models.ManyToManyField(ThirdAuthorityAdharCardAttachments)
    third_authority_pan_card_attachments = models.ManyToManyField(ThirdAuthorityPanCardAttachments)
    
    captive_rec_nonrec_rpo = models.CharField(max_length=100, choices=CAPTIVE_REC_NONREC_RPO_CHOICES, null=True, blank=True)
    declaration_of_getco = models.TextField(null=True, blank=True)
    undertaking_geda = models.TextField(null=True, blank=True)
    authorization_to_epc = models.TextField(null=True, blank=True)
    last_3_year_turn_over_details = models.TextField(null=True, blank=True)
    factory_end = models.CharField(max_length=100,null=True, blank=True)
    cin = models.CharField(max_length=100,null=True, blank=True)
    moa_partnership = models.CharField(max_length=100,null=True, blank=True)
    board_authority_signing = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_client_created = models.BooleanField(default=False, null=True, blank=True)


class LOIAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    loi_attachments = models.FileField(upload_to='loi_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Loa_PoAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    loa_po_attachments = models.FileField(upload_to='loa_po_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Epc_ContractAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    epc_contract_attachments = models.FileField(upload_to='epc_contract_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OMMContactAttachments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    omm_contact_attachments = models.FileField(upload_to='omm_contact_attachments',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WO_PO(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    loi_attachments = models.ManyToManyField(LOIAttachments)
    loa_po_attachments = models.ManyToManyField(Loa_PoAttachments)
    epc_contract_attachments = models.ManyToManyField(Epc_ContractAttachments)
    omm_contact_attachments = models.ManyToManyField(OMMContactAttachments)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ProjectMilestone(models.Model):
    MILESTONE_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'InProgress'),
        ('completed', 'Completed')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)
    project_main_activity = models.ForeignKey(ProjectActivity, on_delete=models.CASCADE,null=True, blank=True)
    project_sub_activity = models.ManyToManyField(SubActivityName, blank=True)
    project_sub_sub_activity = models.ManyToManyField(SubSubActivityName, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    milestone_name = models.TextField(null=True, blank=True)
    milestone_description = models.TextField(null=True, blank=True)
    milestone_status = models.CharField(default='pending',max_length=100, choices=MILESTONE_STATUS, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_depended = models.BooleanField(default=False, null=True, blank=True)





