import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.drawing.image import Image
from django.http import HttpResponse
from rest_framework.response import Response
import logging
import os
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_project_status_management_report(request):
    try:
        pass
        # Create workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Project Status Management"

        # Define the file path to save the report
        reports_dir = os.path.join(settings.MEDIA_ROOT, "reports/project/")
        os.makedirs(reports_dir, exist_ok=True)  # Ensure the directory exists
        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(reports_dir, f"project_status_management_report_{datetime_str}.xlsx")

        # Save the workbook to the file path
        workbook.save(file_path)

        # Construct the file URL
        file_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/project/project_status_management_report_{datetime_str}.xlsx")
        return Response({"status": True, "message": "Project Status Management report generated successfully", "file_url": file_url}, status=200)

    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)