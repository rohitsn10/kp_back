from django.db import models
from land_module.models import *
from user_profile.models import *


class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    project_name = models.CharField(max_length=100)

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

    msme_certificate = models.ManyToManyField(MsMeCertificateAttachments)
    adhar_card = models.ManyToManyField(AdharCardAttachments)
    pan_card = models.ManyToManyField(PanCardAttachments)
    third_authority_adhar_card_attachments = models.ManyToManyField(ThirdAuthorityAdharCardAttachments)
    third_authortity_pan_card_attachments = models.ManyToManyField(ThirdAuthorityPanCardAttachments)
    
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





