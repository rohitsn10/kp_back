import datetime
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from activity_module.models import *
from material_management.models import *
from material_management.serializers import *
from user_profile.function_call import *

class MaterialManagementCreateViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialManagementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        # if not request.user.groups.filter(name='Admin').exists():
        #     return Response({"status": False, "message": "You do not have permission to perform this action."})
        try:
            # client_vendor_choices = request.data.get('client_vendor_choices',None)
            # client_name = None
            # vendor_code = None
            # if client_vendor_choices == 'client':
                # client_name = request.data.get('client_name','')
            # if client_vendor_choices == 'vendor':
                # vendor_name = request.data.get('vendor_name')

            material_code = request.data.get('material_code')
            # material_name = request.data.get('material_name')
            vendor_code = request.data.get('vendor_code')
            uom = request.data.get('uom')
            price = request.data.get('price')
            PR_number = request.data.get('PR_number')
            pr_date = parse_date(request.data.get('pr_date'))
            PO_number = request.data.get('PO_number')
            po_date = parse_date(request.data.get('po_date'))
            material_required_date = parse_date(request.data.get('material_required_date'))
            quantity = request.data.get('quantity')
            project_id = request.data.get('project_id')
            # projectactivity_id = request.data.get('projectactivity_id')
            # sub_activity_id = request.data.get('subactivity_id')
            # sub_sub_activity_id = request.data.get('sub_sub_activity_id')


            try:  # Inner try-except for Project lookup
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({"status": False, "message": "Project not found."})
            # projectactivity = ProjectActivity.objects.get(id=projectactivity_id)
            # subactivity = SubActivityName.objects.get(id=sub_activity_id)
            # sub_sub_activity = SubSubActivityName.objects.get(id=sub_sub_activity_id)

            # if not projectactivity:
            #     return Response({"status": False, "message": "Project Activity not found."})
            # if not subactivity:
            #     return Response({"status": False, "message": "Sub Activity not found."})
            # if not sub_sub_activity:
            #     return Response({"status": False, "message": "Sub Sub Activity not found."})
            
            
            material = MaterialManagement.objects.create(
                user = user,
                # client_vendor_choices=client_vendor_choices,
                # client_name=client_name,
                vendor_code=vendor_code,
                material_code=material_code,
                # material_name=material_name,
                uom=uom,
                price=price,
                PR_number=PR_number,
                pr_date = pr_date,
                PO_number=PO_number,
                po_date = po_date,
                material_required_date = material_required_date,
                quantity=quantity,
                project=project,
                # projectactivity=projectactivity,
                # subactivity=subactivity,
                # sub_sub_activity=sub_sub_activity,
            )
            serializer = self.serializer_class(material)
            data = serializer.data
            return Response({"status": True, "message": "Material Management created successfully.", "data":data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
    
    def list(self, request, *args, **kwargs):
        # if not request.user.groups.filter(name='Admin').exists():
        #     return Response({"status": False, "message": "You do not have permission to perform this action."})
        queryset = MaterialManagement.objects.all().order_by('-id')
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
            # client_name = None
            # vendor_name = None
            # client_vendor_choices = request.data.get('client_vendor_choices',None)
            
            # if client_vendor_choices == 'client':
                # client_name = request.data.get('client_name')
                # vendor_name = None
                # if not client_name:
                #   return Response({"status": False, "message": "Client name is required."})

            # elif client_vendor_choices == 'vendor':
                # vendor_name = request.data.get('vendor_name')
                # client_name = None
                # if not vendor_name:
                #   return Response({"status": False, "message": "Vendor name is required."})

            material_code = request.data.get('material_code')
            vendor_code = request.data.get('vendor_code')
            # material_name = request.data.get('material_name')
            uom = request.data.get('uom')
            price = request.data.get('price')
            PR_number = request.data.get('PR_number')
            pr_date = parse_date(request.data.get('pr_date'))
            PO_number = request.data.get('PO_number')
            po_date = parse_date(request.data.get('po_date'))
            material_required_date = request.data.get('material_required_date')
            quantity = request.data.get('quantity')
            status = request.data.get('status')
            payment_status = request.data.get('payment_status')
            project_id = request.data.get('project_id')
            # project_activity_id = request.data.get('project_activity_id')
            # sub_activity_id = request.data.get('sub_activity_id')
            # sub_sub_activity_id = request.data.get('sub_sub_activity_id')

            if project_id:
                try:
                    project_id = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return Response({"status": False, "message": "Invalid project."})

            # if project_activity_id:
            #     try:
            #         project_activity_id = ProjectActivity.objects.get(id=project_activity_id)
            #     except ProjectActivity.DoesNotExist:
            #         return Response({"status": False, "message": "Invalid project activity."})

            # if sub_activity_id:
            #     try:
            #         sub_activity_id = SubActivityName.objects.get(id=sub_activity_id)
            #     except SubActivityName.DoesNotExist:
            #         return Response({"status": False, "message": "Invalid sub activity."})

            # if sub_sub_activity_id:
            #     try:
            #         sub_sub_activity_id = SubSubActivityName.objects.get(id=sub_sub_activity_id)
            #     except SubSubActivityName.DoesNotExist:
            #         return Response({"status": False, "message": "Invalid sub sub activity."})
            # if client_vendor_choices:
                # material_obj.client_vendor_choices = client_vendor_choices
            # if client_name is not None:
                # material_obj.client_name = client_name
            # if vendor_name is not None:
                # material_obj.vendor_name = vendor_name
            if material_code:
                material_obj.material_code = material_code
            if vendor_code:
                material_obj.vendor_code = vendor_code
            # if material_name:
                # material_obj.material_name = material_name
            if uom:
                material_obj.uom = uom
            if price:
                material_obj.price = price
            if PR_number:
                material_obj.PR_number = PR_number
            if pr_date:
                material_obj.pr_date = pr_date
            if PO_number:
                material_obj.PO_number = PO_number
            if po_date:
                material_obj.po_date = po_date
            if material_required_date:
                material_obj.material_required_date = material_required_date
            if quantity:
                material_obj.quantity = quantity
            if status:
                material_obj.status = status
            if payment_status:
                material_obj.payment_status = payment_status
            if project_id:
                material_obj.project = project_id
            # if project_activity_id:
            #     material_obj.projectactivity = project_activity_id
            # if sub_activity_id:
            #     material_obj.subactivity = sub_activity_id
            # if sub_sub_activity_id:
            #     material_obj.sub_sub_activity = sub_sub_activity_id
            material_obj.updated_at = datetime.now()
            material_obj.save()

            serializer = self.serializer_class(material_obj, context={'request': request})
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
        
        
class UpddateOnlyDeliverDateOfMaterialViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialManagementSerializer
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        
        try:
            material_id = self.kwargs.get('material_id')
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            material_obj = MaterialManagement.objects.get(id=material_id)
            if not material_obj:
                return Response({"status": True, "message": "Material Management Data is not found"})
            delivered_date = parse_date(request.data.get('delivered_date'))
            number_of_delay = request.data.get('number_of_delay')
            material_obj.delivered_date = delivered_date
            material_obj.number_of_delay = number_of_delay
            material_obj.status = 'delivered'
            material_obj.save()
            serializer = self.serializer_class(material_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Material Management updated successfully.", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class ApprovedMaterialViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialManagementSerializer
    queryset = MaterialManagement.objects.all()
    lookup_field = "material_id"
    def update(self, request, *args, **kwargs):
        
        try:
            user = self.request.user
            material_id = kwargs.get('material_id')
            is_approved_remarks = request.data.get('is_approved_remarks','')
            
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            material_obj = MaterialManagement.objects.get(id=material_id)
            if not material_obj:
                return Response({"status": True, "message": "Material Data is not found"})
            
            material_obj.is_approved = True
            material_obj.is_approved_by = user
            material_obj.is_approved_date = datetime.now()
            if is_approved_remarks:
                material_obj.is_approved_remarks = is_approved_remarks
            
            add_in_approval_action = MaterialApprovalAction.objects.create(user = user,material = material_obj,remarks = is_approved_remarks)
            add_in_approval_action.save()
            material_obj.save()
            
            serializer = self.serializer_class(material_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Material updated successfully.", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
            


class AddInspectionOfMaterialViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InspectionMaterialSerializer
    queryset = InspectionOfMaterial.objects.all()
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        
        try:
            material_id = request.data.get('material_id')
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            material_obj = MaterialManagement.objects.get(id=material_id)
            if not material_obj:
                return Response({"status": True, "message": "Material Management Data is not found"})
            
            inspection_date = parse_date(request.data.get('inspection_date'))
            inspection_quality_report = request.data.get('inspection_quality_report')
            gtp = request.data.get('gtp')
            qap = request.data.get('qap')
            gtp_attachments = request.data.getlist('gtp_attachments', []) or []
            qap_attachments = request.data.getlist('qap_attachments', []) or []
            inspection_quality_report_attachments = request.data.getlist('inspection_quality_report_attachments',[]) or []
            remarks = request.data.get('remarks','')
            
            inspection_obj = InspectionOfMaterial.objects.create(
                user = user,
                material_management = material_obj,
                inspection_date = inspection_date,
                inspection_quality_report = inspection_quality_report,
                remarks = remarks,
                gtp = gtp,
                qap = qap
            )
            
            for attachment in inspection_quality_report_attachments:
                attachment_obj = MaterialQualityReportAttacchments.objects.create(
                    inspection_quality_report_attachments = attachment
                )
                inspection_obj.inspection_quality_report_attachments.add(attachment_obj)
            
            for attachment in gtp_attachments:
                attachment_obj = MaterialGTPAttachment.objects.create(
                    gtp_attachments = attachment
                )
                inspection_obj.gtp_attachments.add(attachment_obj)
            
            for attachment in qap_attachments:
                attachment_obj = MaterialQAPAttachment.objects.create(
                    qap_attachments = attachment
                )
                inspection_obj.qap_attachments.add(attachment_obj)
                
            serializer = self.serializer_class(inspection_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Inspection Material created successfully.", "data": data})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Inspection Material List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
class MaterialIdwiseGetInspectionViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InspectionMaterialSerializer
    queryset = InspectionOfMaterial.objects.all()
    lookup_field = 'material_id'
    
    def list(self, request, *args, **kwargs):
        try:
            material_id = kwargs.get('material_id')
            if not material_id:
                return Response({"status": False, "message": "Material ID not found."})
            
            queryset = self.filter_queryset(self.get_queryset()).filter(material_management=material_id).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Inspection Material List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
class ApprovedInspectionViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InspectionMaterialSerializer
    queryset = InspectionOfMaterial.objects.all()
    lookup_field = "inspection_id"
    def update(self, request, *args, **kwargs):
        
        try:
            user = self.request.user
            inspection_id = kwargs.get('inspection_id')
            is_approved_remarks = request.data.get('is_approved_remarks','')
            
            if not inspection_id:
                return Response({"status": False, "message": "Inspection ID not found."})
            
            inspection_obj = InspectionOfMaterial.objects.get(id=inspection_id)
            if not inspection_obj:
                return Response({"status": True, "message": "Inspection Data is not found"})
            
            inspection_obj.is_approved = True
            inspection_obj.is_approved_by = user
            inspection_obj.is_approved_date = datetime.now()
            if is_approved_remarks:
                inspection_obj.is_approved_remarks = is_approved_remarks
            
            add_in_approval_action = InseptionOfMaterialApprovalAction.objects.create(user = user,inspection_of_material = inspection_obj,remarks = is_approved_remarks)
            add_in_approval_action.save()
            inspection_obj.save()
            
            serializer = self.serializer_class(inspection_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Inspection Material updated successfully.", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
            
                
class ProjectIdwisePendingMaterialsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialManagementSerializer
    queryset = MaterialManagement.objects.all()
    lookup_field = 'project_id'
    
    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            if not project_id:
                return Response({"status": False, "message": "Project ID not found."})
            
            queryset = self.filter_queryset(self.get_queryset()).filter(project=project_id, status='pending').order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Pending Material List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    
class ProjectIdwiseDeliveredMaterialsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialManagementSerializer
    queryset = MaterialManagement.objects.all()
    lookup_field = 'project_id'
    
    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            if not project_id:
                return Response({"status": False, "message": "Project ID not found."})
            
            queryset = self.filter_queryset(self.get_queryset()).filter(project=project_id, status='delivered').order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Delivered Material List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})