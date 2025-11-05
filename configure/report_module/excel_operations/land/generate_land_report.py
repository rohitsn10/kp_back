
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import openpyxl
from openpyxl.styles import Font
from land_module.models import LandBankMaster
import logging
from django.conf import settings
import os
from datetime import datetime
logger = logging.getLogger(__name__)


def generate_land_report(request):
     # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Land Report"

    # Define the mapping of sheet column names to database column names
    column_mapping = {
        "Sn": None,  # Serial number is generated dynamically
        "Land Bank Name": "land_name",
        "Area- Acre": "area_acres",
        "Survey No": "survey_number",
        "Village": "village_name",
        "Taluka": "taluka_tahshil_name",
        "District": "district_name",
        "State": "state",  # If this field doesn't exist, it will be handled as 'Missing'
        "Land Lease Date": "lease_deed_date",
        "Lease Start": "lease_deed_date",
        "Lease End": "lease_end",
        "Leaser": "leaser",
        "Leasee": "leasee",
        "Lease Rate/Acre": "lease_rate_per_acre",
        "TSR Status": "tsr",
        "NA Status": "na_status",
        "DILR Status": "dilr_status",
        "Land Handover date": "land_handover_date",
        "ROW if any": "row_if_any",
        "PSS": "pss",
        "GSS": "propose_gss_number",
        "Connectivity Voltage": "connectivity_voltage",
        "Allocated Project Name": "allocated_project_name",
    }

    # Add headers to the sheet
    headers = list(column_mapping.keys())
    bold_font = Font(bold=True)  # Define a bold font
    sheet.append(headers)

    # Apply bold font to the header row
    for cell in sheet[1]:  # Access the first row (header row)
        cell.font = bold_font

    # Get all field names from the model
    model_fields = {field.name for field in LandBankMaster._meta.get_fields()}
    logger.debug(f"Available model fields: {model_fields}")

    # Filter out only the columns that exist in the database
    valid_db_columns = [col for col in column_mapping.values() 
                        if col is not None and col in model_fields]
    
    # Track which columns are missing from the database
    missing_columns = {sheet_col: db_col for sheet_col, db_col in column_mapping.items() 
                        if db_col is not None and db_col not in model_fields}
    
    if missing_columns:
        logger.warning(f"Missing database columns: {missing_columns}")

    logger.debug(f"Valid database columns: {valid_db_columns}")

    try:
        # Only query fields that actually exist in the database
        land_data = LandBankMaster.objects.all().values(*valid_db_columns)
        logger.debug(f"Fetched {len(land_data)} records")
    except Exception as query_error:
        logger.error(f"Error fetching data: {query_error}")
        return Response({"error": f"Error fetching data: {query_error}"}, status=500)

    # Add data rows to the sheet
    for index, row in enumerate(land_data, start=1):
        row_data = []
        for col_name, db_field in column_mapping.items():
            if col_name == "Sn":
                # Add serial number for "Sn"
                row_data.append(index)
            elif db_field is None:
                # If no mapping is defined, leave empty
                row_data.append("")
            elif db_field not in model_fields:
                # If the field doesn't exist in the model, mark as missing
                row_data.append("N/A")
            else:
                # Add the value from the database or empty string if None
                value = row.get(db_field)
                row_data.append(value if value is not None else "")
        
        sheet.append(row_data)

    # If no data was found, add a row indicating this
    if not land_data:
        empty_row = ["No data available"] + [""] * (len(headers) - 1)
        sheet.append(empty_row)

    
    # Define the file path to save the report
    reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)  # Ensure the directory exists
    datetime_str= datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(reports_dir, f"land_report_{datetime_str}.xlsx")

    # Save the workbook to the file path
    workbook.save(file_path)

    # Construct the file URL
    file_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/land_report_{datetime_str}.xlsx")
    return file_url
