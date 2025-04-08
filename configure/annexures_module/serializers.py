from rest_framework import serializers
from .models import *


class PermitToWorkSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source= 'location.land_bank_location_name', read_only=True)
    class Meta:
        model = PermitToWork
        fields = [
            'id','user','location','location_name','site_name', 'department', 'permit_number', 'name_of_external_agency', 
            'type_of_permit', 'job_activity_details', 'location_area', 'tools_equipment', 
            'permit_issue_for', 'hazard_consideration', 'fire_protection', 'job_preparation',
            'other_permit_description', 'other_hazard_consideration', 'other_fire_protection',
            'risk_assessment_number', 'other_job_preparation', 'day', 'night', 'expiry_date', 'is_active', 'created_at', 'updated_at'
        ]

class ApprovePermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovePermit
        fields = ['id', 'permit', 'issuer', 'approver', 'receiver', 'start_time', 'end_time', 'created_at']

class ClosureOfPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosureOfPermit
        fields = ['id', 'user', 'closer_of_permit', 'remarks', 'permit', 'created_at']

class IncidentNearMissSerializer(serializers.ModelSerializer):
    user_status = serializers.SerializerMethodField()
    class Meta:
        model = IncidentNearMiss
        fields = [
            'id', 'user', 'site_name', 'location', 'date_of_occurrence', 'date_of_report', 'category', 'title_incident_nearmiss',
            'description', 'investigation_findings', 'physical_factor', 'human_factor', 'system_factor', 'user_status', 'recommendation_for_preventive_action',
            'committee_members', 'created_at', 'updated_at'
        ]
    def get_user_status(self, obj):
        request = self.context.get('request')
        if request and request.user:
            user = request.user
            has_reviewed = ReviewIncidentNearMiss.objects.filter(incident_nearmiss=obj, reviewer=user).exists()
            if has_reviewed:
                return "reviewed"
            else:
                return "under review"
        return obj.status
    
class ReviewIncidentNearMissSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewIncidentNearMiss
        fields = ['id', 'incident_nearmiss', 'reviewer', 'remarks', 'created_at']

class ApproveIncidentNearMissSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApproveIncidentNearMiss
        fields = ['id', 'incident_nearmiss', 'approver', 'remarks', 'created_at']

class ReportOfIncidentNearmissSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportOfIncidentNearmiss
        fields = ['id','user', 'incident_nearmiss', 'immediate_action_taken', 'apparent_cause', 'preventive_action', 'created_at']

class SafetyViolationReportAgainstUnsafeACTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyViolationReportAgainstUnsafeACT
        fields = [
            'id', 'user', 'site_name', 'issued_to', 'issued_to_violator_name', 'issued_to_designation', 'issued_to_department',
            'issued_by', 'issued_by_name', 'issued_by_designation', 'issued_by_department', 'contractors_name', 'description_safety_violation',
            'action_taken', 'created_at', 'updated_at'
        ]

class BoomLiftInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoomLiftInspection
        fields = [
            'id', 'user', 'site_name', 'location', 'equipment_name', 'make_model', 'identification_number', 'inspection_date',
            'all_valid_document_observations', 'all_valid_document_action_by', 'all_valid_document_remarks', 'operator_fitness_certificate_observations',
            'operator_fitness_certificate_action_by', 'operator_fitness_certificate_remarks', 'main_horn_reverse_horn_observations', 'main_horn_reverse_horn_action_by',
            'main_horn_reverse_horn_remarks', 'emergency_lowering_observations', 'emergency_lowering_action_by', 'emergency_lowering_remarks',
            'tyre_pressure_condition_observations', 'tyre_pressure_condition_action_by', 'tyre_pressure_condition_remarks', 'any_leakage_observations', 'any_leakage_action_by',
            'any_leakage_remarks', 'smooth_function_observations', 'smooth_function_action_by', 'smooth_function_remarks',
            'brake_stop_hold_observations', 'brake_stop_hold_action_by', 'brake_stop_hold_remarks', 'condition_of_all_observations',
            'condition_of_all_action_by', 'condition_of_all_remarks', 'guard_rails_without_damage_observations', 'guard_rails_without_damage_action_by',
            'guard_rails_without_damage_remarks', 'toe_guard_observations', 'toe_guard_action_by', 'toe_guard_remarks', 'platform_condition_observations',
            'platform_condition_action_by', 'platform_condition_remarks', 'door_lock_platform_observations', 'door_lock_platform_action_by', 'door_lock_platform_remarks',
            'swl_observations', 'swl_action_by', 'swl_remarks', 'over_load_indicator_cut_off_devices_observations', 'over_load_indicator_cut_off_devices_action_by',
            'over_load_indicator_cut_off_devices_remarks', 'battery_condition_observations', 'battery_condition_action_by', 'battery_condition_remarks',
            'operator_list_observations', 'operator_list_action_by', 'operator_list_remarks', 'ppe_observations', 'ppe_action_by', 'ppe_remarks',
            'created_at', 'updated_at'
        ]


class CraneHydraInspectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CraneHydraInspections
        fields = [
            "user", "equipment_name", "make_model", "identification_number", "inspection_date",
            "site_name", "location", "all_valid_document_observations", "all_valid_document_action_by",
            "all_valid_document_remarks", "driver_fitness_certificate_observations", "driver_fitness_certificate_action_by",
            "driver_fitness_certificate_remarks", "main_horn_reverse_horn_observations", "main_horn_reverse_horn_action_by",
            "main_horn_reverse_horn_remarks", "cutch_brake_observations", "cutch_brake_action_by", "cutch_brake_remarks",
            "tyre_pressure_condition_observations", "tyre_pressure_condition_action_by", "tyre_pressure_condition_remarks",
            "head_light_indicator_observations", "head_light_indicator_action_by", "head_light_indicator_remarks",
            "seat_belt_observations", "seat_belt_action_by", "seat_belt_remarks", "wiper_blade_observations",
            "wiper_blade_action_by", "wiper_blade_remarks", "side_mirror_observations", "side_mirror_action_by",
            "side_mirror_remarks", "wind_screen_observations", "wind_screen_action_by", "wind_screen_remarks",
            "door_lock_observations", "door_lock_action_by", "door_lock_remarks", "battery_condition_observations",
            "battery_condition_action_by", "battery_condition_remarks", "hand_brake_observations", "hand_brake_action_by",
            "hand_brake_remarks", "swl_on_boom_lift_observations", "swl_on_boom_lift_action_by", "swl_on_boom_lift_remarks",
            "any_leakage_observations", "any_leakage_action_by", "any_leakage_remarks", "speedometere_observations",
            "speedometere_action_by", "speedometere_remarks", "guard_parts_observations", "guard_parts_action_by",
            "guard_parts_remarks", "ppe_observations", "ppe_action_by", "ppe_remarks", "created_at", "updated_at"
        ]

class TrailerInspectionChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailerInspectionChecklist
        fields = [
            'id',
            "user",
            "equipment_name",
            "make_model",
            "identification_number",
            "inspection_date",
            "site_name",
            "location",
            "all_valid_document_observations",
            "all_valid_document_action_by",
            "all_valid_document_remarks",
            "driver_fitness_certificate_observations",
            "driver_fitness_certificate_action_by",
            "driver_fitness_certificate_remarks",
            "main_horn_reverse_horn_observations",
            "main_horn_reverse_horn_action_by",
            "main_horn_reverse_horn_remarks",
            "cutch_brake_observations",
            "cutch_brake_action_by",
            "cutch_brake_remarks",
            "tyre_pressure_condition_observations",
            "tyre_pressure_condition_action_by",
            "tyre_pressure_condition_remarks",
            "head_light_indicator_observations",
            "head_light_indicator_action_by",
            "head_light_indicator_remarks",
            "seat_belt_observations",
            "seat_belt_action_by",
            "seat_belt_remarks",
            "wiper_blade_observations",
            "wiper_blade_action_by",
            "wiper_blade_remarks",
            "side_mirror_observations",
            "side_mirror_action_by",
            "side_mirror_remarks",
            "wind_screen_observations",
            "wind_screen_action_by",
            "wind_screen_remarks",
            "door_lock_action_by",
            "door_lock_remarks",
            "door_lock_observations",
            "battery_condition_observations",
            "battery_condition_action_by",
            "battery_condition_remarks",
            "hand_brake_observations",
            "hand_brake_action_by",
            "hand_brake_remarks",
            "any_leakage_observations",
            "any_leakage_action_by",
            "any_leakage_remarks",
            "speedometere_observations",
            "speedometere_action_by",
            "speedometere_remarks",
            "guard_parts_observations",
            "guard_parts_action_by",
            "guard_parts_remarks",
            "ppe_observations",
            "ppe_action_by",
            "ppe_remarks"
        ]

class MockDrillReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockDrillReport
        fields = [
            'id', 'user', 'site_plant_name', 'location', 'emergncy_scenario_mock_drill',
            'type_of_mock_drill', 'mock_drill_date', 'mock_drill_time', 'completed_time',
            'overall_time', 'team_leader_incident_controller', 'performance', 'traffic_or_evacuation',
            'ambulance_first_aid_ppe_rescue', 'team_member1', 'team_member2', 'table_top_records',
            'description_of_control', 'head_count_at_assembly_point', 'rating_of_emergency_team_members',
            'overall_rating', 'observation', 'recommendations', 'created_at', 'updated_at'
        ]