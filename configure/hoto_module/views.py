from django.shortcuts import render
from user_profile.models import *
from .views import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
import os
import time


class UploadMainDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            project_id = request.data.get('project_id')
            document_name = request.data.get('document_name')
            category = request.data.get('category')
            status = request.data.get('status')
            file = request.FILES.getlist('file')

            hoto_doc = HotoDocument.objects.create(
                project_id=project_id,
                document_name=document_name,
                category=category,
                status=status,
                created_by=user,
                updated_by=user
            )

            for doc in file:
                document = DocumentsForHoto.objects.create(file=doc)
                hoto_doc.document.add(document)

            serializer = HotoDocumentSerializer(hoto_doc)
            return Response({"status": True, "message": "Documents Uploaded/created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class ViewDocumentViewSet(viewsets.ModelViewSet):
    queryset = HotoDocument.objects.all()
    serializer_class = HotoDocumentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            documents = HotoDocument.objects.filter(project=project_id).order_by('-created_at')
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

    def update(self, request, *args, **kwargs):
        try:
            doc_id = kwargs.get('doc_id')
            file = request.FILES.getlist('file')

            hoto_doc = HotoDocument.objects.get(id=doc_id)

            for doc in file:
                document = DocumentsForHoto.objects.create(file=doc)
                hoto_doc.document.add(document)

            serializer = HotoDocumentSerializer(hoto_doc)
            return Response({"status": True, "message": "Documents Uploaded successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        


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
            for doc_id in doc_ids:
                doc = DocumentsForHoto.objects.filter(id=doc_id).first()
                if doc:
                    file_path = os.path.join(settings.MEDIA_ROOT, str(doc.file))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    doc.delete()
                    deleted_docs.append(doc_id)

            if deleted_docs:
                return Response({"status": True, "message": f"Deleted documents: {deleted_docs}"})
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

            hoto_doc = HotoDocument.objects.get(id=doc_id)
            hoto_doc.status = status
            hoto_doc.verify_comment = verify_comment
            hoto_doc.updated_by = request.user
            hoto_doc.save()

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
            status = request.data.get('status')
            punch_file = request.FILES.getlist('punch_file')

            hoto_doc = HotoDocument.objects.get(id=hoto_id)

            punch_point_obj = PunchPointsRaise.objects.create(
                hoto=hoto_doc,
                punch_title=punch_title,
                punch_description=punch_description,
                punch_point_raised=punch_point_raised,
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