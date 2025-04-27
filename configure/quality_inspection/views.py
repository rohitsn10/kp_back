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

            quality_inspection = RFIFieldActivity.objects.filter(id=rfi_id).update(
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

            quality_inspection = InspectionOutcome.objects.create(
                project_id=project_id,
                rfi_field_activity=rfi_id,
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

            quality_inspection = InspectionOutcome.objects.filter(id=rfi_id).update(
                project_id=project_id,
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