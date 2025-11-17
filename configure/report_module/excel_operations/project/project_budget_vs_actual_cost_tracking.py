from .project_budget_cost_tracking.cil import generate_cil_report
from .project_budget_cost_tracking.aditya_ultra import generate_aditya_ultra_report
import logging
from rest_framework.response import Response
from django.conf import settings
import os
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_budget_vs_actual_cost_tracking_report(request):
        try:
            response = generate_cil_report(request)
            workbook = response.data.get('workbook')
            workbook=generate_aditya_ultra_report(workbook)
             # Define the file path to save the report
            reports_dir = os.path.join(settings.MEDIA_ROOT, "reports/project/")
            os.makedirs(reports_dir, exist_ok=True)  # Ensure the directory exists
            datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(reports_dir, f"project_budget_vs_actual_cost_tracking_report_{datetime_str}.xlsx")

            # Save the workbook to the file path
            workbook.save(file_path)

            # Construct the file URL
            file_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/project/project_budget_vs_actual_cost_tracking_report_{datetime_str}.xlsx")
            return Response({"status": True, "message": "Project Budget vs Actual Cost Tracking report generated successfully", "file_url": file_url}, status=200)




        except Exception as e:
            logger.error(f"Error generating Budget vs Actual Cost Tracking report: {e}", exc_info=True)
            return Response({"error": str(e)}, status=500)
