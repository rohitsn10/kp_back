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
            'overall_time', 'drill_details', 'team_members', 'table_top_records',
            'description_of_control', 'head_count_at_assembly_point', 'rating_of_emergency_team_members',
            'overall_rating', 'observation', 'recommendations', 'created_at', 'updated_at'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        # Format drill_details with full image URLs
        drill_details = representation.get("drill_details", {})
        formatted_details = {}
        for key, value in drill_details.items():
            if isinstance(value, dict):
                formatted_details[key] = value.get("value")
                image_url = value.get("image")
                if image_url and request:
                    image_url = request.build_absolute_uri(image_url)
                formatted_details[f"{key}_image"] = image_url
            else:
                formatted_details[key] = value
        representation["drill_details"] = formatted_details

        # Format team_members with full image URLs
        team_members = representation.get("team_members", [])
        formatted_members = []
        for member in team_members:
            member_name = member.get("name")
            member_image = member.get("image")
            if member_image and request:
                member_image = request.build_absolute_uri(member_image)

            formatted_member = {
                "member_name": member_name,
                "member_image": member_image,
            }

            formatted_members.append(formatted_member)
        representation["team_members"] = formatted_members
        head_count_data = representation.get("head_count_at_assembly_point", {})
        formatted_head_count = {
            "people_present_as_per_record": {
                "no_of_kpi_employee": head_count_data.get("people_present_as_per_record", {}).get("no_of_kpi_employee"),
                "no_of_contractor_employee": head_count_data.get("people_present_as_per_record", {}).get("no_of_contractor_employee"),
                "no_of_visitor_angies": head_count_data.get("people_present_as_per_record", {}).get("no_of_visitor_angies"),
                "remarks": head_count_data.get("people_present_as_per_record", {}).get("head_count_remarks")
            },
            "actual_participants_participate_in_drill": {
                "no_of_kpi_employee": head_count_data.get("actual_participants_participate_in_drill", {}).get("no_of_kpi_employee"),
                "no_of_contractor_employee": head_count_data.get("actual_participants_participate_in_drill", {}).get("no_of_contractor_employee"),
                "no_of_visitor_angies": head_count_data.get("actual_participants_participate_in_drill", {}).get("no_of_visitor_angies"),
                "remarks": head_count_data.get("actual_participants_participate_in_drill", {}).get("actual_remarks")
            },
            "no_of_people_not_participated_in_drill": {
                "no_of_kpi_employee": head_count_data.get("no_of_people_not_participated_in_drill", {}).get("no_of_kpi_employee"),
                "no_of_contractor_employee": head_count_data.get("no_of_people_not_participated_in_drill", {}).get("no_of_contractor_employee"),
                "no_of_visitor_angies": head_count_data.get("no_of_people_not_participated_in_drill", {}).get("no_of_visitor_angies"),
                "remarks": head_count_data.get("no_of_people_not_participated_in_drill", {}).get("not_participated_remarks")
            }
        }
        representation["head_count_at_assembly_point"] = formatted_head_count
        return representation




class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'designation', 'signature']

class TrainingAttendanceSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = SafetyTrainingAttendance
        fields = ['id', 'site_name', 'date', 'training_topic', 'faculty_name', 'faculty_signature', 'participants']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        training = SafetyTrainingAttendance.objects.create(**validated_data)
        for participant_data in participants_data:
            Participant.objects.create(training=training, **participant_data)
        return training


class InternalAuditReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalAuditReport
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['name', 'designation', 'remarks']


class InductionTrainingSerializer(serializers.ModelSerializer):
    # participants = ParticipantSerializer(many=True)
    # training_topics = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=TrainingTopic.objects.all()
    # )

    class Meta:
        model = InductionTraining
        fields = ['id', 'site_name', 'date', 'faculty_name', 'faculty_signature', 'training_topics', 'participants_file', 'topic_1', 'topic_2', 'topic_3',
                  'topic_4', 'topic_5', 'topic_6', 'topic_7', 'topic_8', 'topic_9', 'topic_10', 'topic_11', 'topic_12', 'topic_13', 'topic_14']

    # def create(self, validated_data):
    #     # participants_data = validated_data.pop('participants')
    #     training_topics = validated_data.pop('training_topics')
    #     training = InductionTraining.objects.create(**validated_data)
    #     training.training_topics.set(training_topics)
    #     # for participant_data in participants_data:
    #     #     Participant.objects.create(training=training, **participant_data)
    #     return training
    


class FireExtinguisherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireExtinguisherDetail
        fields = '__all__'
        extra_kwargs = {'inspection': {'required': False}}

import json
class FireExtinguisherInspectionSerializer(serializers.ModelSerializer):
    extinguishers = FireExtinguisherDetailSerializer(many=True, required=True)

    class Meta:
        model = FireExtinguisherInspection
        fields = ['id', 'site_name', 'date_of_inspection', 'checked_by_name', 'signature', 'extinguishers']

    def to_internal_value(self, data):
        # Check and parse 'extinguishers' if it's a JSON string (comes as string in multipart/form-data)
        if 'extinguishers' in data and isinstance(data.get('extinguishers'), str):
            try:
                data = data.copy()  # Make a mutable copy for QueryDict
                data['extinguishers'] = json.loads(data['extinguishers'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    'extinguishers': 'Invalid JSON format.'
                })
        return super().to_internal_value(data)

    def create(self, validated_data):
        extinguisher_data = validated_data.pop('extinguishers')
        inspection = FireExtinguisherInspection.objects.create(**validated_data)
        for extinguisher in extinguisher_data:
            FireExtinguisherDetail.objects.create(inspection=inspection, **extinguisher)
        return inspection

class FireExtinguisherInspectionJSONFormatSerializer(serializers.ModelSerializer):

    class Meta: 
        model = FireExtinguisherInspectionJSONFormat
        fields = ['id', 'site_name', 'date_of_inspection', 'checked_by_name', 'signature', 'fire_extinguisher_details', 'created_at']


class ToollboxTalkAttendenceSerializer(serializers.ModelSerializer):
    tbt_conducted_by_signature = serializers.SerializerMethodField()
    participant_upload_attachments = serializers.SerializerMethodField()
    class Meta:
        model = ToollboxTalkAttendence
        fields = [
            'id', 'site_name', 'location', 'date', 'time',
            'tbt_against_permit_no', 'permit_date', 'tbt_conducted_by_name',
            'tbt_conducted_by_signature', 'name_of_contractor',
            'job_activity_in_detail',
            'use_of_ppes_topic_discussed', 'use_of_tools_topic_discussed',
            'hazard_at_work_place_topic_discussed',
            'use_of_action_in_an_emergency_topic_discussed',
            'use_of_health_status_topic_discussed',
            'use_of_others_topic_discussed',
            'participant_upload_attachments', 'remarks',
            'created_at', 'updated_at'
        ]

    def get_tbt_conducted_by_signature(self, obj):
        if obj.tbt_conducted_by_signature:
            return self.context['request'].build_absolute_uri(obj.tbt_conducted_by_signature.url)
        return None

    def get_participant_upload_attachments(self, obj):
        if obj.participant_upload_attachments:
            return self.context['request'].build_absolute_uri(obj.participant_upload_attachments.url)
        return None


class FirstAidRecordSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.land_bank_location_name', read_only=True)
    class Meta:
        model = FirstAidRecord
        fields = [
            'id', 'site_name', 'location','location_name','date',
            'first_aid_name', 'designation', 'employee_of', 'description',
            'created_at', 'updated_at'
        ]

class HarnessInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarnessInspection
        fields = '__all__'

class ExcavationPermitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExcavationPermit
        fields = [
            'id', 'site_name', 'location', 'permit_number', 'date', 'description_of_work', 'location_area_work', 'length', 'breadth',
            'depth', 'start_work_date', 'start_work_time', 'duration_work_day', 'duration_work_hors', 'purpose_of_excavation',
            'electrical_cable_description', 'electrical_cable_name', 'electrical_cable_date', 'sign_upload', 'water_gas_description',
            'water_gas_name', 'water_gas_date', 'water_sign_upload', 'telephone_description', 'telephone_name', 'telephone_date',
            'telephone_sign_upload', 'road_barricading', 'warning_sign', 'barricading_excavated_area', 'shoring_carried', 'any_other_precaution',
            'name_acceptor', 'acceptor_sign_upload', 'remarks', 'check_by_name', 'check_by_sign', 'created_at', 'updated_at'
        ]