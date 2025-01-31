from django.db import models
from user_profile.models import *

class LandCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SFRAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    sfr_file = models.FileField(upload_to='land_sfr_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SFRforTransmissionLineGSSAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    sfr_for_transmission_line_gss_file = models.FileField(upload_to='sfr_for_transmission_line_gss_file', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class LandLocationAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_location_file = models.FileField(upload_to='land_location', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandSurveyNumbeAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_survey_number_file = models.FileField(upload_to='land_survey_number', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandKeyPlanAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_key_plan_file = models.FileField(upload_to='land_key_plan', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandAttachApprovalReportAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_attach_approval_report_file = models.FileField(upload_to='land_attach_approval_report', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandApproachRoadAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_approach_road_file = models.FileField(upload_to='land_approach_road', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandCoOrdinatesAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_co_ordinates_file = models.FileField(upload_to='land_co_ordinates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandProposedGssAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_proposed_gss_file = models.FileField(upload_to='land_proposed_gss', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandTransmissionLineAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_transmission_line_file = models.FileField(upload_to='land_transmission_line', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandApprovedReportAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved_report_file = models.FileField(upload_to='approved_report', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandBankMaster(models.Model):
    SOLAR_WIND_CHOICES = (
        ('Solar', 'Solar'),
        ('Wind', 'Wind'),
    )

    LAND_BANK_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_category = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    land_name = models.TextField()
    land_sfr_file = models.ManyToManyField(SFRAttachment)
    sfr_for_transmission_line_gss_file = models.ManyToManyField(SFRforTransmissionLineGSSAttachment)
    land_location_file = models.ManyToManyField(LandLocationAttachment)
    land_survey_number_file = models.ManyToManyField(LandSurveyNumbeAttachment)
    land_key_plan_file = models.ManyToManyField(LandKeyPlanAttachment)
    land_attach_approval_report_file = models.ManyToManyField(LandAttachApprovalReportAttachment)
    land_approach_road_file = models.ManyToManyField(LandApproachRoadAttachment)
    land_co_ordinates_file = models.ManyToManyField(LandCoOrdinatesAttachment)
    land_proposed_gss_file = models.ManyToManyField(LandProposedGssAttachment)
    land_transmission_line_file = models.ManyToManyField(LandTransmissionLineAttachment)
    solar_or_winds = models.CharField(max_length=10, choices=SOLAR_WIND_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    land_bank_status = models.CharField(max_length=255, choices=LAND_BANK_STATUS, null=True, blank=True, default='Pending')
    approved_report_file = models.ManyToManyField(LandApprovedReportAttachment)



class LandSFRAData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LandBankApproveAction(models.Model):
    approved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)

class LandBankRejectAction(models.Model):
    rejected_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    rejected_at = models.DateTimeField(auto_now_add=True)

class DILRAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dilr_file = models.FileField(upload_to='dilr', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NA_65B_Permission_Attachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    na_65b_permission_file = models.FileField(upload_to='na_65b_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Revenue_7_12_Records_Attachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    revenue_7_12_records_file = models.FileField(upload_to='revenue_7_12_records', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MunicipalCorporationPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    municipal_corporation_permission_file = models.FileField(upload_to='municipal_corporation_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TSRAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tsr_file = models.FileField(upload_to='tsr', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CoordinateVerificationAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coordinate_verification_file = models.FileField(upload_to='coordinate_verification', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EncumbranceNOCAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    encumbrance_noc_file = models.FileField(upload_to='encumbrance_noc', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DeveloperPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    developer_permission_file = models.FileField(upload_to='developer_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ListOfOtherApprovalsLandAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    list_of_other_approvals_land_file = models.FileField(upload_to='list_of_other_approvals_land', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromMinistryofDefenceAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    noc_from_ministry_of_defence_file = models.FileField(upload_to='noc_from_ministry_of_defence', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromAirportAuthorityOfIndiaAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    noc_from_airport_authority_of_india_file = models.FileField(upload_to='noc_from_airport_authority_of_india', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromForestAndAmpAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    noc_from_forest_and_amp_file = models.FileField(upload_to='noc_from_forest_and_amp', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NOCfromGeologyAndMiningOfficeAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    noc_from_geology_and_mining_office_file = models.FileField(upload_to='noc_from_geology_and_mining_office', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ApprovalsRequiredForTransmissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approvals_required_for_transmission_file = models.FileField(upload_to='approvals_required_for_transmission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CanalCrossingAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    canal_crossing_file = models.FileField(upload_to='canal_crossing', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LeaseDeedAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lease_deed_file = models.FileField(upload_to='lease_deed', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RailwayCrossingAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    railway_crossing_file = models.FileField(upload_to='railway_crossing', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyGasPipelineCrossingAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    any_gas_pipeline_crossing_file = models.FileField(upload_to='any_gas_pipeline_crossing', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoadCrossingPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    road_crossing_permission_file = models.FileField(upload_to='road_crossing_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyTransmissionLineCrossingPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    any_transmission_line_crossing_permission_file = models.FileField(upload_to='any_transmission_line_crossing_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnyTransmissionLineShiftingPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    any_transmission_line_shifting_permission_file = models.FileField(upload_to='any_transmission_line_shifting_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GramPanchayatPermissionAttachment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gram_panchayat_permission_file = models.FileField(upload_to='gram_panchayat_permission', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LandBankAfterApprovedData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE,null=True, blank=True)
    dilr_attachment_file = models.ManyToManyField(DILRAttachment)
    na_65b_permission_attachment_file = models.ManyToManyField(NA_65B_Permission_Attachment)
    revenue_7_12_records_attachment = models.ManyToManyField(Revenue_7_12_Records_Attachment)
    noc_from_forest_and_amp_attachment_file = models.ManyToManyField(NOCfromForestAndAmpAttachment)
    noc_from_geology_and_mining_office_attachment_file = models.ManyToManyField(NOCfromGeologyAndMiningOfficeAttachment)
    approvals_required_for_transmission_attachment_file = models.ManyToManyField(ApprovalsRequiredForTransmissionAttachment)
    canal_crossing_attachment_file = models.ManyToManyField(CanalCrossingAttachment)
    lease_deed_attachment_file = models.ManyToManyField(LeaseDeedAttachment)
    railway_crossing_attachment_file = models.ManyToManyField(RailwayCrossingAttachment)
    any_gas_pipeline_crossing_attachment_file = models.ManyToManyField(AnyGasPipelineCrossingAttachment)
    road_crossing_permission_attachment_file = models.ManyToManyField(RoadCrossingPermissionAttachment)
    any_transmission_line_crossing_permission_attachment_file = models.ManyToManyField(AnyTransmissionLineCrossingPermissionAttachment)
    any_transmission_line_shifting_permission_attachment_file = models.ManyToManyField(AnyTransmissionLineShiftingPermissionAttachment)
    gram_panchayat_permission_attachment_file = models.ManyToManyField(GramPanchayatPermissionAttachment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LandBankLocation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE)
    land_bank_location_name = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_land_area = models.CharField(null=True, blank=True)
    near_by_area = models.CharField(max_length=500,null=True, blank=True)

class LandSurveyNumber(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    land_bank = models.ForeignKey(LandBankMaster, on_delete=models.CASCADE,null=True, blank=True)
    location_name = models.ForeignKey(LandBankLocation, on_delete=models.CASCADE, related_name='land_survey_numbers', null=True, blank=True)
    land_survey_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)