from django.urls import path
from .views import LandReportAPIView, HSEMISReportAPIView, ProcurementTrackerReportAPIView

urlpatterns = [
    path("land_report/", LandReportAPIView.as_view(), name="land-report"),
    path("hse_mis_report/", HSEMISReportAPIView.as_view(), name="hse-mis-report"),
    path("scm_material_tracking_report/", ProcurementTrackerReportAPIView.as_view(), name="scm-material-tracking-report"),
]