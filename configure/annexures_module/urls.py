from django.urls import path
from annexures_module.views import *

urlpatterns = [

    path('create_permit_to_work', PermitToWorkViewSet.as_view({'post': 'create'}), name='create_permit_to_work'),
    path('get_permit_to_work', GetPermitToWorkViewSet.as_view({'get': 'list'}), name='get_permit_to_work'),

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

    path('create_mock_drill_report', MockDrillReportViewSet.as_view({'post': 'create'}), name='create_mock_drill_report'),
    path('get_mock_drill_report', GetMockDrillReportViewSet.as_view({'get': 'list'}), name='get_mock_drill_report'),
]