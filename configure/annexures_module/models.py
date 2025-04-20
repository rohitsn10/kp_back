from django.db import models
from user_profile.models import *
from land_module.models import *

class PermitToWork(models.Model):
    DEPARTMENT_CHOICES = (
        ('onm', 'ONM'),
        ('project', 'Project'),
    )
    PERMIT_CHOICES = (
        ('cold work', 'Cold Work'),
        ('hot work', 'Hot Work'),
        ('work at height', 'Work at Height'),
        ('electrical work', 'Electrical Work'),
        ('excavation', 'Excavation'),
        ('equipment testing', 'Equipment Testing'),
        ('crane/hydra/jcb work', 'Crane/Hydra/Jcb Work'),
        ('other', 'Other')
    )
    PERMIT_ISSUED_CHOICES = (
    ('day', 'Day'),
    ('night', 'Night'),
    )

    HAZARD_CHOICES = (
        ('fire', 'Fire'),
        ('electrical', 'Electrical'),
        ('fall', 'Fall'),
        ('slip & trip', 'Slip & Trip'),
        ('cut & injury', 'Cut & Injury'),
        ('toppling', 'Toppling'),
        ('dust', 'Dust'),
        ('other', 'Other'),
    )

    FIRE_PROTECTION_CHOICES = (
        ('fire extinguisher', 'Fire Extinguisher'),
        ('fire blanket', 'Fire Blanket'),
        ('face shield', 'Face Shield'),
        ('dust mask', 'Dust Mask'),
        ('full body harness', 'Full Body Harness'),
        ('other', 'Other'),
    )
    JOB_PREPARATIONS_CHOICES = (
        ('risk assessment', 'Risk Assessment'),
        ('safe operating procedure', 'Safe Operating Procedure'),
        ('work permit procedure', 'Work permit Procedure'),
        ('other', 'Other'),
    )
    RISK_CHOICES = (
        ('critical', 'Critical'),
        ('general', 'General'),
    )
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=25, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    permit_number = models.CharField(max_length=255, blank=True, null=True)
    permit_date = models.DateTimeField(max_length=255, blank=True, null=True)
    name_of_external_agency = models.CharField(max_length=255, blank=True, null=True)
    type_of_permit = models.CharField(max_length=255, choices=PERMIT_CHOICES, blank=True, null=True)
    permit_valid_from = models.TimeField(max_length=255, blank=True, null=True)
    permit_valid_to = models.TimeField(max_length=255, blank=True, null=True)
    permit_risk_type = models.CharField(max_length=255, choices=RISK_CHOICES, blank=True, null=True)
    other_permit_description = models.CharField(max_length=255, blank=True, null=True)
    job_activity_details = models.CharField(max_length=255, blank=True, null=True)
    location_area = models.CharField(max_length=255, blank=True, null=True)
    tools_equipment = models.CharField(max_length=255, blank=True, null=True)
    hazard_consideration = models.CharField(max_length=255, choices=HAZARD_CHOICES, blank=True, null=True)
    other_hazard_consideration = models.CharField(max_length=255, blank=True, null=True)
    fire_protection = models.CharField(max_length=255, choices=FIRE_PROTECTION_CHOICES, blank=True, null=True)
    other_fire_protection = models.CharField(max_length=255, blank=True, null=True)
    permit_issue_for = models.CharField(max_length=255, choices=PERMIT_ISSUED_CHOICES, blank=True, null=True)
    day = models.CharField(max_length=255, blank=True, null=True)
    night = models.CharField(max_length=255, blank=True, null=True)
    job_preparation = models.CharField(max_length=255, choices=JOB_PREPARATIONS_CHOICES, blank=True, null=True)
    other_job_preparation = models.CharField(max_length=255, blank=True, null=True)
    risk_assessment_number = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    issuer_name = models.CharField(max_length=255, blank=True, null=True)
    issuer_sign = models.FileField(upload_to='permitwork/', null=True, blank=True)
    issuer_done = models.BooleanField(default=False, null=True, blank=True)
    approver_done = models.BooleanField(default=False, null=True, blank=True)
    receiver_done = models.BooleanField(default=False, null=True, blank=True)
    closure_done = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ClosureOfPermit(models.Model):
    CLOSURE_APPLICABLE_CHOICES = (
        ('where applicable', 'Where Applicable'),
        ('where not applicable', 'Where Not Applicable'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    closer_of_permit = models.CharField(max_length=255, choices=CLOSURE_APPLICABLE_CHOICES, null=True, blank=True)
    inspector_name = models.CharField(max_length=255, blank=True, null=True)
    closure_sign = models.FileField(upload_to='permitwork/', null=True, blank=True)
    closure_remarks = models.TextField(blank=True,null=True)
    closure_time = models.TimeField(max_length=255, blank=True, null=True)
    permit = models.ForeignKey(PermitToWork, related_name='closure_of_permit', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class IssueApprovePermit(models.Model):
    permit = models.ForeignKey(PermitToWork,related_name='permitforissue', on_delete=models.SET_NULL, null=True, blank=True)
    issuer_name = models.CharField(max_length=255, blank=True, null=True)
    issuer_sign = models.FileField(upload_to='permitwork/', null=True, blank=True)
    # approver = models.ForeignKey(CustomUser,related_name='approver', on_delete=models.SET_NULL, null=True, blank=True)
    # receiver = models.ForeignKey(CustomUser,related_name='receiver', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(max_length=255, blank=True, null=True)
    end_time = models.DateTimeField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ApproverApprovePermit(models.Model):
    permit = models.ForeignKey(PermitToWork,related_name='permitforapprove', on_delete=models.SET_NULL, null=True, blank=True)
    approver_name = models.CharField(max_length=255, blank=True, null=True)
    approver_sign = models.FileField(upload_to='permitwork/', null=True, blank=True)
    approver_status = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(max_length=255, blank=True, null=True)
    end_time = models.DateTimeField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ReceiverApprovePermit(models.Model):
    permit = models.ForeignKey(PermitToWork,related_name='permitforrecive', on_delete=models.SET_NULL, null=True, blank=True)
    receiver_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_sign = models.FileField(upload_to='permitwork/', null=True, blank=True)
    start_time = models.DateTimeField(max_length=255, blank=True, null=True)
    end_time = models.DateTimeField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IncidentNearMiss(models.Model):
    STATUS_CHOICES = (
        ('under review', 'Under Review'),
        ('reviewed', 'Reviewed'),
        ('under approval', 'Under Approval'),
        ('approved', 'Approved'),
    )
    CATEGORY_CHOICES = (
        ('incident', 'Incident'),
        ('nearmiss', 'Nearmiss'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    # location = models.CharField(max_length=255, blank=True, null=True)
    date_of_occurrence = models.DateTimeField(max_length=255, blank=True, null=True)
    date_of_report = models.DateTimeField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)
    title_incident_nearmiss = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    investigation_findings = models.TextField(blank=True, null=True)
    physical_factor = models.TextField(blank=True, null=True)
    human_factor = models.TextField(blank=True, null=True)
    system_factor = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=True, blank=True)
    recommendation_for_preventive_action = models.JSONField(default=dict)
    committee_members = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewIncidentNearMiss(models.Model):
    incident_nearmiss = models.ForeignKey(IncidentNearMiss, related_name='review_incident_nearmiss', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(CustomUser, related_name='reviewers', on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ApproveIncidentNearMiss(models.Model):
    incident_nearmiss = models.ForeignKey(IncidentNearMiss, related_name='approve_incident_nearmiss', on_delete=models.SET_NULL, null=True, blank=True)
    approver = models.ForeignKey(CustomUser, related_name='approvers', on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ReportOfIncidentNearmiss(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_occurrence = models.DateTimeField(max_length=255, blank=True, null=True)
    date_of_report = models.DateTimeField(max_length=255, blank=True, null=True)
    reported_by = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    employee_code = models.CharField(max_length=255, blank=True, null=True)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    immediate_action_taken = models.CharField(max_length=255, null=True, blank=True)
    apparent_cause = models.CharField(max_length=255, null=True, blank=True)
    preventive_action = models.CharField(max_length=255, null=True, blank=True)
    member_1 = models.CharField(max_length=255, blank=True, null=True)
    member_2 = models.CharField(max_length=255, blank=True, null=True)
    member_3 = models.CharField(max_length=255, blank=True, null=True)
    member_1_sign = models.FileField(upload_to='incidentnearmiss/', null=True, blank=True)
    member_2_sign = models.FileField(upload_to='incidentnearmiss/', null=True, blank=True)
    member_3_sign = models.FileField(upload_to='incidentnearmiss/', null=True, blank=True)
    site_incharge_name = models.CharField(max_length=255, blank=True, null=True)
    site_incharge_designation = models.CharField(max_length=255, blank=True, null=True)
    site_incharge_sign = models.FileField(upload_to='incidentnearmiss/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SafetyViolationReportAgainstUnsafeACT(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    issued_to = models.CharField(max_length=255, blank=True, null=True)
    issued_to_violator_name = models.CharField(max_length=255, blank=True, null=True)
    issued_to_designation = models.CharField(max_length=255, blank=True, null=True)
    issued_to_department = models.CharField(max_length=255, blank=True, null=True)
    issued_to_sign = models.FileField(upload_to='safetyviolation/', null=True, blank=True)
    issued_by = models.CharField(max_length=255, blank=True, null=True)
    issued_by_name = models.CharField(max_length=255, blank=True, null=True)
    issued_by_designation = models.CharField(max_length=255, blank=True, null=True)
    issued_by_department = models.CharField(max_length=255, blank=True, null=True)
    issued_by_sign = models.FileField(upload_to='safetyviolation/', null=True, blank=True)
    contractors_name = models.CharField(max_length=255, blank=True, null=True)
    description_safety_violation = models.TextField(max_length=255, blank=True, null=True)
    action_taken = models.CharField(max_length=255, blank=True, null=True)
    hseo_name = models.CharField(max_length=255, blank=True, null=True)
    hseo_sign = models.FileField(upload_to='safetyviolation/', null=True, blank=True)
    site_incharge_name = models.CharField(max_length=255, blank=True, null=True)
    site_incharge_sign = models.FileField(upload_to='safetyviolation/', null=True, blank=True)
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    manager_sign = models.FileField(upload_to='safetyviolation/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BoomLiftInspection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    equipment_name = models.CharField(max_length=255, blank=True, null=True)
    make_model = models.CharField(max_length=255, blank=True, null=True)
    identification_number = models.CharField(max_length=255, blank=True, null=True)
    inspection_date = models.DateTimeField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    # location = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_observations = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_action_by = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_remarks = models.CharField(max_length=255, blank=True, null=True)
    operator_fitness_certificate_observations = models.CharField(max_length=255, blank=True, null=True)
    operator_fitness_certificate_action_by = models.CharField(max_length=255, blank=True, null=True)
    operator_fitness_certificate_remarks = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_observations = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_action_by = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_remarks = models.CharField(max_length=255, blank=True, null=True)
    emergency_lowering_observations = models.CharField(max_length=255, blank=True, null=True)
    emergency_lowering_action_by = models.CharField(max_length=255, blank=True, null=True)
    emergency_lowering_remarks = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_remarks = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_observations = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_action_by = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_remarks = models.CharField(max_length=255, blank=True, null=True)
    smooth_function_observations = models.CharField(max_length=255, blank=True, null=True)
    smooth_function_action_by = models.CharField(max_length=255, blank=True, null=True)
    smooth_function_remarks = models.CharField(max_length=255, blank=True, null=True)
    brake_stop_hold_observations = models.CharField(max_length=255, blank=True, null=True)
    brake_stop_hold_action_by = models.CharField(max_length=255, blank=True, null=True)
    brake_stop_hold_remarks = models.CharField(max_length=255, blank=True, null=True)
    condition_of_all_observations = models.CharField(max_length=255, blank=True, null=True)
    condition_of_all_action_by = models.CharField(max_length=255, blank=True, null=True)
    condition_of_all_remarks = models.CharField(max_length=255, blank=True, null=True)
    guard_rails_without_damage_observations = models.CharField(max_length=255, blank=True, null=True)
    guard_rails_without_damage_action_by = models.CharField(max_length=255, blank=True, null=True)
    guard_rails_without_damage_remarks = models.CharField(max_length=255, blank=True, null=True)
    toe_guard_observations = models.CharField(max_length=255, blank=True, null=True)
    toe_guard_action_by = models.CharField(max_length=255, blank=True, null=True)
    toe_guard_remarks = models.CharField(max_length=255, blank=True, null=True)
    platform_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    platform_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    platform_condition_remarks = models.CharField(max_length=255, blank=True, null=True)
    door_lock_platform_observations = models.CharField(max_length=255, blank=True, null=True)
    door_lock_platform_action_by = models.CharField(max_length=255, blank=True, null=True)
    door_lock_platform_remarks = models.CharField(max_length=255, blank=True, null=True)
    swl_observations = models.CharField(max_length=255, blank=True, null=True)
    swl_action_by = models.CharField(max_length=255, blank=True, null=True)
    swl_remarks = models.CharField(max_length=255, blank=True, null=True)
    over_load_indicator_cut_off_devices_observations = models.CharField(max_length=255, blank=True, null=True)
    over_load_indicator_cut_off_devices_action_by = models.CharField(max_length=255, blank=True, null=True)
    over_load_indicator_cut_off_devices_remarks = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_remarks = models.CharField(max_length=255, blank=True, null=True)
    operator_list_observations = models.CharField(max_length=255, blank=True, null=True)
    operator_list_action_by = models.CharField(max_length=255, blank=True, null=True)
    operator_list_remarks = models.CharField(max_length=255, blank=True, null=True)
    ppe_observations = models.CharField(max_length=255, blank=True, null=True)
    ppe_action_by = models.CharField(max_length=255, blank=True, null=True)
    ppe_remarks = models.CharField(max_length=255, blank=True, null=True)
    inspected_name = models.CharField(max_length=255, blank=True, null=True)
    inspected_sign = models.FileField(upload_to='boomlift/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class CraneHydraInspections(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    equipment_name = models.CharField(max_length=255, blank=True, null=True)
    make_model = models.CharField(max_length=255, blank=True, null=True)
    identification_number = models.CharField(max_length=255, blank=True, null=True)
    inspection_date = models.DateTimeField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    # location = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_observations = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_action_by = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_remarks = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_observations = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_action_by = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_remarks = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_observations = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_action_by = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_remarks = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_observations = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_action_by = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_remarks = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_remarks = models.CharField(max_length=255, blank=True, null=True)    
    head_light_indicator_observations = models.CharField(max_length=255, blank=True, null=True)
    head_light_indicator_action_by = models.CharField(max_length=255, blank=True, null=True)
    head_light_indicator_remarks = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_observations = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_action_by = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_remarks = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_observations = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_action_by = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_remarks = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_observations = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_action_by = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_remarks = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_observations = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_action_by = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_remarks = models.CharField(max_length=255, blank=True, null=True)
    door_lock_observations = models.CharField(max_length=255, blank=True, null=True)
    door_lock_action_by = models.CharField(max_length=255, blank=True, null=True)
    door_lock_remarks = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_remarks = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_observations = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_action_by = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_remarks = models.CharField(max_length=255, blank=True, null=True)
    swl_on_boom_lift_observations = models.CharField(max_length=255, blank=True, null=True)
    swl_on_boom_lift_action_by = models.CharField(max_length=255, blank=True, null=True)
    swl_on_boom_lift_remarks = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_observations = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_action_by = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_remarks = models.CharField(max_length=255, blank=True, null=True)
    speedometere_observations = models.CharField(max_length=255, blank=True, null=True)
    speedometere_action_by = models.CharField(max_length=255, blank=True, null=True)
    speedometere_remarks = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_observations = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_action_by = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_remarks = models.CharField(max_length=255, blank=True, null=True)
    ppe_observations = models.CharField(max_length=255, blank=True, null=True)
    ppe_action_by = models.CharField(max_length=255, blank=True, null=True)
    ppe_remarks = models.CharField(max_length=255, blank=True, null=True)
    inspected_name = models.CharField(max_length=255, blank=True, null=True)
    inspected_sign = models.FileField(upload_to='cranehydra/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TrailerInspectionChecklist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    equipment_name = models.CharField(max_length=255, blank=True, null=True)
    make_model = models.CharField(max_length=255, blank=True, null=True)
    identification_number = models.CharField(max_length=255, blank=True, null=True)
    inspection_date = models.DateTimeField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    # location = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_observations = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_action_by = models.CharField(max_length=255, blank=True, null=True)
    all_valid_document_remarks = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_observations = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_action_by = models.CharField(max_length=255, blank=True, null=True)
    driver_fitness_certificate_remarks = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_observations = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_action_by = models.CharField(max_length=255, blank=True, null=True)
    main_horn_reverse_horn_remarks = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_observations = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_action_by = models.CharField(max_length=255, blank=True, null=True)
    cutch_brake_remarks = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    tyre_pressure_condition_remarks = models.CharField(max_length=255, blank=True, null=True)    
    head_light_indicator_observations = models.CharField(max_length=255, blank=True, null=True)
    head_light_indicator_action_by = models.CharField(max_length=255, blank=True, null=True)
    head_light_indicator_remarks = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_observations = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_action_by = models.CharField(max_length=255, blank=True, null=True)
    seat_belt_remarks = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_observations = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_action_by = models.CharField(max_length=255, blank=True, null=True)
    wiper_blade_remarks = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_observations = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_action_by = models.CharField(max_length=255, blank=True, null=True)
    side_mirror_remarks = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_observations = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_action_by = models.CharField(max_length=255, blank=True, null=True)
    wind_screen_remarks = models.CharField(max_length=255, blank=True, null=True)
    door_lock_observations = models.CharField(max_length=255, blank=True, null=True)
    door_lock_action_by = models.CharField(max_length=255, blank=True, null=True)
    door_lock_remarks = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_observations = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_action_by = models.CharField(max_length=255, blank=True, null=True)
    battery_condition_remarks = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_observations = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_action_by = models.CharField(max_length=255, blank=True, null=True)
    hand_brake_remarks = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_observations = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_action_by = models.CharField(max_length=255, blank=True, null=True)
    any_leakage_remarks = models.CharField(max_length=255, blank=True, null=True)
    speedometere_observations = models.CharField(max_length=255, blank=True, null=True)
    speedometere_action_by = models.CharField(max_length=255, blank=True, null=True)
    speedometere_remarks = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_observations = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_action_by = models.CharField(max_length=255, blank=True, null=True)
    guard_parts_remarks = models.CharField(max_length=255, blank=True, null=True)
    ppe_observations = models.CharField(max_length=255, blank=True, null=True)
    ppe_action_by = models.CharField(max_length=255, blank=True, null=True)
    ppe_remarks = models.CharField(max_length=255, blank=True, null=True)
    inspected_name = models.CharField(max_length=255, blank=True, null=True)
    inspected_sign = models.FileField(upload_to='trailerinspection/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MockDrillReport(models.Model):
    TYPE_MOCK_DRILL = (
        ('table top drill', 'Table Top Drill'),
        ('physical practice drill', 'Physical Practice Drill'),
    )
    TEAM_LEADER_CHOICES = (
        ('team leader', 'Team Leader'),
        ('incident controller', 'Incident Controller'),
    )
    PERFORMANCE_CHOICES = (
        ('o&m', 'O&M'),
        ('control', 'Control')
    )
    TRAFFIC_CHOICES = (
        ('traffic', 'Traffic'),
        ('evacuation', 'Evacuation'),
        ('assembly point & head count', 'Assembly Point & Head Count'),
    )
    AMBULANCE_CHOICES = (
        ('ambulance', 'Ambulance'),
        ('first aid', 'First Aid'),
        ('ppe', 'Ppe'),
        ('rescue', 'Rescue'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    site_plant_name = models.CharField(max_length=255, blank=True,null=True)
    emergncy_scenario_mock_drill = models.CharField(max_length=255, blank=True, null=True)
    type_of_mock_drill = models.CharField(max_length=255, choices=TYPE_MOCK_DRILL, blank=True, null=True)
    mock_drill_date = models.DateField(max_length=255, blank=True, null=True)
    mock_drill_time = models.TimeField(max_length=255, blank=True, null=True)
    completed_time = models.TimeField(max_length=255, blank=True, null=True)
    overall_time = models.TimeField(max_length=255, blank=True, null=True)
    
    drill_details = models.JSONField(default=dict, blank=True, null=True)
    team_members = models.JSONField(max_length=255, blank=True, null=True)
    
    table_top_records = models.JSONField(default=dict)
    description_of_control = models.CharField(max_length=255, blank=True, null=True)
    head_count_at_assembly_point = models.JSONField(default=dict)
    rating_of_emergency_team_members = models.JSONField(default=dict)
    overall_rating = models.CharField(max_length=255, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    recommendations = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class MinutesSafetyTraining(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    mom_recorded_by = models.CharField(max_length=255, blank=True, null=True)
    mom_issue_date = models.DateTimeField(max_length=255, blank=True, null=True)
    chairman_name = models.CharField(max_length=255, blank=True, null=True)
    hse_performance_data = models.JSONField(default=dict, blank=True, null=True)
    incident_investigation = models.JSONField(default=dict, blank=True, null=True)
    safety_training = models.JSONField(default=dict, blank=True, null=True)
    internal_audit = models.JSONField(default=dict, blank=True, null=True)
    mock_drill = models.JSONField(default=dict, blank=True, null=True)
    procedure_checklist_update = models.JSONField(default=dict, blank=True, null=True)
    review_last_meeting = models.JSONField(default=dict, blank=True, null=True)
    new_points_discussed = models.JSONField(default=dict, blank=True, null=True)
    minutes_prepared_by = models.CharField(max_length=255, blank=True, null=True)
    signature_prepared_by = models.FileField(upload_to='signatures/minutes/', null=True, blank=True)
    signature_chairman = models.FileField(upload_to='signatures/minutes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class SafetyTrainingAttendance(models.Model):
    site_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    training_topic = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    faculty_name = models.CharField(max_length=255, null=True, blank=True)
    faculty_signature = models.FileField(upload_to='signatures/faculty/', null=True, blank=True)
    file_upload = models.FileField(upload_to='safety_training_attendance/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Participant(models.Model):
    training = models.ForeignKey(SafetyTrainingAttendance, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    signature = models.FileField(upload_to='signatures/participants/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"
    

class InternalAuditReport(models.Model):
    site_name = models.CharField(max_length=255)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    observer_details = models.CharField(max_length=255, null=True, blank=True)
    observer_name = models.CharField(max_length=255, null=True, blank=True)
    observer_sign = models.FileField(upload_to='signatures/observer/', null=True, blank=True)
    auditee_name = models.CharField(max_length=255, null=True, blank=True)
    auditee_sign = models.FileField(upload_to='signatures/auditee/', null=True, blank=True)
    agreed_completion_date = models.DateField(null=True, blank=True)
    is_correction_done = models.BooleanField(default=False, null=True, blank=True)
    is_verification_done = models.BooleanField(default=False, null=True, blank=True)
    is_closure_done = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
class CorrectionInternalAuditReport(models.Model):
    audit_report = models.ForeignKey(InternalAuditReport, on_delete=models.CASCADE, related_name='corrections')
    # correction_details = models.TextField(null=True, blank=True)
    root_cause = models.TextField(null=True, blank=True)
    corrective_action = models.TextField(null=True, blank=True)
    correction_auditee_name = models.CharField(max_length=255, null=True, blank=True)
    correction_auditee_sign = models.FileField(upload_to='signatures/correction_auditee/', null=True, blank=True)
    correction_auditee_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class VerificationInternalAuditReport(models.Model):
    audit_report = models.ForeignKey(InternalAuditReport, on_delete=models.CASCADE, related_name='verifications')
    verification_auditor_name = models.CharField(max_length=255, null=True, blank=True)
    verification_auditor_sign = models.FileField(upload_to='signatures/verification_auditor/', null=True, blank=True)
    verification_auditor_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class ClosureInternalAuditReport(models.Model):
    audit_report = models.ForeignKey(InternalAuditReport, on_delete=models.CASCADE, related_name='closures')
    report_closure = models.TextField(null=True, blank=True)
    siteincharge_name = models.CharField(max_length=255, null=True, blank=True)
    siteincharge_sign = models.FileField(upload_to='signatures/siteincharge/', null=True, blank=True)
    siteincharge_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class TrainingTopic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class InductionTraining(models.Model):
    site_name = models.CharField(max_length=255)  # Or models.ForeignKey(Site, on_delete=models.CASCADE)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    faculty_name = models.CharField(max_length=255)
    faculty_signature = models.FileField(upload_to='faculty_signatures/')
    training_topics = models.CharField(max_length=255, null=True, blank=True)
    participants_file = models.FileField(upload_to="participants_files/", null=True, blank=True)
    topic_1 = models.CharField(max_length=255, null=True, blank=True)
    topic_2 = models.CharField(max_length=255, null=True, blank=True)
    topic_3 = models.CharField(max_length=255, null=True, blank=True)
    topic_4 = models.CharField(max_length=255, null=True, blank=True)
    topic_5 = models.CharField(max_length=255, null=True, blank=True)
    topic_6 = models.CharField(max_length=255, null=True, blank=True)
    topic_7 = models.CharField(max_length=255, null=True, blank=True)
    topic_8 = models.CharField(max_length=255, null=True, blank=True)
    topic_9 = models.CharField(max_length=255, null=True, blank=True)
    topic_10 = models.CharField(max_length=255, null=True, blank=True)
    topic_11 = models.CharField(max_length=255, null=True, blank=True)
    topic_12 = models.CharField(max_length=255, null=True, blank=True)
    topic_13 =models.CharField(max_length=255, null=True, blank=True)
    topic_14 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.site_name} - {self.date}"


class Participant(models.Model):
    training = models.ForeignKey(InductionTraining, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.name   


class FireExtinguisherInspection(models.Model):
    site_name = models.CharField(max_length=255)
    date_of_inspection = models.DateField()
    checked_by_name = models.CharField(max_length=255)
    signature = models.FileField(upload_to='signatures/', null=True, blank=True)

class FireExtinguisherDetail(models.Model):
    inspection = models.ForeignKey(FireExtinguisherInspection, on_delete=models.CASCADE, related_name='extinguishers')
    extinguisher_no = models.CharField(max_length=100)
    extinguisher_type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    seal_intact = models.BooleanField(default=True)
    pressure_in_gauge = models.CharField(max_length=100)
    tube_nozzle = models.CharField(max_length=100)
    painting_condition = models.CharField(max_length=100)
    refilling_date = models.DateField()
    due_date_refilling = models.DateField()
    due_date_hydro_test = models.DateField()
    access = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

class FireExtinguisherInspectionJSONFormat(models.Model):
    site_name = models.CharField(max_length=255)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_inspection = models.DateField()
    checked_by_name = models.CharField(max_length=255)
    signature = models.FileField(upload_to='signatures/', null=True, blank=True)
    fire_extinguisher_details = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class ToollboxTalkAttendence(models.Model):
    site_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    tbt_against_permit_no = models.CharField(max_length=255,null=True,blank=True)
    permit_date = models.DateField(null=True,blank=True)
    tbt_conducted_by_name = models.CharField(max_length=255,null=True,blank=True)
    tbt_conducted_by_signature = models.FileField(upload_to='signatures/tbt_conducted_by/', null=True, blank=True)
    name_of_contractor = models.CharField(max_length=255,null=True,blank=True)
    job_activity_in_detail = models.TextField(null=True,blank=True)
    
    use_of_ppes_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    use_of_tools_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    hazard_at_work_place_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    use_of_action_in_an_emergency_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    use_of_health_status_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    use_of_others_topic_discussed = models.CharField(max_length=500,null=True,blank=True)
    participant_upload_attachments = models.FileField(upload_to='signatures/participants/', null=True, blank=True)
    
    remarks = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class FirstAidRecord(models.Model):
    site_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    first_aid_name = models.CharField(max_length=255,null=True,blank=True)
    designation = models.CharField(max_length=255,null=True,blank=True)
    employee_of = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)


class HarnessInspection(models.Model):
    site_name = models.CharField(max_length=255)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    make_model = models.CharField(max_length=255)
    manufacturing_date = models.DateField()
    date_of_inspection = models.DateField()

    wear_or_twisted_strap_status = models.BooleanField()
    wear_or_twisted_strap_remarks = models.TextField(blank=True)

    waist_buckle_status = models.BooleanField()
    waist_buckle_remarks = models.TextField(blank=True)

    both_leg_strap_buckle_status = models.BooleanField()
    both_leg_strap_buckle_remarks = models.TextField(blank=True)

    waist_buckle_status_2 = models.BooleanField()
    waist_buckle_remarks_2 = models.TextField(blank=True)

    metal_d_ring_status = models.BooleanField()
    metal_d_ring_remarks = models.TextField(blank=True)

    buckle_working_status = models.BooleanField()
    buckle_working_remarks = models.TextField(blank=True)

    harness_shelf_life_status = models.BooleanField()
    harness_shelf_life_remarks = models.TextField(blank=True)

    lanyard_wear_twist_status = models.BooleanField()
    lanyard_wear_twist_remarks = models.TextField(blank=True)

    lanyard_two_ropes_status = models.BooleanField()
    lanyard_two_ropes_remarks = models.TextField(blank=True)

    sleeve_fissures_status = models.BooleanField()
    sleeve_fissures_remarks = models.TextField(blank=True)

    shock_absorber_status = models.BooleanField()
    shock_absorber_remarks = models.TextField(blank=True)

    snap_hooks_status = models.BooleanField()
    snap_hooks_remarks = models.TextField(blank=True)

    report = models.TextField(blank=True)

    inspector_name = models.CharField(max_length=255)
    inspector_signature = models.FileField(upload_to='harness_signatures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)    

class ExcavationPermit(models.Model):
    site_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    permit_number = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    description_of_work = models.CharField(max_length=255,null=True,blank=True)
    location_area_work = models.CharField(max_length=255,null=True,blank=True)
    length = models.CharField(max_length=255,null=True,blank=True)
    breadth = models.CharField(max_length=255,null=True,blank=True)
    depth = models.CharField(max_length=255,null=True,blank=True)
    start_work_date = models.DateField(null=True,blank=True)
    start_work_time = models.TimeField(null=True,blank=True)
    duration_work_day = models.CharField(max_length=255,null=True,blank=True)
    duration_work_hors = models.CharField(max_length=255,null=True,blank=True)
    purpose_of_excavation = models.CharField(max_length=255,null=True,blank=True)
    electrical_cable_description = models.CharField(max_length=255,null=True,blank=True)
    electrical_cable_name = models.CharField(max_length=255,null=True,blank=True)
    electrical_cable_date = models.DateTimeField(max_length=255,null=True,blank=True)
    sign_upload = models.FileField(upload_to='excavation_signatures/', blank=True, null=True)
    water_gas_description = models.CharField(max_length=255,null=True,blank=True)
    water_gas_name = models.CharField(max_length=255,null=True,blank=True)
    water_gas_date = models.DateTimeField(max_length=255,null=True,blank=True)
    water_sign_upload = models.FileField(upload_to='excavation_signatures/', blank=True, null=True)
    telephone_description = models.CharField(max_length=255,null=True,blank=True)
    telephone_name = models.CharField(max_length=255,null=True,blank=True)
    telephone_date = models.DateTimeField(max_length=255,null=True,blank=True)
    telephone_sign_upload = models.FileField(upload_to='excavation_signatures/', blank=True, null=True)
    road_barricading = models.BooleanField(default=False, null=True, blank=True)
    warning_sign = models.BooleanField(default=False, null=True, blank=True)
    barricading_excavated_area = models.BooleanField(default=False, null=True, blank=True)
    shoring_carried = models.BooleanField(default=False, null=True, blank=True)
    any_other_precaution = models.CharField(max_length=255,null=True,blank=True)
    name_acceptor = models.CharField(max_length=255,null=True,blank=True)
    acceptor_sign_upload = models.FileField(upload_to='excavation_signatures/', blank=True, null=True)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    check_by_name = models.CharField(max_length=255,null=True,blank=True)
    check_by_sign = models.FileField(upload_to='excavation_signatures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

class LadderInspection(models.Model):
    site_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    ladder_no = models.CharField(max_length=100,null=True,blank=True)
    date_of_inspection = models.DateField(null=True,blank=True)

    rail_strings_damaged = models.CharField(max_length=255,null=True,blank=True)
    rung_missing = models.CharField(max_length=255,null=True,blank=True)
    rung_broken = models.CharField(max_length=255,null=True,blank=True)
    rung_distance_uneven = models.CharField(max_length=255,null=True,blank=True)
    rungs_loose = models.CharField(max_length=255,null=True,blank=True)
    top_hook_missing_damaged = models.CharField(max_length=255,null=True,blank=True)
    bottom_non_skid_pad_missing_damaged = models.CharField(max_length=255,null=True,blank=True)
    non_slip_bases = models.CharField(max_length=255,null=True,blank=True)
    custom_check = models.CharField(max_length=255,null=True,blank=True)

    remarks = models.TextField(blank=True,null=True)

    inspected_by_name = models.CharField(max_length=255,null=True,blank=True)
    inspected_by_signature = models.FileField(upload_to='ladder_signatures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)    


class SuggestionSchemeReport(models.Model):
    site = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    designation = models.CharField(max_length=255,null=True,blank=True)
    suggestion_description = models.TextField(null=True,blank=True)
    benefits_upon_implementation = models.TextField(null=True,blank=True)
    evaluated_by = models.CharField(max_length=255,null=True,blank=True)
    evaluator_name = models.CharField(max_length=255,null=True,blank=True)
    evaluator_designation = models.CharField(max_length=255,null=True,blank=True)
    evaluation_remarks = models.TextField(null=True,blank=True)
    evaluator_signature = models.FileField(upload_to='suggestion_signatures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)      

class LotoAppliedInfo(models.Model):
    site_name = models.CharField(max_length=255,null=True,blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    applied_datetime = models.DateTimeField(null=True,blank=True)
    applied_lock_tag_number = models.CharField(max_length=100,null=True,blank=True)
    applied_permit_number = models.CharField(max_length=100,null=True,blank=True)
    applied_by_name = models.CharField(max_length=255,null=True,blank=True)
    applied_by_signature = models.FileField(upload_to='signatures/')
    applied_approved_by_name = models.CharField(max_length=255,null=True,blank=True)
    applied_approved_by_signature = models.FileField(upload_to='signatures/')

    def __str__(self):
        return f"{self.site_name} - {self.applied_lock_tag_number}"


class LotoRegister(models.Model):
    applied_info = models.ForeignKey(LotoAppliedInfo, on_delete=models.CASCADE, related_name='removal_info')
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    removed_datetime = models.DateTimeField(null=True,blank=True)
    removed_lock_tag_number = models.CharField(max_length=100,null=True,blank=True)
    removed_permit_number = models.CharField(max_length=100,null=True,blank=True)
    removed_by_name = models.CharField(max_length=255,null=True,blank=True)
    removed_by_signature = models.FileField(upload_to='signatures/')
    removed_site_incharge_name = models.CharField(max_length=255,null=True,blank=True)
    removed_approved_by_signature = models.FileField(upload_to='signatures/')

    def __str__(self):
        return f"Removal - {self.removed_lock_tag_number}"          