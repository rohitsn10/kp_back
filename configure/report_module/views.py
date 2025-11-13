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
from .excel_operations.project.generate_ear_report import generate_ear_report
from .excel_operations.project.generate_dpr_project_execution_report import generate_dpr_project_execution_report
from .excel_operations.project.project_status_management_report import generate_project_status_management_report
from .excel_operations.project.project_hoto_summary_report import generate_hoto_summary_report
from .excel_operations.project.project_iar_report import generate_iar_report
from .excel_operations.project.project_delay_analysis_report import generate_project_delay_analysis_report
from .excel_operations.design.generate_design_mdl_report import generate_design_mdl_report
from .excel_operations.satutory_approval.generate_satutory_approval_report import generate_66kv_satutory_status_report
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
        

class EARFormatReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            response = generate_ear_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating EAR report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)

        

class DPRProjectExecutionReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_dpr_project_execution_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating DPR Project Execution report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)


class ProjectStatusManagementReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_project_status_management_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating Project Status Management report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        
class ProjectHotoSummaryReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_hoto_summary_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating HOTO Summary report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        
class ProjectIARReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_iar_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating IAR report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
        

class ProjectDelayAnalysisReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_project_delay_analysis_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating Project Delay Analysis report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)


class DesignMDLReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_design_mdl_report(request=request)
            if isinstance(response, Response):
                return response

        except Exception as e:
            logger.error(f"Error generating Design MDL report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)


class Generate66kvSatutoryStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            response = generate_66kv_satutory_status_report(request=request)
            if isinstance(response, Response):
                return response
            return response
        except Exception as e:
            logger.error(f"Error generating 66kV Statutory Approval report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)