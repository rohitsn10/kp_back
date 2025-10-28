from django.shortcuts import render
from user_profile.models import *
from .views import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML
import os
import time
from rest_framework.views import APIView
from hoto_module.models import DocumentCategory, Document

class FetchAllDocumentsNamesView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categories = DocumentCategory.objects.all()
            data = []

            for category in categories:
                documents = category.documents.all()
                data.append({
                    "id": category.id,
                    "category": category.name,
                    "documents": [{'id': doc.id, 'name': doc.name} for doc in documents]
                })

            return Response({"status": True, "message": "Documents fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class UploadMainDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            project_id = request.data.get('project_id')
            document_name_id = request.data.get('document_name_id')  # Updated to use document ID
            category_id = request.data.get('category_id')  # Updated to use category ID
            status = request.data.get('status')
            remarks = request.data.get('remarks', None)
            file = request.FILES.getlist('file')

            # Validate document and category
            document_name = Document.objects.filter(id=document_name_id).first()
            category = DocumentCategory.objects.filter(id=category_id).first()

            if not document_name or not category:
                return Response({"status": False, "message": "Invalid document name or category"})

            # Create HotoDocument entry
            hoto_doc = HotoDocument.objects.create(
                project_id=project_id,
                document_name=document_name,
                category=category,
                status=status,
                remarks=remarks,
                created_by=user,
                updated_by=user
            )

            # Add uploaded files to DocumentsForHoto
            for doc in file:
                document = DocumentsForHoto.objects.create(file=doc)
                hoto_doc.document.add(document)

            serializer = HotoDocumentSerializer(hoto_doc)
            return Response({"status": True, "message": "Documents uploaded/created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
class ViewDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            project_id = request.query_params.get('project_id')  # Use query parameters for better flexibility

            if not project_id:
                return Response({"status": False, "message": "Project ID is required"})

            # Filter documents by project ID
            documents = HotoDocument.objects.filter(project_id=project_id).order_by('-created_at')

            if not documents.exists():
                return Response({"status": False, "message": "No documents found for the given project"})

            # Serialize the documents
            serializer = HotoDocumentSerializer(documents, many=True)
            return Response({"status": True, "message": "Documents retrieved successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})

class AddRemarksToDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            doc_id = kwargs.get('doc_id')
            remarks = request.data.get('remarks')

            hoto_doc = HotoDocument.objects.get(id=doc_id)
            hoto_doc.remarks = remarks
            hoto_doc.updated_by = request.user
            hoto_doc.save()

            serializer = HotoDocumentSerializer(hoto_doc)
            return Response({"status": True, "message": "Remarks added successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        

class UploadDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def upload_or_update(self, request, *args, **kwargs):
        try:
            user = request.user
            project_id = request.data.get('project_id')
            document_id = request.data.get('document_id')
            category_id = request.data.get('category_id')
            files = request.FILES.getlist('file')

            # Validate document and category
            document_name = Document.objects.filter(id=document_id).first()
            category = DocumentCategory.objects.filter(id=category_id).first()

            if not document_name or not category:
                return Response({"status": False, "message": "Invalid document name or category"})

            # Try to find existing HotoDocument
            hoto_doc = HotoDocument.objects.filter(document_name_id=document_id, project_id=project_id).first()

            if hoto_doc:
                # Update existing
                if not files:
                    return Response({"status": False, "message": "No files provided for upload"})
                for doc in files:
                    document = DocumentsForHoto.objects.create(file=doc)
                    hoto_doc.document.add(document)
                hoto_doc.is_uploaded = True
                hoto_doc.updated_by = user
                hoto_doc.save()
                serializer = HotoDocumentSerializer(hoto_doc)
                return Response({"status": True, "message": "Documents uploaded successfully", "data": serializer.data})
            else:
                # Create new
                if not files:
                    return Response({"status": False, "message": "No files provided for upload"})
                hoto_doc = HotoDocument.objects.create(
                    project_id=project_id,
                    document_name=document_name,
                    category=category,
                    created_by=user,
                    updated_by=user,
                    is_uploaded=True
                )
                for doc in files:
                    document = DocumentsForHoto.objects.create(file=doc)
                    hoto_doc.document.add(document)
                serializer = HotoDocumentSerializer(hoto_doc)
                return Response({"status": True, "message": "Documents uploaded/created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def create(self, request, *args, **kwargs):
        return self.upload_or_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.upload_or_update(request, *args, **kwargs)

class DeleteParticularDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            doc_ids = request.data.get('doc_id', [])
            if not doc_ids:
                return Response({"status": False, "message": "No document IDs provided"})

            deleted_docs = []
            not_found_docs = []

            for doc_id in doc_ids:
                doc = DocumentsForHoto.objects.filter(id=doc_id).first()
                if doc:
                    file_path = os.path.join(settings.MEDIA_ROOT, str(doc.file))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    doc.delete()
                    deleted_docs.append(doc_id)
                else:
                    not_found_docs.append(doc_id)

            if deleted_docs:
                message = f"Deleted documents: {deleted_docs}"
                if not_found_docs:
                    message += f". Documents not found: {not_found_docs}"
                return Response({"status": True, "message": message})
            else:
                return Response({"status": False, "message": "No matching documents found"})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
    
class VerifyDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            doc_id = kwargs.get('doc_id')
            status = request.data.get('status')
            verify_comment = request.data.get('verify_comment')

            # Validate if the HotoDocument exists
            hoto_doc = HotoDocument.objects.filter(id=doc_id).first()
            if not hoto_doc:
                return Response({"status": False, "message": "HotoDocument not found"})

            # Validate status
            if status not in ["Verified", "Rejected", "Pending"]:
                return Response({"status": False, "message": "Invalid status value"})

            # Update the HotoDocument
            hoto_doc.status = status
            hoto_doc.verify_comment = verify_comment
            hoto_doc.updated_by = request.user
            hoto_doc.save()

            # Serialize and return the updated HotoDocument
            serializer = HotoDocumentSerializer(hoto_doc)
            return Response({"status": True, "message": "Document verified successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})

class RaisePunchPointsViewSet(viewsets.ModelViewSet):
    queryset = PunchPointsRaise.objects.all()
    serializer_class = PunchPointsRaiseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            hoto_id = request.data.get('hoto_id')
            punch_title = request.data.get('punch_title')
            punch_description = request.data.get('punch_description')
            punch_point_raised = request.data.get('punch_point_raised')
            closure_date = request.data.get('closure_date')
            status = request.data.get('status')
            punch_file = request.FILES.getlist('punch_file')

            hoto_doc = HotoDocument.objects.get(id=hoto_id)

            punch_point_obj = PunchPointsRaise.objects.create(
                hoto=hoto_doc,
                punch_title=punch_title,
                punch_description=punch_description,
                punch_point_raised=punch_point_raised,
                closure_date=closure_date,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )

            for file in punch_file:
                punch_file_obj = PunchFile.objects.create(file=file)
                punch_point_obj.punch_file.add(punch_file_obj)

            serializer = PunchPointsRaiseSerializer(punch_point_obj)
            return Response({"status": True, "message": "Punch point created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    
class CompletedPunchPointsViewSet(viewsets.ModelViewSet):
    queryset = CompletedPunchPoints.objects.all()
    serializer_class = CompletedPunchPointsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            punch_id = request.data.get('punch_id')
            punch_description = request.data.get('punch_description')
            punch_point_completed = request.data.get('punch_point_completed')
            status = request.data.get('status')
            punch_file = request.FILES.getlist('punch_file')

            punch_point_obj = PunchPointsRaise.objects.get(id=punch_id)

            completed_punch_obj = CompletedPunchPoints.objects.create(
                raise_punch=punch_point_obj,
                punch_description=punch_description,
                punch_point_completed=punch_point_completed,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )

            for file in punch_file:
                completed_punch_file_obj = CompletedPunchFile.objects.create(file=file)
                completed_punch_obj.punch_file.add(completed_punch_file_obj)

            serializer = CompletedPunchPointsSerializer(completed_punch_obj)
            return Response({"status": True, "message": "Completed punch point created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    
class VerifyCompletedPunchPointsViewSet(viewsets.ModelViewSet):
    queryset = VerifyPunchPoints.objects.all()
    serializer_class = VerifyPunchPointsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            completed_punch_id = kwargs.get('completed_punch_id')
            verify_description = request.data.get('verify_description')
            status = request.data.get('status')

            completed_punch_obj = CompletedPunchPoints.objects.get(id=completed_punch_id)
            if status == "Completed":
                pass
            else:
                completed_punch_obj.punch_point_completed = 0
                completed_punch_obj.save()

            verify_punch_obj = VerifyPunchPoints.objects.create(
                completed_punch=completed_punch_obj,
                verify_description=verify_description,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )

            serializer = VerifyPunchPointsSerializer(verify_punch_obj)
            return Response({"status": True, "message": "Completed punch point verified successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        


class GetAllObjectWisePunchRaiseCompletedVerifyViewSet(viewsets.ModelViewSet):
    queryset = PunchPointsRaise.objects.all()
    serializer_class = PunchPointsRaiseSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            hoto_id = request.query_params.get('hoto_id')

            punch_points = PunchPointsRaise.objects.filter(hoto=hoto_id)
            completed_punch_points = CompletedPunchPoints.objects.filter(raise_punch__hoto=hoto_id)
            verified_punch_points = VerifyPunchPoints.objects.filter(completed_punch__raise_punch__hoto=hoto_id)

            punch_points_serializer = PunchPointsRaiseSerializer(punch_points, many=True)
            completed_punch_points_serializer = CompletedPunchPointsSerializer(completed_punch_points, many=True)
            verified_punch_points_serializer = VerifyPunchPointsSerializer(verified_punch_points, many=True)

            return Response({
                "status": True,
                "message": "All object-wise punch points retrieved successfully",
                "data": {
                    "punch_points": punch_points_serializer.data,
                    "completed_punch_points": completed_punch_points_serializer.data,
                    "verified_punch_points": verified_punch_points_serializer.data
                }
            })
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        


class HOTOCertificateViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            context = {
                'project_id': data.get('project_id'),
                'plant_name': data.get('plant_name'),
                'plant_cod': data.get('plant_cod'),
                'issued_date': data.get('issued_date'),
                'project_team_name': data.get('project_team_name'),
                'onm_team_name': data.get('onm_team_name'),
                'epc_team_name': data.get('epc_team_name'),
                'list_attached': [doc for doc in data.get('list_attached', []) if doc.strip()],
                'design_section': data.get('design_section', {}),
                'scm_section': data.get('scm_section', {}),
                'project_section': data.get('project_section', {}),
                'user_names': data.get('user_names', {})
            }

            # Load and render HTML template
            template = get_template('hoto_certificate.html')  # Ensure template name matches
            html = template.render(context)

            # Save PDF
            timestamp = int(time.time())
            filename = f"hoto_certificate_{timestamp}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'hoto_pdfs', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(file_path)

            # Respond with full URL
            file_url = f"{settings.MEDIA_URL}hoto_pdfs/{filename}"
            full_url = f"{request.scheme}://{request.get_host()}{file_url}"
            return Response({"status": True, "message": "PDF generated successfully", "data": full_url})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": ""})