from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
from .excel_operations.land.generate_land_report import generate_land_report
from .excel_operations.hse_mis.generate_hse_mis_report import generate_hse_mis_report
from .excel_operations.quality.generate_quality_report import generate_quality_report
from .excel_operations.scm.generate_scm_material_tracking_report import generate_scm_material_tracking_report
class LandReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            file_url = generate_land_report(request=request)
            return Response({"file_url": file_url}, status=200)
            
        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        



class HSEMISReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            file_url = generate_hse_mis_report(request=request)
            return Response({"file_url": file_url}, status=200)

        except Exception as e:
            logger.error(f"Error generating HSE MIS report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        
class ProcurementTrackerReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            file_url = generate_scm_material_tracking_report(request=request)
            return Response({"file_url": file_url}, status=200)

        except Exception as e:
            logger.error(f"Error generating SCM Material Tracking report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        
class CheckQualityReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_quality_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating Quality report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        
