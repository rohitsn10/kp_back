from django.shortcuts import render

# Create your views here.
import openpyxl
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from land_module.models import LandBankMaster  # Assuming this is the model for land_module

class LandReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Create an Excel workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Land Report"

        # Add headers to the sheet
        headers = ["ID", "Land Name", "Location", "Area", "Status", "Created At"]
        sheet.append(headers)

        # Fetch data from the LandBankMaster model
        land_data = LandBankMaster.objects.all().values_list(
            "id", "land_name", "location", "area", "status", "created_at"
        )

        # Add data rows to the sheet
        for row in land_data:
            sheet.append(row)

        # Save the workbook to an in-memory buffer
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="land_report.xlsx"'
        workbook.save(response)

        return response