from django.shortcuts import render
from user_profile.models import *
from quality_inspection.views import *
from rest_framework import viewsets
from rest_framework.response import Response
from quality_inspection.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class AddItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            item_name = request.data.get('item_name')
            item_category = request.data.get('item_category')
            item_number = request.data.get('item_number')
            dicipline = request.data.get('dicipline')

            items = ItemsProduct.objects.create(
                item_name=item_name,
                item_category=item_category,
                item_number=item_number,
                dicipline=dicipline
            )

            serializer = ItemsProductSerializer(items)
            return Response({"status": True, "message": "items created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class ActiveItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            item_id = request.data.get('item_id')
            item = ItemsProduct.objects.get(id=item_id)
            project_id = request.data.get('project_id')
            project = Project.objects.get(id=project_id)
            is_active = request.data.get('is_active', True)

            if is_active:
                if project not in item.project.all():
                    item.project.add(project)

                item.is_active = is_active
                item.save()
            else:
                if project in item.project.all():
                    item.project.remove(project)

                item.is_active = False
                item.save()

            serializer = ItemsProductSerializer(item)
            return Response({"status": True, "message": "items updated successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ProjectIdWiseItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            items = Project.objects.filter(id=project_id)
            serializer = ItemsProductSerializer(items, many=True)
            return Response({"status": True, "message": "items fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class UpdateItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            item_name = request.data.get('item_name')
            item_category = request.data.get('item_category')
            item_number = request.data.get('item_number')
            dicipline = request.data.get('dicipline')

            items = ItemsProduct.objects.filter(id=item_id).update(
                item_name=item_name,
                item_category=item_category,
                item_number=item_number,
                dicipline=dicipline
            )

            serializer = ItemsProductSerializer(items)
            return Response({"status": True, "message": "items updated successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            items = ItemsProduct.objects.filter(id=item_id).delete()
            return Response({"status": True, "message": "items deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class QualityInspectionDocumentUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QualityInspectionSerializer
    queryset = QualityInspection.objects.all()
 
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            project_id = data.get('project_id')
            item_id = data.get('item_id')
            vendor_id = data.get('vendor_id')
            remarks = data.get('remarks')

            quality_inspection = QualityInspection.objects.create(
                project_id=project_id,
                items_id=item_id,
                vendor_id=vendor_id,
                remarks=remarks,
            )

            upload_map = {
                'mqap_upload': (MQAPUpload, 'mqap_revision_number', 'mqap_revision_status'),
                'quality_dossier_upload': (QualityDossierUpload, 'quality_dossier_revision_number', 'quality_dossier_revision_status'),
                'drawing_upload': (DrawingUpload, 'drawing_revision_number', 'drawing_revision_status'),
                'data_sheet_upload': (DataSheetUpload, 'data_sheet_revision_number', 'data_sheet_revision_status'),
                'specification_upload': (SpecificationUpload, 'specification_revision_number', 'specification_revision_status'),
                'mdcc_upload': (MDCCUpload, 'mdcc_revision_number', 'mdcc_revision_status'),
            }

            for field, (model_class, rev_num_field, rev_status_field) in upload_map.items():
                uploads = request.data.getlist(field)
                for i in range(len(uploads)):
                    file_obj = request.FILES.getlist(field)[i]
                    rev_number = data.getlist(rev_num_field)[i]
                    rev_status = data.getlist(rev_status_field)[i]

                    doc_instance = model_class.objects.create(
                        file=file_obj,
                        **{rev_num_field: rev_number, rev_status_field: rev_status}
                    )
                    getattr(quality_inspection, field).add(doc_instance)

            serializer = QualityInspectionSerializer(quality_inspection, context={'request': request})
            return Response({"status": True, "message": "Documents uploaded successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class QualityInspectionDocumentListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QualityInspectionSerializer
    queryset = QualityInspection.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            quality_inspection = QualityInspection.objects.filter(items_id=item_id)
            serializer = QualityInspectionSerializer(quality_inspection, many=True)
            return Response({"status": True, "message": "Documents fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class CreateRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            project_id = data.get('project_id')
            rfi_activity = data.get('rfi_activity')
            rfi_number = data.get('rfi_number')
            rfi_classification = data.get('rfi_classification')
            rfi_other = data.get('rfi_other')
            epc_name = data.get('epc_name')
            offered_date = data.get('offered_date')
            block_number = data.get('block_number')
            table_number = data.get('table_number')
            activity_description = data.get('activity_description')
            hold_details = data.get('hold_details')
            location_name = data.get('location_name')
            construction_activity = data.get('construction_activity')

            quality_inspection = RFIFieldActivity.objects.create(
                project_id=project_id,
                rfi_activity=rfi_activity,
                rfi_number=rfi_number,
                rfi_classification=rfi_classification,
                rfi_other=rfi_other,
                epc_name=epc_name,
                offered_date=offered_date,
                block_number=block_number,
                table_number=table_number,
                activity_description=activity_description,
                hold_details=hold_details,
                location_name=location_name,
                construction_activity=construction_activity,
            )

            serializer = RFIFieldActivitySerializer(quality_inspection, context={'request': request})
            return Response({"status": True, "message": "RFI created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            rfi_field_activity = RFIFieldActivity.objects.filter(project=project_id)
            serializer = RFIFieldActivitySerializer(rfi_field_activity, many=True)
            return Response({"status": True, "message": "RFI fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class ElectricalGetRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            rfi_field_activity = RFIFieldActivity.objects.filter(project=project_id, rfi_activity='electrical')
            serializer = RFIFieldActivitySerializer(rfi_field_activity, many=True)
            return Response({"status": True, "message": "Electrical RFI fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class MechanicalGetRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            rfi_field_activity = RFIFieldActivity.objects.filter(project=project_id, rfi_activity='mechanical')
            serializer = RFIFieldActivitySerializer(rfi_field_activity, many=True)
            return Response({"status": True, "message": "Mechanical RFI fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class CivilGetRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            rfi_field_activity = RFIFieldActivity.objects.filter(project=project_id, rfi_activity='civil')
            serializer = RFIFieldActivitySerializer(rfi_field_activity, many=True)
            return Response({"status": True, "message": "Civil RFI fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    
class UpdateRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            data = request.data
            project_id = data.get('project_id')
            rfi_activity = data.get('rfi_activity')
            rfi_number = data.get('rfi_number')
            rfi_classification = data.get('rfi_classification')
            rfi_other = data.get('rfi_other')
            epc_name = data.get('epc_name')
            offered_date = data.get('offered_date')
            block_number = data.get('block_number')
            table_number = data.get('table_number')
            activity_description = data.get('activity_description')
            hold_details = data.get('hold_details')
            location_name = data.get('location_name')
            construction_activity = data.get('construction_activity')

            rfi = RFIFieldActivity.objects.get(id=rfi_id)

            rfi.project = project_id
            rfi.rfi_activity = rfi_activity
            rfi.rfi_number = rfi_number
            rfi.rfi_classification = rfi_classification
            rfi.rfi_other = rfi_other
            rfi.epc_name = epc_name
            rfi.offered_date = offered_date
            rfi.block_number = block_number
            rfi.table_number = table_number
            rfi.activity_description = activity_description
            rfi.hold_details = hold_details
            rfi.location_name = location_name
            rfi.construction_activity = construction_activity
            rfi.save()

            serializer = RFIFieldActivitySerializer(rfi, context={'request': request})
            return Response({"status": True, "message": "RFI updated successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            items = RFIFieldActivity.objects.filter(id=rfi_id).delete()
            return Response({"status": True, "message": "RFI deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class CreateRFIInspectionOutcomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionOutcomeSerializer
    queryset = InspectionOutcome.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            project_id = data.get('project_id')
            rfi_id = data.get('rfi_id')
            offered_time = data.get('offered_time')
            reaching_time = data.get('reaching_time')
            inspection_start_time = data.get('inspection_start_time')
            inspection_end_time = data.get('inspection_end_time')
            observation = data.get('observation', [])
            disposition_status = data.get('disposition_status')
            actions = data.get('actions')
            responsibility = data.get('responsibility')
            timelines = data.get('timelines')
            remarks = data.get('remarks')

            rfi = RFIFieldActivity.objects.get(id=rfi_id)

            quality_inspection = InspectionOutcome.objects.create(
                project_id=project_id,
                rfi_field_activity=rfi,
                offered_time=offered_time,
                reaching_time=reaching_time,
                inspection_start_time=inspection_start_time,
                inspection_end_time=inspection_end_time,
                disposition_status=disposition_status,
                actions=actions,
                responsibility=responsibility,
                timelines=timelines,
                remarks=remarks
            )

            for observation_text in observation:
                observation_instance = Observation.objects.create(observation=observation_text)
                quality_inspection.observation.add(observation_instance)

            serializer = InspectionOutcomeSerializer(quality_inspection, context={'request': request})
            return Response({"status": True, "message": "RFI Inspection Outcome created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class GetRFIInspectionOutcomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionOutcomeSerializer
    queryset = InspectionOutcome.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            rfi_inspection_outcome = InspectionOutcome.objects.filter(rfi_field_activity=rfi_id)
            serializer = InspectionOutcomeSerializer(rfi_inspection_outcome, many=True)
            return Response({"status": True, "message": "RFI Inspection Outcome fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class UpdateRFIInspectionOutcomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionOutcomeSerializer
    queryset = InspectionOutcome.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            data = request.data
            project_id = data.get('project_id')
            offered_time = data.get('offered_time')
            reaching_time = data.get('reaching_time')
            inspection_start_time = data.get('inspection_start_time')
            inspection_end_time = data.get('inspection_end_time')
            observation = data.get('observation', [])
            disposition_status = data.get('disposition_status')
            actions = data.get('actions')
            responsibility = data.get('responsibility')
            timelines = data.get('timelines')
            remarks = data.get('remarks')

            quality_inspection = InspectionOutcome.objects.get(id=rfi_id)

            quality_inspection.project = project_id
            quality_inspection.offered_time = offered_time
            quality_inspection.reaching_time = reaching_time
            quality_inspection.inspection_start_time = inspection_start_time
            quality_inspection.inspection_end_time = inspection_end_time
            quality_inspection.disposition_status = disposition_status
            quality_inspection.actions = actions
            quality_inspection.responsibility = responsibility
            quality_inspection.timelines = timelines
            quality_inspection.remarks = remarks
            quality_inspection.save()

            quality_inspection.observation.clear()

            for observation_text in observation:
                observation_instance = Observation.objects.create(observation=observation_text)
                quality_inspection.observation.add(observation_instance)

            serializer = InspectionOutcomeSerializer(quality_inspection, context={'request': request})
            return Response({"status": True, "message": "RFI Inspection Outcome updated successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    
class CreateFilesUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionOutcomeDocumentSerializer
    queryset = InspectionOutcomeDocument.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            rfi_id = data.get('rfi_id')
            files = request.FILES.getlist('files')

            inspection_outcome = InspectionOutcome.objects.get(id=rfi_id)

            uploaded_documents = []

            for file_obj in files:
                doc = InspectionOutcomeDocument.objects.create(
                    inspection_outcome=inspection_outcome,
                    document=file_obj
                )
                uploaded_documents.append(doc)
                inspection_outcome.documents.add(doc)

            serializer = InspectionOutcomeDocumentSerializer(uploaded_documents, many=True, context={'request': request})
            return Response({"status": True, "message": "Files uploaded successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetFilesUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InspectionOutcomeDocumentSerializer
    queryset = InspectionOutcomeDocument.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            files = InspectionOutcomeDocument.objects.filter(inspection_outcome=rfi_id)
            serializer = InspectionOutcomeDocumentSerializer(files, many=True)
            return Response({"status": True, "message": "Files fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        



# class RFIExcelGenerateViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = RFIFieldActivity.objects.all()
#     serializer_class = RFIFieldActivitySerializer

#     def list(self, request, *args, **kwargs):
#         try:
#             status_id = request.query_params.get('status_id', None)
#             if not status_id:
#                 return Response({"status": False, "message": "status_id parameter is required", "data": []})
#             user = self.request.user

#             if user.groups.filter(name='QA').exists() or user.groups.filter(name='Doc Admin').exists():
#                 queryset = PrintRequest.objects.all().order_by('-created_at')

#             elif status_id == 'all':
#                 # If status_id is "all", fetch all data for the current user
#                 queryset = PrintRequest.objects.filter(user=user).order_by('-created_at')

#             else:
#                 try:
#                     dynamic_status = DynamicStatus.objects.get(id=status_id)
#                 except DynamicStatus.DoesNotExist:
#                     return Response({"status": False, "message": "DynamicStatus with the given ID does not exist.", "data": []})

#                 queryset = PrintRequest.objects.filter(user=user, print_request_status=dynamic_status).order_by('-created_at')

#             if not queryset:
#                 return Response({"status": False, "message": "No data available for the selected status.", "data": []})

#             wb = openpyxl.Workbook()
#             ws = wb.active
#             ws.title = "Print Requests"

#             headers = [
#                 'Data Number', 'User','SOP Document Number','SOP Document Title', 'No of Prints', 'Retrieval Numbers', 'Issue Type', 'Reason for Print',
#                 'Print Request Status', 'Created At', 'Printer', 'Master Copy Users', 'Other Users', 'Reminder Sent'
#             ]

#             for col_num, header in enumerate(headers, 1):
#                 col_letter = get_column_letter(col_num)
#                 ws[f'{col_letter}1'] = header

#             for row_num, (index, print_request) in enumerate(enumerate(queryset, start=1), 2):
#                 ws[f'A{row_num}'] = index
#                 ws[f'B{row_num}'] = print_request.user.username  # User's username
#                 ws[f'C{row_num}'] = print_request.sop_document_id.document_number if print_request.sop_document_id else ""
#                 ws[f'D{row_num}'] = print_request.sop_document_id.document_title if print_request.sop_document_id else ""
#                 ws[f'E{row_num}'] = print_request.no_of_print
#                 ws[f'F{row_num}'] = ", ".join([str(num) for num in print_request.approvals.all().values_list('retrival_numbers__retrival_number', flat=True) if num])
#                 ws[f'G{row_num}'] = print_request.issue_type
#                 ws[f'H{row_num}'] = print_request.reason_for_print
#                 status = print_request.print_request_status.status if print_request.print_request_status else ""
#                 ws[f'I{row_num}'] = status.capitalize() if status else ""
#                 ws[f'J{row_num}'] = print_request.created_at.strftime('%d-%m-%Y')
#                 ws[f'K{row_num}'] = print_request.printer.printer_name if print_request.printer else ""
#                 ws[f'L{row_num}'] = ", ".join([user.username for user in print_request.master_copy_user.all()])
#                 ws[f'M{row_num}'] = ", ".join([user.username for user in print_request.other_user.all()])
#                 ws[f'N{row_num}'] = "Yes" if print_request.reminder_sent else "No"

#             for col_num in range(1, len(headers) + 1):
#                 col_letter = get_column_letter(col_num)
#                 max_length = 0
#                 for row in ws.iter_rows(min_col=col_num, max_col=col_num):
#                     for cell in row:
#                         try:
#                             if len(str(cell.value)) > max_length:
#                                 max_length = len(cell.value)
#                         except:
#                             pass
#                 adjusted_width = (max_length + 2)
#                 ws.column_dimensions[col_letter].width = adjusted_width
#             timestamp = time.strftime("%d_%m_%Y_%H_%M_%S")
#             filename = f"print_request_report_{timestamp}.xlsx"

#             file_path = os.path.join(settings.MEDIA_ROOT, 'print_request_excel_sheet', filename)

#             folder_path = os.path.dirname(file_path)
#             if not os.path.exists(folder_path):
#                 os.makedirs(folder_path)

#             file_stream = BytesIO()
#             wb.save(file_stream)
#             file_stream.seek(0)

#             with open(file_path, 'wb') as f:
#                 f.write(file_stream.read())
#             base_url = request.build_absolute_uri('/')
#             file_url = base_url + 'media/print_request_excel_sheet/' + filename

#             return Response({"status": True,"message": "Excel report generated successfully.","data": file_url})

#         except Exception as e:
#             return Response({"status": False, "message": str(e), "data": []})