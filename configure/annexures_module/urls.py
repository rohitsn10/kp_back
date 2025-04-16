from django.urls import path
from annexures_module.views import *

urlpatterns = [

    path('create_permit_to_work', PermitToWorkViewSet.as_view({'post': 'create'}), name='create_permit_to_work'),
    path('get_permit_to_work', GetPermitToWorkViewSet.as_view({'get': 'list'}), name='get_permit_to_work'),
    path('loaction_id_wise_permit_to_work/<int:location_id>', LocationIdWisePermitToWorkViewSet.as_view({'get': 'list'}), name='loaction_id_wise_permit_to_work'),

    path('update_permit_to_work/<int:permit_id>', UpdatePermitToWorkViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_permit_to_work'),
    path('approve_permit/<int:permit_id>', ApprovePermitToWorkViewSet.as_view({'put':'update'}), name='approve_permit'),
    path('closure_of_permit/<int:permit_id>', ClosureOfPermitToWorkViewSet.as_view({'put':'update'}), name='closure_of_permit'),

    path('create_incident_nearmiss_investigation', IncidentNearmissInvestigationViewSet.as_view({'post': 'create'}), name='create_incident_nearmiss_investigation'),
    path('get_incident_nearmiss_investigation', GetIncidentNearmissInvestigationViewSet.as_view({'get': 'list'}), name='get_incident_nearmiss_investigation'),

    path('id_wise_incident_nearmiss_investigation/<int:incident_nearmiss_id>', IDWiseGetIncidentNearmissInvestigationViewSet.as_view({'get': 'list'}), name='id_wise_incident_nearmiss_investigation'),

    path('update_incident_nearmiss_investigation/<int:id>', UpdateIncidentNearmissInvestigationViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_incident_nearmiss_investigation'),
    path('reviewed_incident_nearmiss_by_reviewer/<int:id>', ReviewByIncidentNearmissViewSet.as_view({'put':'update'}), name='reviewed_incident_nearmiss_by_reviewer'),
    path('approve_incident_nearmiss_by_reviewer/<int:id>', ApproveByIncidentNearmissViewSet.as_view({'put':'update'}), name='approve_incident_nearmiss_by_reviewer'),

    path('create_report_of_incident_nearmiss/<int:incident_nearmiss_id>', ReportOfIncidentNearmissViewSet.as_view({'post': 'create'}), name='create_report_of_incident_nearmiss'),

    path('create_safety_violation_report', SafetyViolationReportViewSet.as_view({'post': 'create'}), name='create_safety_violation_report'),
    path('get_safety_violation_report', GetSafetyViolationReportViewSet.as_view({'get': 'list'}), name='get_safety_violation_report'),

    path('create_boom_lift_inspection', BoomLiftInspectionViewSet.as_view({'post': 'create'}), name='create_boom_lift_inspection'),
    path('get_boom_lift_inspection', GetBoomLiftInspectionViewSet.as_view({'get': 'list'}), name='get_boom_lift_inspection'),

    path('create_crane_hydra_inspection', CraneHydraInspectionChecklistViewSet.as_view({'post': 'create'}), name='create_crane_hydra_inspection'),
    path('get_crane_hydra_inspection', GetCraneHydraInspectionChecklistViewSet.as_view({'get': 'list'}), name='get_crane_hydra_inspection'),      

    path('create_trailer_inspection', TrailerInspectionChecklistViewSet.as_view({'post': 'create'}), name='create_trailer_inspection'),
    path('get_trailer_inspection', GetTrailerInspectionChecklistViewSet.as_view({'get': 'list'}), name='get_trailer_inspection'),   

    path('create_mock_drill_report', MockDrillReportViewSet.as_view({'post': 'create'}), name='create_mock_drill_report'),
    path('get_mock_drill_report', GetMockDrillReportViewSet.as_view({'get': 'list'}), name='get_mock_drill_report'),

    path('create_safety_training_attendance', SafetyTrainingAttendanceViewSet.as_view({'post': 'create'}), name='create_safety_training_attendance'),
    path('get_safety_training_attendance', GetTrainingAttendanceViewSet.as_view({'get': 'list'}), name='get_safety_training_attendance'),

    path('create_internal_audit_report', InternalAuditReportViewSet.as_view({'post': 'create'}), name='create_internal_audit_report'),
    path('get_internal_audit_report', GetInternalAuditReportViewSet.as_view({'get': 'list'}), name='get_internal_audit_report'),


    path('create_induction_training', CreateInductionTrainingViewSet.as_view({'post': 'create'}), name='create_induction_training'),
    path('get_induction_training', GetInductionTrainingViewSet.as_view({'get': 'list'}), name='get_induction_training'),

    path('create_fire_extinguisher_inspection', FireExtinguisherInspectionViewSet.as_view({'post': 'create'}), name='create_fire_extinguisher_inspection'),
    path('get_fire_extinguisher_inspection', FireExtinguisherInspectionViewSet.as_view({'get': 'list'}), name='get_fire_extinguisher_inspection'),

    path('create_tooltalk_attendence',ToollboxTalkAttendenceCreateViewSet.as_view({'post': 'create'}),name = 'create_tooltalk_attendence'),
    path('get_tooltalk_attendence',ToollboxTalkAttendenceGetViewSet.as_view({'get': 'list'}),name = 'get_tooltalk_attendence'),
    path('location_wise_get_tooltalk_attendence/<int:location_id>',LocationIdwiseGetToollboxTalkAttendenceGetViewSet.as_view({'get': 'list'}),name = 'get_location_wise_tooltalk_attendence'),
    
    path('create_first_aid_record',FirstAidRecordViewSet.as_view({'post': 'create'}),name = 'create_first_aid_record'),
    path('get_first_aid_record',GetListFirstrecordViewSet.as_view({'get': 'list'}),name = 'get_first_aid_record'),
    path('get_location_wise_first_aid_record/<int:location_id>',LocationIdwiseGetListFirstrecordViewSet.as_view({'get': 'list'}),name = 'get_location_wise_first_aid_record'),

    path('create_harness_inspection', HarnessInspectionViewSet.as_view({'post': 'create'}), name='create_harness_inspection'),
    path('get_harness_inspection', HarnessInspectionViewSet.as_view({'get': 'list'}), name='get_harness_inspection'),

    path('create_excavationpermit', ExcavationPermitViewSet.as_view({'post': 'create'}), name='create_harness_inspection'),
    path('get_excavationpermit', ExcavationPermitViewSet.as_view({'get': 'list'}), name='get_harness_inspection')


]