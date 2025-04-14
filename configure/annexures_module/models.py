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
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=25, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    permit_number = models.CharField(max_length=255, blank=True, null=True)
    name_of_external_agency = models.CharField(max_length=255, blank=True, null=True)
    type_of_permit = models.CharField(max_length=255, choices=PERMIT_CHOICES, blank=True, null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ClosureOfPermit(models.Model):
    CLOSURE_APPLICABLE_CHOICES = (
        ('where applicable', 'Where Applicable'),
        ('where not applicable', 'Where Not Applicable'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    closer_of_permit = models.CharField(max_length=255, choices=CLOSURE_APPLICABLE_CHOICES, null=True, blank=True)
    remarks = models.TextField(blank=True,null=True)
    permit = models.ForeignKey(PermitToWork, related_name='closure_of_permit', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ApprovePermit(models.Model):
    permit = models.ForeignKey(PermitToWork,related_name='permit', on_delete=models.SET_NULL, null=True, blank=True)
    issuer = models.ForeignKey(CustomUser,related_name='issuer', on_delete=models.SET_NULL, null=True, blank=True)
    approver = models.ForeignKey(CustomUser,related_name='approver', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(CustomUser,related_name='receiver', on_delete=models.SET_NULL, null=True, blank=True)
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
    location = models.CharField(max_length=255, blank=True, null=True)
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
    incident_nearmiss = models.ForeignKey(IncidentNearMiss, related_name='report_incident_nearmiss', on_delete=models.SET_NULL, null=True, blank=True)
    immediate_action_taken = models.CharField(max_length=255, null=True, blank=True)
    apparent_cause = models.CharField(max_length=255, null=True, blank=True)
    preventive_action = models.CharField(max_length=255, null=True, blank=True)
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
    issued_by = models.CharField(max_length=255, blank=True, null=True)
    issued_by_name = models.CharField(max_length=255, blank=True, null=True)
    issued_by_designation = models.CharField(max_length=255, blank=True, null=True)
    issued_by_department = models.CharField(max_length=255, blank=True, null=True)
    contractors_name = models.CharField(max_length=255, blank=True, null=True)
    description_safety_violation = models.TextField(max_length=255, blank=True, null=True)
    action_taken = models.CharField(max_length=255, blank=True, null=True)
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
    location = models.CharField(max_length=255, blank=True, null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CraneHydraInspections(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LandBankLocation, on_delete=models.SET_NULL, null=True, blank=True)
    equipment_name = models.CharField(max_length=255, blank=True, null=True)
    make_model = models.CharField(max_length=255, blank=True, null=True)
    identification_number = models.CharField(max_length=255, blank=True, null=True)
    inspection_date = models.DateTimeField(max_length=255, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
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
    location = models.CharField(max_length=255, blank=True, null=True)
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





class SafetyTrainingAttendance(models.Model):
    site_name = models.CharField(max_length=255)
    date = models.DateField()
    training_topic = models.CharField(max_length=255)
    faculty_name = models.CharField(max_length=255)
    faculty_signature = models.FileField(upload_to='signatures/faculty/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_name} - {self.training_topic} - {self.date}"

class Participant(models.Model):
    training = models.ForeignKey(SafetyTrainingAttendance, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    signature = models.FileField(upload_to='signatures/participants/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"
    

class InternalAuditReport(models.Model):
    site_name = models.CharField(max_length=255)
    date = models.DateField()

    observer_name = models.CharField(max_length=255)
    observer_sign = models.FileField(upload_to='signatures/observer/', null=True, blank=True)

    auditee_name = models.CharField(max_length=255)
    auditee_sign = models.FileField(upload_to='signatures/auditee/', null=True, blank=True)

    agreed_completion_date = models.DateField()
    correction_details = models.TextField()
    root_cause = models.TextField()
    corrective_action = models.TextField()

    correction_auditee_name = models.CharField(max_length=255)
    correction_auditee_sign = models.FileField(upload_to='signatures/correction_auditee/', null=True, blank=True)
    correction_auditee_date = models.DateField()

    verification_auditor_name = models.CharField(max_length=255)
    verification_auditor_sign = models.FileField(upload_to='signatures/verification_auditor/', null=True, blank=True)
    verification_auditor_date = models.DateField()

    report_closure = models.TextField()

    siteincharge_name = models.CharField(max_length=255)
    siteincharge_sign = models.FileField(upload_to='signatures/siteincharge/', null=True, blank=True)
    siteincharge_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_name} - {self.date}"

    

class TrainingTopic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class InductionTraining(models.Model):
    site_name = models.CharField(max_length=255)  # Or models.ForeignKey(Site, on_delete=models.CASCADE)
    date = models.DateField()
    faculty_name = models.CharField(max_length=255)
    faculty_signature = models.FileField(upload_to='faculty_signatures/')
    training_topics = models.ManyToManyField(TrainingTopic, related_name='induction_trainings')

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
    location = models.CharField(max_length=255)
    seal_intact = models.BooleanField(default=True)
    pressure_in_gauge = models.CharField(max_length=100)
    tube_nozzle = models.CharField(max_length=100)
    painting_condition = models.CharField(max_length=100)
    refilling_date = models.DateField()
    due_date_refilling = models.DateField()
    due_date_hydro_test = models.DateField()
    access = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)



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
