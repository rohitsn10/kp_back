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
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from hoto_module.models import DocumentCategory, Document

class FetchAllDocumentsNamesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotoDocumentSerializer


    def get(self, request, project_id, *args, **kwargs):
        try:

            # Validate project existence
            project = Project.objects.filter(id=project_id).first()
            if not project:
                return Response({"status": False, "message": "Project not found"})

            # Check if the user has any role in the project
            user = request.user
            if not project.project_assigned_users.filter(user=user).exists():
                return Response({"status": False, "message": "You do not have any role in this project"})
            # Fetch all categories
            categories = DocumentCategory.objects.all()

            # Use the serializer to construct the response
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )
            return Response({"status": True, "message": "Documents fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class UploadMainDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            project_id = request.data.get('project_id')
            document_name_id = request.data.get('document_id')  # Updated to use document ID
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
        
class ViewDocumentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, project_id, *args, **kwargs):
        try:
            if not Project.objects.filter(id=project_id).exists():
                return Response({"status": False, "message": "Project not found"})

            # Fetch all categories
            categories = DocumentCategory.objects.all()

            # Use the serializer to construct the response
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )
            return Response({"status": True, "message": "Documents retrieved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

class AddRemarksToDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, project_id, *args, **kwargs):
        try:
            doc_id = request.data.get('document_id')
            remarks = request.data.get('remarks')

            hoto_doc = HotoDocument.objects.get(document_name_id=doc_id, project_id=project_id)
            hoto_doc.remarks = remarks
            hoto_doc.updated_by = request.user
            hoto_doc.save()

            # Fetch updated categories and documents
            categories = DocumentCategory.objects.all()
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )
            return Response({"status": True, "message": "Remarks added successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        

class UploadDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]


    def create_or_update(self, request, project_id, *args, **kwargs):
        try:
            user = request.user
            document_name_id = request.data.get('document_id')
            status = request.data.get('status')
            remarks = request.data.get('remarks', None)
            files = request.FILES.getlist('file')

            # Validate document and category
            document_name = Document.objects.filter(id=document_name_id).first()
            category = DocumentCategory.objects.filter(id=document_name.category_id).first()

            if not document_name or not category:
                return Response({"status": False, "message": "Invalid document name or category"})
            project = Project.objects.filter(id=project_id).first()
            if not project:
                return Response({"status": False, "message": "Invalid project ID"})

            # Check if HotoDocument exists
            hoto_doc = HotoDocument.objects.filter(document_name_id=document_name_id, project_id=project_id).first()
            
            if not hoto_doc:
                # Create a new HotoDocument if it doesn't exist
                hoto_doc = HotoDocument.objects.create(
                    project=project,
                    document_name=document_name,
                    category=category,
                    status=status,
                    remarks=remarks,
                    created_by=user,
                    updated_by=user
                )
                message = "HotoDocument created successfully"
            else:
                hoto_doc.document_name = document_name
                hoto_doc.category = category
                hoto_doc.status = status
                hoto_doc.remarks = remarks
                hoto_doc.updated_by = user
                hoto_doc.save()
                message = "HotoDocument updated successfully"

            # Add uploaded files to DocumentsForHoto
            if files:
                for doc in files:
                    document = DocumentsForHoto.objects.create(file=doc)
                    hoto_doc.document.add(document)

                hoto_doc.is_uploaded = True
                hoto_doc.save()

            categories = DocumentCategory.objects.all()
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )
            return Response({"status": True, "message": "Document uploaded successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})

class DeleteParticularDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, project_id, *args, **kwargs):
        try:
            doc_ids = request.data.get('document_id', [])
            if not doc_ids:
                return Response({"status": False, "message": "No document IDs provided"})

            deleted_docs = []
            not_found_docs = []

            for doc_id in doc_ids:
                # Get the HotoDocument for this document_name_id
                hoto_doc = HotoDocument.objects.filter(document_name_id=doc_id, project_id=project_id).first()
                if not hoto_doc:
                    not_found_docs.append(doc_id)
                    continue
                
                # Find the specific DocumentsForHoto entries to delete
                docs_to_delete = hoto_doc.document.all()
                if docs_to_delete:
                    for doc in docs_to_delete:
                        file_path = os.path.join(settings.MEDIA_ROOT, str(doc.file))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        doc.delete()
                    
                    # Clear all documents from the HotoDocument
                    hoto_doc.document.clear()
                    
                    # Set is_uploaded to False since no documents remain
                    hoto_doc.is_uploaded = False
                    hoto_doc.updated_by = request.user
                    hoto_doc.save()
                    
                    deleted_docs.append(doc_id)
                else:
                    not_found_docs.append(doc_id)

            # Fetch updated categories and documents
            categories = DocumentCategory.objects.all()
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )

            if deleted_docs:
                message = f"Deleted documents: {deleted_docs}"
                if not_found_docs:
                    message += f". Documents not found: {not_found_docs}"
                return Response({"status": True, "message": message, "data": serializer.data})
            else:
                return Response({"status": False, "message": "No matching documents found", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
    
class VerifyDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, project_id, *args, **kwargs):
        try:
            doc_id = request.data.get('document_id')
            status = request.data.get('status')
            verify_comment = request.data.get('verify_comment')

            # Validate if the HotoDocument exists
            hoto_doc = HotoDocument.objects.filter(document_name_id=doc_id, project_id=project_id).first()
            if not hoto_doc:
                return Response({"status": False, "message": "HotoDocument not found"})

            # Validate status
            if status not in ["Verified", "Rejected", "Pending"]:
                return Response({"status": False, "message": "Invalid status value"})

            # Update the HotoDocument
            hoto_doc.status = status
            hoto_doc.verify_comment = verify_comment
            hoto_doc.updated_by = request.user
            hoto_doc.is_verified = True if status == "Verified" else False
            hoto_doc.save()

            # Fetch updated categories and documents
            categories = DocumentCategory.objects.all()
            serializer = HotoDocumentSerializer(
                categories, many=True, context={'project_id': project_id, 'request': request}
            )

            return Response({
                "status": True,
                "message": "Document verified successfully",
                "data": serializer.data
            })

        except Exception as e:
            return Response({"status": False, "message": str(e)})

class RaisePunchPointsViewSet(viewsets.ModelViewSet):
    queryset = PunchPointsRaise.objects.all()
    serializer_class = PunchPointsRaiseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, project_id, *args, **kwargs):
        try:
            punch_title = request.data.get('punch_title')
            punch_description = request.data.get('punch_description')
            punch_file = request.FILES.getlist('punch_file')

            project = Project.objects.get(id=project_id)
            user = request.user

            # Ensure user has ONM role
            user_role = get_user_role_for_project(project, user, allowed_roles=['on₹m'])
            if not user_role:
                return Response({"status": False, "message": "You do not have permission to raise punch points for this project"})

            punch_point_obj = PunchPointsRaise.objects.create(
                project=project,
                punch_title=punch_title,
                punch_description=punch_description,
                status="Open",
                created_by=user,
                updated_by=user
            )

            for file in punch_file:
                punch_file_obj = PunchFile.objects.create(file=file)
                punch_point_obj.punch_file.add(punch_file_obj)

            serializer = self.serializer_class(punch_point_obj)
            return Response({"status": True, "message": "Punch point created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

class AcceptedRejectedPunchPointsViewSet(viewsets.ModelViewSet):
    queryset = AcceptedRejectedPunchPoints.objects.all()
    serializer_class = AcceptedRejectedPunchPointsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
            user = request.user

            user_role = get_user_role_for_project(project, user, allowed_roles=['ondm'])
            if not user_role:
                return Response({"status": False, "message": "You do not have permission to raise punch points for this project"})

            punch_id = request.data.get('punch_id')
            is_accepted = request.data.get('is_accepted')
            punch_description = request.data.get('punch_description')
            tentative_timeline = request.data.get('tentative_timeline')
            comments = request.data.get('comments', '')
            punch_file = request.FILES.getlist('punch_file')

            punch_point_obj = PunchPointsRaise.objects.get(id=punch_id)

            if is_accepted:
                # If accepted, create a completed punch point
                accepted_punch_obj = AcceptedRejectedPunchPoints.objects.create(
                    raise_punch=punch_point_obj,
                    punch_description=punch_description,
                    tentative_timeline=tentative_timeline,
                    comments=comments,
                    status="Accepted",
                    created_by=user,
                    updated_by=user
                )

                for file in punch_file:
                    accepted_punch_file_obj = AcceptedRejectedPunchFile.objects.create(file=file)
                    accepted_punch_obj.punch_file.add(accepted_punch_file_obj)
                completed_punch_obj= CompletedPunchPoints.objects.create(
                    accepted_rejected_punch=accepted_punch_obj,  # Use the correct field name
                    remarks=comments,  # Map comments to remarks
                    status="Accepted",
                    created_by=user,
                    updated_by=user
                )
                for file in punch_file:
                    completed_punch_file_obj = CompletedPunchFile.objects.create(file=file)
                    completed_punch_obj.punch_file.add(completed_punch_file_obj)
                punch_point_obj.status = "Accepted"
                punch_point_obj.is_verified = True
                punch_point_obj.save()
                serializer = self.serializer_class(accepted_punch_obj)
                return Response({"status": True, "message": "Punch point accepted successfully", "data": serializer.data})
            else:
                # If rejected, update the punch point
                punch_point_obj.status = "Rejected"
                punch_point_obj.is_verified = False
                punch_point_obj.save()

                for file in punch_file:
                    punch_file_obj = PunchFile.objects.create(file=file)
                    punch_point_obj.punch_file.add(punch_file_obj)

                serializer = PunchPointsRaiseSerializer(punch_point_obj)
                return Response({"status": True, "message": "Punch point rejected successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class MarkPunchPointsCompletedViewSet(viewsets.ModelViewSet):
    queryset = CompletedPunchPoints.objects.all()
    serializer_class = CompletedPunchPointsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, project_id, *args, **kwargs):
        try:
            completed_punch_id = request.data.get('completed_punch_id')
            remarks = request.data.get('remarks')
            punch_file = request.FILES.getlist('punch_file')

            project = Project.objects.get(id=project_id)
            user = request.user

            user_role = get_user_role_for_project(project, user, allowed_roles=['onm'])
            if not user_role:
                return Response({"status": False, "message": "You do not have permission to raise punch points for this project"})

            completed_punch_obj = CompletedPunchPoints.objects.get(id=completed_punch_id)

            completed_punch_obj.remarks = remarks
            completed_punch_obj.status = "Completed"
            completed_punch_obj.updated_by = user
            completed_punch_obj.save()

            for file in punch_file:
                completed_punch_file_obj = CompletedPunchFile.objects.create(file=file)
                completed_punch_obj.punch_file.add(completed_punch_file_obj)

            serializer = self.serializer_class(completed_punch_obj)
            return Response({"status": True, "message": "Punch point marked as completed successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        

class VerifyCompletedPunchPointsViewSet(viewsets.ModelViewSet):
    queryset = VerifyPunchPoints.objects.all()
    serializer_class = VerifyPunchPointsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, project_id, *args, **kwargs):
        try:
            completed_punch_id = request.data.get('completed_punch_id')
            verify_description = request.data.get('verify_description')
            status = request.data.get('status')

            project = Project.objects.get(id=project_id)
            user = request.user

            # Ensure user has ONM role
            user_role = get_user_role_for_project(project, user, allowed_roles=['onm'])
            if not user_role:
                return Response({"status": False, "message": "You do not have permission to raise punch points for this project"})

            completed_punch_obj = CompletedPunchPoints.objects.get(id=completed_punch_id)

            verify_punch_obj = VerifyPunchPoints.objects.create(
                completed_punch=completed_punch_obj,
                verify_description=verify_description,
                status=status,
                created_by=user,
                updated_by=user
            )

            serializer = self.serializer_class(verify_punch_obj)
            return Response({"status": True, "message": "Punch point verified successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

class GetAllProjectWisePunchRaiseCompletedVerifyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, project_id, *args, **kwargs):
        try:
            # Fetch the project and validate user access
            project = get_object_or_404(Project, id=project_id)
            user = request.user
            if not project.project_assigned_users.filter(user=user).exists():
                return Response(
                    {"status": False, "message": "You do not have any role in this project"},
                    status=403,
                )

            # Fetch data for the project
            punch_points = PunchPointsRaise.objects.filter(project=project)
            completed_punch_points = CompletedPunchPoints.objects.filter(
                accepted_rejected_punch__raise_punch__project=project
            )
            verified_punch_points = VerifyPunchPoints.objects.filter(
                completed_punch__accepted_rejected_punch__raise_punch__project=project
            )

            # Serialize the data
            punch_points_serializer = PunchPointsRaiseSerializer(punch_points, many=True)
            completed_punch_points_serializer = CompletedPunchPointsSerializer(
                completed_punch_points, many=True
            )
            verified_punch_points_serializer = VerifyPunchPointsSerializer(
                verified_punch_points, many=True
            )

            # Return the response
            return Response(
                {
                    "status": True,
                    "message": "All object-wise punch points retrieved successfully",
                    "data": {
                        "punch_points": punch_points_serializer.data,
                        "completed_punch_points": completed_punch_points_serializer.data,
                        "verified_punch_points": verified_punch_points_serializer.data,
                    },
                }
            )
        except Project.DoesNotExist:
            return Response(
                {"status": False, "message": "Project not found"}, status=404
            )
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)
        
    

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
        
def get_user_role_for_project(project, user, allowed_roles=None):
    """
    Returns the role string if user is assigned to project.
    If allowed_roles is provided (iterable of substrings), returns None when role not matching.
    Matching is case-insensitive and checks substring.
    """
    role = project.project_assigned_users.filter(user=user).values_list('role', flat=True).first()
    if not role:
        return None
    if allowed_roles:
        role_l = role.lower()
        for ar in allowed_roles:
            if ar.lower() in role_l:
                return role
        return None
    return role