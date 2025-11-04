from django.urls import path
from .views import LandReportAPIView

urlpatterns = [
    path("land_report/", LandReportAPIView.as_view(), name="land-report"),
]