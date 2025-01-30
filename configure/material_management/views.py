from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from activity_module.models import *
from material_management.models import *
from material_management.serializers import *


class MaterialManagementCreateViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialManagementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not request.user.groups.filter(name='Admin').exists():
            return Response({"status": False, "message": "You do not have permission to perform this action."})
        try:
            vendor_name = request.data.get('vendor_name')
            material_name = request.data.get('material_name')
            uom = request.data.get('uom')
            price = request.data.get('price')
            end_date = request.data.get('end_date')
            PR_number = request.data.get('PR_number')
            PO_number = request.data.get('PO_number')
            quantity = request.data.get('quantity')
            status = request.data.get('status')
            payment_status = request.data.get('payment_status')
            project_id = request.data.get('project_id')
            projectactivity_id = request.data.get('projectactivity_id')
            sub_activity_id = request.data.get('subactivity_id')
            sub_sub_activity_id = request.data.get('sub_sub_activity_id')


            project = Project.objects.get(id=project_id)
            projectactivity = ProjectActivity.objects.get(id=projectactivity_id)
            subactivity = SubActivityName.objects.get(id=sub_activity_id)
            sub_sub_activity = SubSubActivityName.objects.get(id=sub_sub_activity_id)

            if not project:
                return Response({"status": False, "message": "Project not found."})
            if not projectactivity:
                return Response({"status": False, "message": "Project Activity not found."})
            if not subactivity:
                return Response({"status": False, "message": "Sub Activity not found."})
            if not sub_sub_activity:
                return Response({"status": False, "message": "Sub Sub Activity not found."})
            

            if not vendor_name:
                return Response({"status": False, "message": "Vendor Name is required."})
            if not material_name:
                return Response({"status": False, "message": "Material Name is required."})
            if not uom:
                return Response({"status": False, "message": "Unit of Measurement is required."})
            if not price:
                return Response({"status": False, "message": "Price is required."})
            if not end_date:
                return Response({"status": False, "message": "End Date is required."})
            if not PR_number:
                return Response({"status": False, "message": "Purchase Request Number is required."})
            if not PO_number:
                return Response({"status": False, "message": "Purchase Order Number is required."})
            if not quantity:
                return Response({"status": False, "message": "Quantity is required."})
            if not status:
                return Response({"status": False, "message": "Status is required."})
            if not payment_status:
                return Response({"status": False, "message": "Payment Status is required."})
            
            material = MaterialManagement.objects.create(
                vendor_name=vendor_name,
                material_name=material_name,
                uom=uom,
                price=price,
                end_date=end_date,
                PR_number=PR_number,
                PO_number=PO_number,
                quantity=quantity,
                status=status,
                payment_status=payment_status,
                user=user,
                project=project,
                projectactivity=projectactivity,
                subactivity=subactivity,
                sub_sub_activity=sub_sub_activity,
            )
            serializer = self.serializer_class(material)
            data = serializer.data
            return Response({"status": True, "message": "Material Management created successfully.", "data":data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
    
    def list(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            return Response({"status": False, "message": "You do not have permission to perform this action."})
        queryset = MaterialManagement.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return Response({"status": True, "message": "Material Management List Successfully.", "data": data})
    
        
class MaterialManagementUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialManagementSerializer
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if not request.user.groups.filter(name='Admin').exists():
            return Response({"status": False, "message": "You do not have permission to perform this action."})
        try:
            material_id = self.kwargs.get('material_id')
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            material_obj = MaterialManagement.objects.get(id=material_id)
            if not material_obj:
                return Response({"status": True, "message": "Material Management Data is not found"})
            
            vendor_name = request.data.get('vendor_name')
            material_name = request.data.get('material_name')
            uom = request.data.get('uom')
            price = request.data.get('price')
            end_date = request.data.get('end_date')
            PR_number = request.data.get('PR_number')
            PO_number = request.data.get('PO_number')
            quantity = request.data.get('quantity')
            status = request.data.get('status')
            payment_status = request.data.get('payment_status')
            project_id = request.data.get('project_id')
            projectactivity_id = request.data.get('projectactivity_id')
            sub_activity_id = request.data.get('subactivity_id')
            sub_sub_activity_id = request.data.get('subsubactivity_id')

            material_obje = LandSurveyNumber.objects.create(vendor_name=vendor_name, material_name=material_name, uom=uom, price=price, 
                                                            end_date=end_date, PR_number=PR_number, PO_number=PO_number, quantity=quantity,
                                                            status=status, payment_status=payment_status, project_id=project_id,
                                                            projectactivity_id=projectactivity_id, sub_activity_id=sub_activity_id,
                                                            sub_sub_activity_id=sub_sub_activity_id)
            material_obje.save()
            
            serializer = self.serializer_class(material_obje)
            data = serializer.data
            return Response({"status": True, "message": "Material Management updated successfully.", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if not request.user.groups.filter(name='Admin').exists():
            return Response({"status": False, "message": "You do not have permission to perform this action."})
        try:
            material_id = self.kwargs.get('material_id')
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            material_obj = MaterialManagement.objects.get(id=material_id)
            if not material_obj:
                return Response({"status": True, "message": "Material Management Data is not found"})
            
            material_obj.delete()
            return Response({"status": True, "message": "Material Management deleted successfully."})
        except Exception as e:
            return Response({"status": False, "message": str(e)})