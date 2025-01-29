from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from document_control.models import *
from document_control.serializers import *


class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
                return Response({"status": False, "message": "You do not have permission to perform this action."})
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
            assigned_user = request.data.get('assigned_users', '')
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
            if not assigned_user:
                return Response({"status": False, "message": "assigned_users is required"})
            
            assigned_users = [int(user_id.strip()) for user_id in assigned_user.split(',')]

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
            if assigned_users:
                users_to_assign = CustomUser.objects.filter(id__in=assigned_users)
                if users_to_assign.count() != len(assigned_users):
                    return Response({"status": False, "message": "One or more user IDs are invalid"})
                
                document_obj.assign_users.set(users_to_assign)

            document_obj.document_attachments.set(attachment_instances)
            document_obj.save()

            serializers = self.serializer_class(document_obj)
            data = serializers.data
            assigned_user_ids = [user.id for user in document_obj.assign_users.all()]
            data['assigned_users'] = assigned_user_ids

            return Response({"status": True, "message": "Document Created Successfully", "data": data})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Admin').exists():
            documents = DocumentManagement.objects.all()
        else:
            documents = DocumentManagement.objects.filter(assign_users=request.user)
        serializer = self.serializer_class(documents, many=True)

        for document_data in serializer.data:
            for attachment in document_data.get('document_attachments', []):
                attachment['document_attachments'] = request.build_absolute_uri(attachment['document_attachments'])

        return Response({"status": True, "message": "Documents List Retrieved Successfully", "data": serializer.data})
    
class DocumentUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
                return Response({"status": False, "message": "You do not have permission to perform this action."})
        
        try:
            document_id = self.kwargs.get('document_id')
            if not document_id:
                return Response({"status": False, "message": "document_id not found."}, )

            document_obj = DocumentManagement.objects.get(id = document_id)
            if not document_obj:
                return Response({"status": True, "message": "Documents Data is not found", "data": data})
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
            assigned_user_ids = request.data.get('assigned_users', [])

            if assigned_user_ids:
                assigned_users = CustomUser.objects.filter(id__in=assigned_user_ids)
                document_obj.assign_users.set(assigned_users)

            document_obj.document_attachments.set(attachment_instances)
            document_obj.save()

            serializer = self.serializer_class(document_obj)
            data = serializer.data
            return Response({"status": True, "message": "Document Updated Successfully", "data": data})

        except DocumentManagement.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def destroy(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
                return Response({"status": False, "message": "You do not have permission to perform this action."})
        try:
            document_id = self.kwargs.get('document_id')
            if not document_id:
                return Response({"status": False, "message": "document_id not found."})
            
            document_obj = DocumentManagement.objects.get(id = document_id)
            if not document_obj:
                return Response({"status": True, "message": "Documents Data is not found"})
            
            document_obj.delete()

            return Response({"status": True, "message": "Document Deleted Successfully"})

        except DocumentManagement.DoesNotExist:
            return Response({"status": False, "message": "Document not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})