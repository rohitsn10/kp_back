def data_insert_into_row(current_row, parameters, sheet, border, center_alignment, Alignment):
    """
    Insert parameter data into Excel rows
    Returns the next available row number
    """
    start_row = current_row
    
    for param in parameters:
        # Sr. No. column
        sheet.cell(row=current_row, column=1).value = param["sr"]
        sheet.cell(row=current_row, column=1).alignment = center_alignment
        sheet.cell(row=current_row, column=1).border = border

        # Parameter name column
        sheet.cell(row=current_row, column=2).value = param["name"]
        sheet.cell(row=current_row, column=2).alignment = Alignment(horizontal='left', vertical='center')
        sheet.cell(row=current_row, column=2).border = border

        # Data columns (months) - 12 months from column C to N
        data = param.get("data", '')
        
        # Handle different data types
        if isinstance(data, list):
            # If data is a list, use it directly
            for idx, value in enumerate(data, start=3):
                if idx <= 14:  # Only up to column N (index 14)
                    cell = sheet.cell(row=current_row, column=idx)
                    cell.value = value if value is not None else ''
                    cell.alignment = center_alignment
                    cell.border = border
        else:
            # If data is empty string or other value, fill all 12 month columns with empty
            for col in range(3, 15):  # Columns C to N (3 to 14)
                cell = sheet.cell(row=current_row, column=col)
                cell.value = ''
                cell.alignment = center_alignment
                cell.border = border
        
        # FY-25 column (O) and Remarks column (P)
        sheet.cell(row=current_row, column=15).value = ''  # FY-25 (column O)
        sheet.cell(row=current_row, column=15).alignment = center_alignment
        sheet.cell(row=current_row, column=15).border = border
        
        sheet.cell(row=current_row, column=16).value = ''  # Remarks (column P)
        sheet.cell(row=current_row, column=16).alignment = center_alignment
        sheet.cell(row=current_row, column=16).border = border

        current_row += 1
    
    # Set row heights
    for row in range(start_row, current_row):
        sheet.row_dimensions[row].height = 25
    
    # Return the next available row
    return current_row
