from django.urls import path
from annexures_module.views import *

urlpatterns = [

    path('create_permit_to_work', PermitToWorkViewSet.as_view({'post': 'create'}), name='create_permit_to_work'),
    path('get_permit_to_work', GetPermitToWorkViewSet.as_view({'get': 'list'}), name='get_permit_to_work'),
    path('loaction_id_wise_permit_to_work/<int:location_id>', LocationIdWisePermitToWorkViewSet.as_view({'get': 'list'}), name='loaction_id_wise_permit_to_work'),

    path('update_permit_to_work/<int:permit_id>', UpdatePermitToWorkViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_permit_to_work'),
    path('issuer_approve_permit/<int:permit_id>', IssueApprovePermitToWorkViewSet.as_view({'put':'update'}), name='issuer_approve_permit'),
    path('issuer_get_permit/<int:permit_id>', IssueGetPermitToWorkViewSet.as_view({'get':'list'}), name='issuer_get_permit'),
    path('approver_approve_permit/<int:permit_id>', ApproverApprovePermitToWorkViewSet.as_view({'put':'update'}), name='approver_approve_permit'),
    path('approver_get_permit/<int:permit_id>', ApproverGetPermitToWorkViewSet.as_view({'get':'list'}), name='approver_get_permit'),
    path('receiver_approve_permit/<int:permit_id>', RecevierApprovePermitToWorkViewSet.as_view({'put':'update'}), name='receiver_approve_permit'),
    path('receiver_get_permit/<int:permit_id>', ReceiverGetPermitToWorkViewSet.as_view({'get':'list'}), name='receiver_get_permit'),
    path('closure_of_permit/<int:permit_id>', ClosureOfPermitToWorkViewSet.as_view({'put':'update'}), name='closure_of_permit'),

    path('create_incident_nearmiss_investigation', IncidentNearmissInvestigationViewSet.as_view({'post': 'create'}), name='create_incident_nearmiss_investigation'),
    path('get_incident_nearmiss_investigation/<int:location_id>', GetIncidentNearmissInvestigationViewSet.as_view({'get': 'list'}), name='get_incident_nearmiss_investigation'),

    path('id_wise_incident_nearmiss_investigation/<int:incident_nearmiss_id>', IDWiseGetIncidentNearmissInvestigationViewSet.as_view({'get': 'list'}), name='id_wise_incident_nearmiss_investigation'),

    path('update_incident_nearmiss_investigation/<int:id>', UpdateIncidentNearmissInvestigationViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_incident_nearmiss_investigation'),
    path('reviewed_incident_nearmiss_by_reviewer/<int:id>', ReviewByIncidentNearmissViewSet.as_view({'put':'update'}), name='reviewed_incident_nearmiss_by_reviewer'),
    path('approve_incident_nearmiss_by_reviewer/<int:id>', ApproveByIncidentNearmissViewSet.as_view({'put':'update'}), name='approve_incident_nearmiss_by_reviewer'),

    path('create_report_of_incident_nearmiss', ReportOfIncidentNearmissViewSet.as_view({'post': 'create'}), name='create_report_of_incident_nearmiss'),
    path('get_report_of_incident_nearmiss/<int:location_id>', GetReportOfIncidentNearmissViewSet.as_view({'get': 'list'}), name='get_report_of_incident_nearmiss'),

    path('create_safety_violation_report', SafetyViolationReportViewSet.as_view({'post': 'create'}), name='create_safety_violation_report'),
    path('get_safety_violation_report/<int:location_id>', GetSafetyViolationReportViewSet.as_view({'get': 'list'}), name='get_safety_violation_report'),

    path('create_boom_lift_inspection', BoomLiftInspectionViewSet.as_view({'post': 'create'}), name='create_boom_lift_inspection'),
    path('get_boom_lift_inspection/<int:location_id>', GetBoomLiftInspectionViewSet.as_view({'get': 'list'}), name='get_boom_lift_inspection'),

    path('create_crane_hydra_inspection', CraneHydraInspectionChecklistViewSet.as_view({'post': 'create'}), name='create_crane_hydra_inspection'),
    path('get_crane_hydra_inspection/<int:location_id>', GetCraneHydraInspectionChecklistViewSet.as_view({'get': 'list'}), name='get_crane_hydra_inspection'),      

    path('create_trailer_inspection', TrailerInspectionChecklistViewSet.as_view({'post': 'create'}), name='create_trailer_inspection'),
    path('get_trailer_inspection/<int:location_id>', GetTrailerInspectionChecklistViewSet.as_view({'get': 'list'}), name='get_trailer_inspection'),   

    path('create_mock_drill_report', MockDrillReportViewSet.as_view({'post': 'create'}), name='create_mock_drill_report'),
    path('get_mock_drill_report/<int:location_id>', GetMockDrillReportViewSet.as_view({'get': 'list'}), name='get_mock_drill_report'),

    path('create_safety_training_attendance', SafetyTrainingAttendanceViewSet.as_view({'post': 'create'}), name='create_safety_training_attendance'),
    path('get_safety_training_attendance/<int:location_id>', GetTrainingAttendanceViewSet.as_view({'get': 'list'}), name='get_safety_training_attendance'),

    path('create_minutes_of_safety_training', MinutesSafetyTrainingViewSet.as_view({'post': 'create'}), name='create_minutes_of_safety_training'),
    path('get_minutes_of_safety_training/<int:location_id>', GetMinutesSafetyTrainingViewSet.as_view({'get': 'list'}), name='get_minutes_of_safety_training'),

    path('create_internal_audit_report', InternalAuditReportViewSet.as_view({'post': 'create'}), name='create_internal_audit_report'),
    path('get_internal_audit_report/<int:location_id>', GetInternalAuditReportViewSet.as_view({'get': 'list'}), name='get_internal_audit_report'),

    path('create_correction_internal_audit_report', CorrectionInternalAuditReportViewSet.as_view({'post': 'create'}), name='create_correction_internal_audit_report'),
    path('get_correction_internal_audit_report/<int:audit_report>', GetCorrectionInternalAuditReportViewSet.as_view({'get': 'list'}), name='get_correction_internal_audit_report'),

    path('create_verification_internal_audit_report', VerificationInternalAuditReportViewSet.as_view({'post': 'create'}), name='create_verification_internal_audit_report'),
    path('get_verification_internal_audit_report/<int:audit_report>', GetVerificationInternalAuditReportViewSet.as_view({'get': 'list'}), name='get_verification_internal_audit_report'),

    path('create_closure_internal_audit_report', ClosureInternalAuditReportViewSet.as_view({'post': 'create'}), name='create_closure_internal_audit_report'),
    path('get_closure_internal_audit_report/<int:audit_report>', GetClosureInternalAuditReportViewSet.as_view({'get': 'list'}), name='get_closure_internal_audit_report'),


    path('create_induction_training', CreateInductionTrainingViewSet.as_view({'post': 'create'}), name='create_induction_training'),
    path('get_induction_training/<int:location_id>', GetInductionTrainingViewSet.as_view({'get': 'list'}), name='get_induction_training'),

    path('create_fire_extinguisher_inspection', FireExtinguisherInspectionViewSet.as_view({'post': 'create'}), name='create_fire_extinguisher_inspection'),
    path('get_fire_extinguisher_inspection/<int:location_id>', GetFireExtinguisherInspectionViewSet.as_view({'get': 'list'}), name='get_fire_extinguisher_inspection'),

    path('create_tooltalk_attendence',ToollboxTalkAttendenceCreateViewSet.as_view({'post': 'create'}),name = 'create_tooltalk_attendence'),
    path('get_tooltalk_attendence',ToollboxTalkAttendenceGetViewSet.as_view({'get': 'list'}),name = 'get_tooltalk_attendence'),
    path('location_wise_get_tooltalk_attendence/<int:location_id>',LocationIdwiseGetToollboxTalkAttendenceGetViewSet.as_view({'get': 'list'}),name = 'get_location_wise_tooltalk_attendence'),
    
    path('create_first_aid_record',FirstAidRecordViewSet.as_view({'post': 'create'}),name = 'create_first_aid_record'),
    path('get_first_aid_record',GetListFirstrecordViewSet.as_view({'get': 'list'}),name = 'get_first_aid_record'),
    path('get_location_wise_first_aid_record/<int:location_id>',LocationIdwiseGetListFirstrecordViewSet.as_view({'get': 'list'}),name = 'get_location_wise_first_aid_record'),

    path('create_harness_inspection', HarnessInspectionViewSet.as_view({'post': 'create'}), name='create_harness_inspection'),
    path('get_harness_inspection/<int:location_id>', GetHarnessInspectionViewSet.as_view({'get': 'list'}), name='get_harness_inspection'),

    path('create_excavationpermit', ExcavationPermitViewSet.as_view({'post': 'create'}), name='create_harness_inspection'),
    path('get_excavationpermit/<int:location_id>', GetExcavationPermitViewSet.as_view({'get': 'list'}), name='get_harness_inspection'),

    path('create_ladder_inspection', LadderInspectionViewSet.as_view({'post': 'create'}), name='create_ladder_inspection'),
    path('get_ladder_inspection/<int:location_id>', GetLadderInspectionViewSet.as_view({'get': 'list'}), name='get_ladder_inspection'),

    path('create_suggestion_scheme_report', SuggestionSchemeReportViewSet.as_view({'post': 'create'}), name='create_suggestion_scheme_report'),
    path('get_suggestion_scheme_report/<int:location_id>', GetSuggestionSchemeReportViewSet.as_view({'get': 'list'}), name='get_suggestion_scheme_report'),

    path('create_loto_register', LotoRegisterViewSet.as_view({'post': 'create'}), name='create_loto_register'),
    path('get_loto_register/<int:location_id>', GetLotoRegisterViewSet.as_view({'get': 'list'}), name='get_loto_register'),

    path('remove_loto_register', LotoClearedInfoViewSet.as_view({'post': 'create'}), name='remove_loto_register'),
    path('get_remove_loto_register/<int:loto_id>', GetLotoClearedInfoViewSet.as_view({'get': 'list'}), name='get_remove_loto_register'),


]