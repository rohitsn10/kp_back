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