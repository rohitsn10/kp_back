

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from rest_framework.response import Response
import os
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_hse_mis_report(request):
    try:
        # Create workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "HSE MIS Report"

        # Define styles
        header_fill = PatternFill(start_color="92D050", end_color="92D050", fill_type="solid")
        border = Border(
            left=Side(style='thin', color='000000'),
            right=Side(style='thin', color='000000'),
            top=Side(style='thin', color='000000'),
            bottom=Side(style='thin', color='000000')
        )
        center_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        bold_font = Font(bold=True)

        # Set column widths
        sheet.column_dimensions['A'].width = 10  # Sr. No.
        sheet.column_dimensions['B'].width = 50  # Leading Parameters
        for col in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']:
            sheet.column_dimensions[col].width = 10  # Month columns

        # Row 3: Sr. No. and Site Name
        sheet.merge_cells('A3:A3')
        sheet['A3'] = 'Sr. No.'
        sheet['A3'].font = bold_font
        sheet['A3'].alignment = center_alignment
        sheet['A3'].border = border

        sheet.merge_cells('B3:B3')
        sheet['B3'] = 'Site Name:-'
        sheet['B3'].font = bold_font
        sheet['B3'].alignment = Alignment(horizontal='left', vertical='center')
        sheet['B3'].border = border

        # Row 4: Leading Parameters header with months
        sheet.merge_cells('A4:B4')
        sheet['A4'] = 'Leading Parameters'
        sheet['A4'].font = bold_font
        sheet['A4'].fill = header_fill
        sheet['A4'].alignment = center_alignment
        sheet['A4'].border = border

        # Month headers
        months = ['Apr-24', 'May-24', 'Jun-24', 'Jul-24', 'Aug-24', 'Sep-24', 
                    'Oct-24', 'Nov-24', 'Dec-24', 'Jan-25', 'Feb-25', 'Mar-25']
        
        for idx, month in enumerate(months, start=3):  # Start from column C (index 3)
            cell = sheet.cell(row=4, column=idx)
            cell.value = month
            cell.font = bold_font
            cell.fill = header_fill
            cell.alignment = center_alignment
            cell.border = border

        # Define the parameters with their data
        parameters = [
            {"sr": 1, "name": "No. of Manday's Worked", "data": [0] * 12},
            {"sr": 2, "name": "No. of Employee Worked (On Roll)", "data": [0] * 12},
            {"sr": 3, "name": "No. of Employee Worked ( Off Roll+ Contractual Manpower)", "data": [0] * 12},
            {"sr": 4, "name": "No. of Total Employee Worked", "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
            {"sr": 5, "name": "Manhours Worked Employee(On Roll)", "data": [0] * 12},
            {"sr": 6, "name": "Manhours Employee Worked (Off Roll+ Contractor Workers)", "data": [0] * 12},
        ]

        # Add parameter rows
        current_row = 5
        for param in parameters:
            # Sr. No. column
            sheet.cell(row=current_row, column=1).value = param["sr"]
            sheet.cell(row=current_row, column=1).alignment = center_alignment
            sheet.cell(row=current_row, column=1).border = border

            # Parameter name column
            sheet.cell(row=current_row, column=2).value = param["name"]
            sheet.cell(row=current_row, column=2).alignment = Alignment(horizontal='left', vertical='center')
            sheet.cell(row=current_row, column=2).border = border

            # Data columns (months)
            for idx, value in enumerate(param["data"], start=3):
                cell = sheet.cell(row=current_row, column=idx)
                cell.value = value
                cell.alignment = center_alignment
                cell.border = border

            current_row += 1

        # Set row heights for better visibility
        for row in range(3, current_row):
            sheet.row_dimensions[row].height = 25

        # Define the file path to save the report
        reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)  # Ensure the directory exists
        datetime_str= datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(reports_dir, f"hse_mis_report_{datetime_str}.xlsx")

        workbook.save(file_path)

        file_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/hse_mis_report_{datetime_str}.xlsx")

        return file_url

    except Exception as e:
        logger.error(f"Error generating HSE MIS report: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)