from django.shortcuts import render
from user_profile.models import *
from quality_inspection.views import *
from rest_framework import viewsets
from rest_framework.response import Response
from quality_inspection.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
import os
import time


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
            item_ids = request.data.get('item_id', [])
            if not isinstance(item_ids, list):
                item_ids = [item_ids]

            project_id = request.data.get('project_id')
            is_active = request.data.get('is_active', True)

            project = Project.objects.get(id=project_id)
            updated_items = []

            for item_id in item_ids:
                item = ItemsProduct.objects.get(id=item_id)

                if is_active:
                    if project not in item.project.all():
                        item.project.add(project)
                    item.is_active = True
                else:
                    if project in item.project.all():
                        item.project.remove(project)
                    if item.project.count() == 0:
                        item.is_active = False

                item.save()
                updated_items.append(ItemsProductSerializer(item).data)

            return Response({"status": True, "message": "Items updated successfully", "data": updated_items})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

        

class ProjectIdWiseItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            items = ItemsProduct.objects.filter(project__id=project_id)
            serializer = ItemsProductSerializer(items, many=True, context={'project_id': project_id})
            return Response({"status": True, "message": "items fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ListAllItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemsProductSerializer
    queryset = ItemsProduct.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            items = ItemsProduct.objects.all()
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
            project_id = request.data.get('project_id')
            item_id = kwargs.get('item_id')
            item_name = request.data.get('item_name')
            item_category = request.data.get('item_category')
            item_number = request.data.get('item_number')
            dicipline = request.data.get('dicipline')

            items_ins = ItemsProduct.objects.get(id=item_id, project__id=project_id)
            if item_name:
                items_ins.item_name = item_name
            if item_category:
                items_ins.item_category = item_category
            if item_number:
                items_ins.item_number = item_number
            if dicipline:
                items_ins.dicipline = dicipline

            items_ins.save()

            serializer = ItemsProductSerializer(items_ins)
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
        


class AddVendorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            item_id = request.data.get('item_id')
            project_id = request.data.get('project_id')
            vendor_name = request.data.get('vendor_name')
            file = request.FILES.getlist('file')

            item = ItemsProduct.objects.get(id=item_id)
            project = Project.objects.get(id=project_id)
            vendor = Vendor.objects.create(
                items=item,
                project=project,
                vendor_name=vendor_name,
            )

            for file_obj in file:
                vendor_document = VendorFileUpload.objects.create(file=file_obj)
                vendor.vendor_file.add(vendor_document)

            serializer = VendorSerializer(vendor)
            return Response({"status": True, "message": "Vendor created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ItemsProjectIdWiseVendorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            project_id = kwargs.get('project_id')
            vendor = Vendor.objects.filter(items=item_id, project=project_id)
            serializer = VendorSerializer(vendor, many=True)
            return Response({"status": True, "message": "Vendor fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class VerifyVendorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            vendor_id = kwargs.get('vendor_id')
            is_verified = request.data.get('is_verified', True)

            vendor = Vendor.objects.get(id=vendor_id)
            vendor.is_verified = is_verified
            vendor.save()

            serializer = VendorSerializer(vendor)
            return Response({"status": True, "message": "Vendor updated successfully", "data": serializer.data})
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
            remarks = data.get('remarks')

            quality_inspection, created = QualityInspection.objects.get_or_create(
                project_id=project_id,
                items_id=item_id,
                defaults={'remarks': remarks}
            )

            if not created and remarks:
                quality_inspection.remarks = remarks
                quality_inspection.save()

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
                files = request.FILES.getlist(field)

                for i in range(len(uploads)):
                    file_obj = files[i]
                    rev_number = data.getlist(rev_num_field)[i]
                    rev_status = data.getlist(rev_status_field)[i]

                    existing_docs = model_class.objects.filter(
                        file=file_obj,
                        **{rev_num_field: rev_number, rev_status_field: rev_status}
                    )
                    if existing_docs.exists():
                        doc_instance = existing_docs.first()
                    else:
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
            project_id = kwargs.get('project_id')
            quality_inspection = QualityInspection.objects.filter(items=item_id, project=project_id)
            serializer = QualityInspectionSerializer(quality_inspection, many=True)
            return Response({"status": True, "message": "Documents fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    
class CreateQualityInspectionObservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ObservationReportSerializer
    queryset = ObservationReport.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user
            project_id = data.get('project_id')
            # quality_inspection_id = data.get('quality_inspection_id')
            items_id = data.get('items_id')
            observation_title = data.get('observation_title')
            observation_status = data.get('observation_status')
            observation_text_report = data.get('observation_text_report')
            observation_report_document = request.FILES.getlist('observation_report_document')

            project = Project.objects.get(id=project_id)
            items = ItemsProduct.objects.get(id=items_id)
            # quality_inspection = QualityInspection.objects.get(id=quality_inspection_id)

            observation_report = ObservationReport.objects.create(
                project=project,
                # quality_inspection=quality_inspection,
                items=items,
                observation_title=observation_title,
                observation_status=observation_status,
                observation_text_report=observation_text_report,
                created_by=user,
            )

            for file_obj in observation_report_document:
                doc_instance = ObservationReportDocument.objects.create(file=file_obj)
                observation_report.observation_report_document.add(doc_instance)

            serializer = ObservationReportSerializer(observation_report, context={'request': request})
            return Response({"status": True, "message": "Observation report created successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class GetQualityInspectionObservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ObservationReportSerializer
    queryset = ObservationReport.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            project_id = kwargs.get('project_id')
            observation_report = ObservationReport.objects.filter(items=item_id,project=project_id)
            serializer = ObservationReportSerializer(observation_report, many=True)
            return Response({"status": True, "message": "Observation report fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class SupplyMDCCGeneratePDFViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # item_id = kwargs.get('item_id')
            # item = QualityInspection.objects.get(items=item_id)
            project_id = request.data.get('project_id')
            date = request.data.get('date')
            project_ins = Project.objects.get(id=project_id)
            project = project_ins.project_name if project_ins else None

            context = {
                'project': project,
                'date': date,
                'refNo': request.data.get('refNo', ''),
                'to': request.data.get('to', ''),
                'supplierAddress': request.data.get('supplierAddress', ''),
                'inspectionPlace': request.data.get('inspectionPlace', ''),
                'materialDescription': request.data.get('materialDescription', ''),
                'qap': request.data.get('qap', ''),
                'drawingNo': request.data.get('drawingNo', ''),
                'standard': request.data.get('standard', ''),
                'tpiRequired': request.data.get('tpiRequired', ''),
                'tpiConducted': request.data.get('tpiConducted', ''),
                'tpiReportAttached': request.data.get('tpiReportAttached', ''),
                'tpiDetails': request.data.get('tpiDetails', ''),
                'tpiRecommendation': request.data.get('tpiRecommendation', ''),
                'internalRequired': request.data.get('internalRequired', ''),
                'internalConducted': request.data.get('internalConducted', ''),
                'internalReportAttached': request.data.get('internalReportAttached', ''),
                'internalInspectorDetails': request.data.get('internalInspectorDetails', ''),
                'internalRecommendation': request.data.get('internalRecommendation', ''),
                'quantityOffered': request.data.get('quantityOffered', ''),
                'unitOffered': request.data.get('unitOffered', ''),
                'quantityCleared': request.data.get('quantityCleared', ''),
                'unitCleared': request.data.get('unitCleared', ''),
                'conditions': request.data.get('conditions', ''),
                'comments': request.data.get('comments', ''),
                'annexures': request.data.get('annexures', ''),
                'reviewedBy': request.data.get('reviewedBy', ''),
                'approvedBy': request.data.get('approvedBy', ''),
            }

            template = get_template('mdcc_html_template.html')
            html = template.render(context)
            # print(html)

            timestamp = int(time.time())
            filename = f"mdcc_html_template_report_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'mdcc_html_template_reports', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(file_path)

            file_url = f"{settings.MEDIA_URL}mdcc_html_template_reports/{filename}"
            full_url = f"{request.scheme}://{request.get_host()}{file_url}"
            return Response({"status": True, "message": "PDF generated successfully", "data": full_url})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": ""})



class SupplyInspectionCallPDFViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # item_id = kwargs.get('item_id')
            # item = QualityInspection.objects.get(items=item_id)
            project_id = request.data.get('project_id')
            date = request.data.get('date')
            ic_number = request.data.get('ic_number')
            item_description = request.data.get('item_description')
            name_address_supplier = request.data.get('name_address_supplier')
            place_inspection = request.data.get('place_inspection')
            contact_person = request.data.get('contact_person')
            date_time_inspection = request.data.get('date_time_inspection')
            purchase_order_number_date = request.data.get('purchase_order_number_date')
            quantity_ordered = request.data.get('quantity_ordered')
            quantity_released_till_date = request.data.get('quantity_released_till_date')
            quantity_balance = request.data.get('quantity_balance')
            quantity_offered_for_inspection = request.data.get('quantity_offered_for_inspection')
            item_category = request.data.get('item_category')
            details_num_of_approved_drawings = request.data.get('details_num_of_approved_drawings')
            any_others = request.data.get('any_others')
            raised_by_name = request.data.get('raised_by_name')
            supplier_name = request.data.get('supplier_name')
            epcc_name = request.data.get('epcc_name')
            project_ins = Project.objects.get(id=project_id)
            project = project_ins.project_name if project_ins else None

            context = {
                'project': project,
                'date': date,
                'ic_number': ic_number,
                'item_description': item_description,
                'name_address_supplier': name_address_supplier,
                'place_inspection': place_inspection,
                'contact_person': contact_person,
                'date_time_inspection': date_time_inspection,
                'purchase_order_number_date': purchase_order_number_date,
                'quantity_ordered': quantity_ordered,
                'quantity_released_till_date': quantity_released_till_date,
                'quantity_balance': quantity_balance,
                'quantity_offered_for_inspection': quantity_offered_for_inspection,
                'item_category': item_category,
                'details_num_of_approved_drawings': details_num_of_approved_drawings,
                'any_others': any_others,
                'raised_by_name': raised_by_name,
                'supplier_name': supplier_name,
                'epcc_name': epcc_name,
            }

            template = get_template('inspection.html')
            html = template.render(context)
            # print(html)

            timestamp = int(time.time())
            filename = f"inspection_call_report_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'inspection_call_reports', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(file_path)

            file_url = f"{settings.MEDIA_URL}inspection_call_reports/{filename}"
            full_url = f"{request.scheme}://{request.get_host()}{file_url}"
            return Response({"status": True, "message": "PDF generated successfully", "data": full_url})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": ""})


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
            offered_time = data.get('offered_time')
            reaching_time = data.get('reaching_time')
            inspection_start_time = data.get('inspection_start_time')
            inspection_end_time = data.get('inspection_end_time')
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
                offered_time=offered_time,
                reaching_time=reaching_time,
                inspection_start_time=inspection_start_time,
                inspection_end_time=inspection_end_time,
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
        

from django.db.models import Count
class CountAllRFIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RFIFieldActivitySerializer
    queryset = RFIFieldActivity.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')

            # Count RFIs by activity type
            rfi_queryset = RFIFieldActivity.objects.filter(project=project_id)
            rfi_counts = rfi_queryset.values('rfi_activity').annotate(total=Count('id'))

            rfi_result = {'mechanical': 0, 'electrical': 0, 'civil': 0}
            for item in rfi_counts:
                if item['rfi_activity']:
                    rfi_result[item['rfi_activity']] = item['total']

            # Disposition statuses to track
            disposition_statuses = [
                'Approved with comments',
                'Hold',
                'Reject',
                'Use-As-Is/Deviate',
                'Rework',
                'Sort',
                'Released'
            ]

            # Initialize nested outcome result
            outcome_result = {
                'mechanical': {status: 0 for status in disposition_statuses},
                'electrical': {status: 0 for status in disposition_statuses},
                'civil': {status: 0 for status in disposition_statuses},
            }

            # Filter InspectionOutcome by project
            outcome_queryset = InspectionOutcome.objects.filter(project=project_id).select_related('rfi_field_activity')

            # Count disposition_status grouped by rfi_activity
            outcome_data = outcome_queryset.values('rfi_field_activity__rfi_activity', 'disposition_status') \
                                           .annotate(total=Count('id'))

            for item in outcome_data:
                activity = item['rfi_field_activity__rfi_activity']
                status = item['disposition_status']
                if activity in outcome_result and status in disposition_statuses:
                    outcome_result[activity][status] += item['total']

            return Response({
                "status": True,
                "message": "RFI and outcome counts fetched successfully",
                "data": {
                    "rfi_counts_by_activity": rfi_result,
                    "outcome_counts_by_activity_and_status": outcome_result
                }
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": {}
            })
        
    
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

            inspection_outcome = RFIFieldActivity.objects.get(id=rfi_id)

            uploaded_documents = []

            for file_obj in files:
                doc = InspectionOutcomeDocument.objects.create(
                    rfi=inspection_outcome,
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
            files = InspectionOutcomeDocument.objects.filter(rfi=rfi_id)
            serializer = InspectionOutcomeDocumentSerializer(files, many=True)
            return Response({"status": True, "message": "Files fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class RFIReportPDFViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            rfi_id = kwargs.get('rfi_id')
            rfi = RFIFieldActivity.objects.get(id=rfi_id)
            project = rfi.project.project_name if rfi.project else None
            rfi_activity = rfi.rfi_activity if rfi.rfi_activity else None
            rfi_number = rfi.rfi_number if rfi.rfi_number else None
            rfi_classification = rfi.rfi_classification if rfi.rfi_classification else None
            epc_name = rfi.epc_name if rfi.epc_name else None
            offered_date = rfi.offered_date if rfi.offered_date else None
            block_number = rfi.block_number if rfi.block_number else None
            table_number = rfi.table_number if rfi.table_number else None
            activity_description = rfi.activity_description if rfi.activity_description else None
            hold_details = rfi.hold_details if rfi.hold_details else None
            location_name = rfi.location_name if rfi.location_name else None
            construction_activity = rfi.construction_activity if rfi.construction_activity else None

            context = {
                'project': project,
                'rfi_activity': rfi_activity,
                'rfi_number': rfi_number,
                'rfi_classification': rfi_classification,
                'epc_name': epc_name,
                'offered_date': offered_date,
                'block_number': block_number,
                'table_number': table_number,
                'activity_description': activity_description,
                'hold_details': hold_details,
                'location_name': location_name,
                'construction_activity': construction_activity,
            }

            template = get_template('rfi.html')
            html = template.render(context)
            # print(html)

            timestamp = int(time.time())
            filename = f"rfi_report_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'rfi_reports', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(file_path)

            file_url = f"{settings.MEDIA_URL}rfi_reports/{filename}"
            full_url = f"{request.scheme}://{request.get_host()}{file_url}"
            return Response({"status": True, "message": "PDF generated successfully", "data": full_url})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": ""})
        


class CategoryWisePDFViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            project_id = request.data.get('project_id')
            project = Project.objects.get(id=project_id)
            project_name = request.data.get('project_name')
            doc_no = request.data.get('doc_no')
            customer = request.data.get('customer')
            loa_no = request.data.get('loa_no')
            epc_name = request.data.get('epc_name')
            date = request.data.get('date')
            submitted_by = request.data.get('submitted_by')
            govern = request.data.get('govern')

            category1_items = ItemsProduct.objects.filter(item_category='category_1', project__in=project_id)
            category2_items = ItemsProduct.objects.filter(item_category='category_2', project__in=project_id)
            category3_items = ItemsProduct.objects.filter(item_category='category_3', project__in=project_id)
            other_items = ItemsProduct.objects.filter(item_category='other', project__in=project_id)

            context = {
                'project_name': project_name,
                'doc_no': doc_no,
                'customer': customer,
                'loa_no': loa_no,
                'epc_name': epc_name,
                'date': date,
                'submitted_by': submitted_by,
                'govern': govern,
                'category1_items': category1_items,
                'category2_items': category2_items,
                'category3_items': category3_items,
                'other_items': other_items,
            }

            template = get_template('categorywise_pdf.html')
            html = template.render(context)
            # print(html)

            timestamp = int(time.time())
            filename = f"categorywise_pdf_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'categorywise_pdfs', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(file_path)

            file_url = f"{settings.MEDIA_URL}categorywise_pdfs/{filename}"
            full_url = f"{request.scheme}://{request.get_host()}{file_url}"
            return Response({"status": True, "message": "PDF generated successfully", "data": full_url})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": ""})