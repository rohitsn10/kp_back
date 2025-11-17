from django.urls import path

from .views import (EARFormatReportAPIView, LandReportAPIView,
                    HSEMISReportAPIView, ProcurementTrackerReportAPIView, CheckQualityReportAPIView, DPRProjectExecutionReportAPIView,
                    ProjectStatusManagementReportAPIView, ProjectHotoSummaryReportAPIView,ProjectIARReportAPIView,
                    ProjectDelayAnalysisReportAPIView,DesignMDLReportAPIView,Generate66kvSatutoryStatus)

urlpatterns = [
    path("land_report/", LandReportAPIView.as_view(), name="land-report"),
    path("hse_mis_report/", HSEMISReportAPIView.as_view(), name="hse-mis-report"),
    path("scm_material_tracking_report/", ProcurementTrackerReportAPIView.as_view(), name="scm-material-tracking-report"),
    path("check_quality_report/", CheckQualityReportAPIView.as_view(), name="check-quality-report"),
    path("design_mdl_report/", DesignMDLReportAPIView.as_view(), name="design-mdl-report"),
    
    #Projects
    path("project_ear_report/", EARFormatReportAPIView.as_view(), name="ear-report"),
    path("project_dpr_project_execution_report/", DPRProjectExecutionReportAPIView.as_view(), name="dpr-project-execution-report"),
    path("project_status_management_report/", ProjectStatusManagementReportAPIView.as_view(), name="project-status-management-report"),
    path("project_hoto_summary_report/", ProjectHotoSummaryReportAPIView.as_view(), name="project-hoto-summary-report"),
    path("project_iar_report/", ProjectIARReportAPIView.as_view(), name="project-iar-report"),
    path("project_delay_analysis_report/", ProjectDelayAnalysisReportAPIView.as_view(), name="project-delay-analysis-report"),
    path("project_payment_status_report/",Generate66kvSatutoryStatus.as_view(),name="project-payment-status-report"),
    path("project_budget_vs_actual_cost_tracking_report/",Generate66kvSatutoryStatus.as_view(),name="project-budget-vs-actual-cost-tracking-report"),

    #Satutory Approval Reports
    path("satutory_approval_66kv_report/",Generate66kvSatutoryStatus.as_view(),name="satutory-approval-66kv-report"),

]