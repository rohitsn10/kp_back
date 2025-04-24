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