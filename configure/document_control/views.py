from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from document_control.models import *
from document_control.serializers import *


class DocumentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        try:
            document_name = request.data.get('document_name')
            document_number = request.data.get('document_number')
            project_id = request.data.get('project')
            revision_number = request.data.get('revision_number')
            keywords = request.data.get('keywords')
            confidential_level = request.data.get('confidential_level')
            status = request.data.get('status')
            comments = request.data.get('comments')
            document_attachments = request.FILES.getlist('document_attachments', [])
            user = request.user

            if not document_name:
                return Response({"status": False, "message": "documentname is required"})
            if not document_number:
                return Response({"status": False, "message": "documentnumber is required"})
            if not revision_number:
                return Response({"status": False, "message": "revision_number is required"})
            if not keywords:
                return Response({"status": False, "message": "keywords is required"})
            if not confidential_level:
                return Response({"status": False, "message": "confidential_level is required"})
            if not status:
                return Response({"status": False, "message": "status is required"})
            if not comments:
                return Response({"status": False, "message": "comments is required"})
            if not document_attachments:
                return Response({"status": False, "message": "document_attachments is required"})

            project_instance = None
            if project_id:
                try:
                    project_instance = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return Response({"status": False, "message": "Project not found"})

            attachment_instances = []
            for attachment in document_attachments:
                attachment_obj = DocumentManagementAttachments.objects.create(document_attachments=attachment)
                attachment_instances.append(attachment_obj)

            document_obj = DocumentManagement.objects.create(
                documentname=document_name,
                documentnumber=document_number,
                project=project_instance,
                revision_number=revision_number,
                keywords=keywords,
                confidentiallevel=confidential_level,
                status=status,
                comments=comments,
                created_by=user
            )

            document_obj.document_attachments.set(attachment_instances)
            document_obj.save()

            serializers = self.serializer_class(document_obj)
            data = serializers.data
            return Response({"status": True, "message": "Document Created Successfully", "data": data})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(many=True)
        data = serializer.data
        return Response({"status": True, "message": "Documents List Retrieved Successfully", "data": data})

    def update(self, request, *args, **kwargs):
        try:
            document_id = self.kwargs.get('document_id')
            if not document_id:
                return Response({"status": False, "message": "document_id not found."}, )

            document_obj = self.get_object()

            document_attachments = request.data.get('document_attachments', [])
            attachment_instances = []
            for attachment in document_attachments:
                attachment_obj = DocumentManagementAttachments.objects.create(document_attachments=attachment)
                attachment_instances.append(attachment_obj)

            document_obj.documentname = request.data.get('document_name', document_obj.documentnumber)
            document_obj.documentnumber = request.data.get('documentnumber', document_obj.documentnumber)
            document_obj.project = request.data.get('project', document_obj.project)
            document_obj.revision_number = request.data.get('revision_number', document_obj.revision_number)
            document_obj.keywords = request.data.get('keywords', document_obj.keywords)
            document_obj.confidentiallevel = request.data.get('confidentiallevel', document_obj.confidentiallevel)
            document_obj.status = request.data.get('status', document_obj.status)
            document_obj.comments = request.data.get('comments', document_obj.comments)
            document_obj.created_by = request.user

            document_obj.document_attachments.set(attachment_instances)
            document_obj.save()

            serializer = self.serializer_class(document_obj)
            data = {'documentname': serializer.data['documentname'],'documentnumber': serializer.data['documentnumber'],'updated_at': serializer.data['updated_at'],}
            return Response({"status": True, "message": "Document Updated Successfully", "data": data})

        except DocumentManagement.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def destroy(self, request, *args, **kwargs):
        try:
            document_obj = self.get_object()
            document_obj.delete()

            return Response({"status": True, "message": "Document Deleted Successfully"})

        except DocumentManagement.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})