from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from project_module.models import *
from project_module.serializers import *
import ipdb
from user_profile.function_call import *
from datetime import datetime
import pandas as pd
from django.core.files.storage import default_storage
from openpyxl import load_workbook
from rest_framework.views import APIView

class ProjectExpenseCreateViewset(viewsets.ModelViewSet):
    queryset = ExpenseTracking.objects.all()
    serializer_class = ExpenseTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            project_id = request.data.get('project_id')
            category_id = request.data.get('category_id')
            expense_name = request.data.get('expense_name')
            expense_amount = request.data.get('expense_amount')
            notes = request.data.get('notes')

            expense_document_attachments = request.FILES.getlist('expense_document_attachments')  # Handle multiple files
            # Validation checks
            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})
            project = Project.objects.get(id=project_id)
            if not project:
                return Response({"status": False, "message": "Project not found", "data": []})

            if not category_id:
                return Response({"status": False, "message": "Category Id is required", "data": []})
            category = LandCategory.objects.get(id=category_id)
            if not category:
                return Response({"status": False, "message": "Category not found", "data": []})

            if not expense_name:
                return Response({"status": False, "message": "Expense name is required", "data": []})
            if not expense_amount:
                return Response({"status": False, "message": "Expense amount is required", "data": []})
            expense_obj = ExpenseTracking.objects.create(
                user=user, project=project, category=category, 
                expense_name=expense_name, expense_amount=expense_amount, 
                notes=notes
            )
            if expense_document_attachments:
                for file in expense_document_attachments:
                    attachment = ExpenseProjectAttachments.objects.create(
                        user=user, expense_project_attachments=file
                    )
                    expense_obj.expense_document_attachments.add(attachment)
            expense_obj.save()
            serializer = ExpenseTrackingSerializer(expense_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Expense created successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            project_id = request.query_params.get('project_id')
            if project_id:
                queryset = self.filter_queryset(self.get_queryset().filter(project_id=project_id)).order_by('-id')
            else:
                queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Expense List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class ProjectExpenseUpdateViewset(viewsets.ModelViewSet):
    queryset = ExpenseTracking.objects.all()
    serializer_class = ExpenseTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'expense_id'
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            expense_id = kwargs.get('expense_id')
            project_id = request.data.get('project_id')
            category_id = request.data.get('category_id')
            expense_name = request.data.get('expense_name')
            expense_amount = request.data.get('expense_amount')
            notes = request.data.get('notes')

            expense_document_attachments = request.FILES.getlist('expense_document_attachments') or []
            remove_expense_document_attachments = request.data.get('remove_expense_document_attachments', []) or []

            if not expense_id:
                return Response({"status": False, "message": "Expense Id is required", "data": []})
            expense_obj = ExpenseTracking.objects.get(id=expense_id)
            if not expense_obj:
                return Response({"status": False, "message": "Expense not found", "data": []})

            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})
            project = Project.objects.get(id=project_id)
            if not project:
                return Response({"status": False, "message": "Project not found", "data": []})

            if not category_id:
                return Response({"status": False, "message": "Category Id is required", "data": []})
            category = LandCategory.objects.get(id=category_id)
            if not category:
                return Response({"status": False, "message": "Category not found", "data": []})

            if not expense_name:
                return Response({"status": False, "message": "Expense name is required", "data": []})
            if not expense_amount:
                return Response({"status": False, "message": "Expense amount is required", "data": []})

            if project:
                expense_obj.project = project
            if category:
                expense_obj.category = category
            if expense_name:
                expense_obj.expense_name = expense_name
            if expense_amount:
                expense_obj.expense_amount = expense_amount
            if notes:
                expense_obj.notes = notes
            expense_obj.save()

            if expense_document_attachments:
                for file in expense_document_attachments:
                    attachment = ExpenseProjectAttachments.objects.create(user=user, expense_project_attachments=file)
                    expense_obj.expense_document_attachments.add(attachment)

            if remove_expense_document_attachments:
                if isinstance(remove_expense_document_attachments, str):
                    remove_expense_document_attachments = [int(file_id) for file_id in remove_expense_document_attachments.split(',')]
                else:
                    remove_expense_document_attachments = [int(file_id) for file_id in remove_expense_document_attachments]
                for attachment_id in remove_expense_document_attachments:
                    try:
                        attachment = ExpenseProjectAttachments.objects.get(id=attachment_id)
                        expense_obj.expense_document_attachments.remove(attachment)
                        attachment.delete()
                    except ExpenseProjectAttachments.DoesNotExist:
                        continue


            serializer = ExpenseTrackingSerializer(expense_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Expense updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            expense_id = kwargs.get('expense_id')
            if not expense_id:
                return Response({"status": False, "message": "Expense Id is required", "data": []})
            expense_obj = ExpenseTracking.objects.get(id=expense_id)
            if not expense_obj:
                return Response({"status": False, "message": "Expense not found", "data": []})
            expense_obj.delete()
            return Response({"status": True, "message": "Expense deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class ProjectIdWIseGetExpenseDataViewSet(viewsets.ModelViewSet):
    queryset = ExpenseTracking.objects.all()
    serializer_class = ExpenseTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'project_id'
    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get('project_id')
            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})
            queryset = ExpenseTracking.objects.filter(project=project_id).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Expense List Successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
class ClientDataCreateViewset(viewsets.ModelViewSet):
    queryset = ClientDetails.objects.all()
    serializer_class = ClientDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            project_id = request.data.get('project_id')
            client_name = request.data.get('client_name')
            contact_number = request.data.get('contact_number')
            email = request.data.get('email')
            gst = request.data.get('gst')
            pan_number = request.data.get('pan_number')
            msme_certificate = request.FILES.getlist('msme_certificate') or []
            adhar_card = request.FILES.getlist('adhar_card') or []
            pan_card = request.FILES.getlist('pan_card') or []
            third_authority_adhar_card_attachments = request.FILES.getlist('third_authority_adhar_card_attachments') or []
            third_authortity_pan_card_attachments = request.FILES.getlist('third_authortity_pan_card_attachments') or []
            captive_rec_nonrec_rpo = request.data.get('captive_rec_nonrec_rpo') or []
            declaration_of_getco = request.data.get('declaration_of_getco') or []
            undertaking_geda = request.data.get('undertaking_geda') or []
            authorization_to_epc = request.data.get('authorization_to_epc') or []
            last_3_year_turn_over_details = request.data.get('last_3_year_turn_over_details') or []
            factory_end = request.data.get('factory_end') or []
            cin = request.data.get('cin') or []
            moa_partnership = request.data.get('moa_partnership') or []
            board_authority_signing = request.data.get('board_authority_signing') or []


            if not client_name:
                return Response({"status": False, "message": "Client name is required", "data": []})

            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})

            project = Project.objects.get(id=project_id)
            if not project:
                return Response({"status": False, "message": "Project not found", "data": []})

            if not email:
                return Response({"status": False, "message": "Email not found", "data": []})
            
            client_obj = ClientDetails.objects.create(
                user=user,
                project=project,
                client_name=client_name,
                contact_number=contact_number,
                email=email,
                gst=gst,
                pan_number=pan_number,
                captive_rec_nonrec_rpo=captive_rec_nonrec_rpo,
                declaration_of_getco=declaration_of_getco,
                undertaking_geda=undertaking_geda,
                authorization_to_epc=authorization_to_epc,
                last_3_year_turn_over_details=last_3_year_turn_over_details,
                factory_end=factory_end,
                cin=cin,
                moa_partnership=moa_partnership,
                board_authority_signing=board_authority_signing,
                is_client_created=True
            )

            if msme_certificate:
                for file in msme_certificate:
                    attachment = MsMeCertificateAttachments.objects.create(user=user, msme_certificate_attachments=file)
                    client_obj.msme_certificate_attachments.add(attachment)

            if adhar_card:
                for file in adhar_card:
                    attachment = AdharCardAttachments.objects.create(user=user, adhar_card_attachments=file)
                    client_obj.adhar_card_attachments.add(attachment)

            if pan_card:
                for file in pan_card:
                    attachment = PanCardAttachments.objects.create(user=user, pan_card_attachments=file)
                    client_obj.pan_card_attachments.add(attachment)

            if third_authority_adhar_card_attachments:
                for file in third_authority_adhar_card_attachments:
                    attachment = ThirdAuthorityAdharCardAttachments.objects.create(user=user, third_authority_adhar_card_attachments=file)
                    client_obj.third_authority_adhar_card_attachments.add(attachment)

            if third_authortity_pan_card_attachments:
                for file in third_authortity_pan_card_attachments:
                    attachment = ThirdAuthorityPanCardAttachments.objects.create(user=user, third_authority_pan_card_attachments=file)
                    client_obj.third_authority_pan_card_attachments.add(attachment)


            serializer = self.serializer_class(client_obj,context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Client Created Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Client List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class ProjectClientUpdateViewset(viewsets.ModelViewSet):
    queryset = ClientDetails.objects.all()
    serializer_class = ClientDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'client_id'

    def update(self, request, *args, **kwargs):
        try:
            client_id = kwargs.get('client_id')
            if not client_id:
                return Response({"status": False, "message": "Client Id is required", "data": []})
            client_obj = ClientDetails.objects.get(id=client_id)

            if not client_obj:
                return Response({"status": False, "message": "Client not found", "data": []})

            client_name = request.data.get('client_name')
            contact_number = request.data.get('contact_number')
            email = request.data.get('email')
            gst = request.data.get('gst').upper()
            pan_number = request.data.get('pan_number').upper()

            msme_certificate = request.FILES.getlist('msme_certificate') or []
            adhar_card = request.FILES.getlist('adhar_card') or []
            pan_card = request.FILES.getlist('pan_card') or []
            third_authority_adhar_card_attachments = request.FILES.getlist('third_authority_adhar_card_attachments') or []
            third_authortity_pan_card_attachments = request.FILES.getlist('third_authortity_pan_card_attachments') or []

            remove_msme_certificate = request.data.get('remove_msme_certificate', []) or []
            remove_adhar_card = request.data.get('remove_adhar_card',[]) or []
            remove_pan_card = request.data.get('remove_pan_card',[]) or []
            remove_third_authority_adhar_card_attachments = request.data.get('remove_third_authority_adhar_card_attachments',[]) or []
            remove_third_authortity_pan_card_attachments = request.data.get('remove_third_authortity_pan_card_attachments',[]) or []

            captive_rec_nonrec_rpo = request.data.get('captive_rec_nonrec_rpo')
            declaration_of_getco = request.data.get('declaration_of_getco')
            undertaking_geda = request.data.get('undertaking_geda')
            authorization_to_epc = request.data.get('authorization_to_epc')
            last_3_year_turn_over_details = request.data.get('last_3_year_turn_over_details')
            factory_end = request.data.get('factory_end')
            cin = request.data.get('cin')
            moa_partnership = request.data.get('moa_partnership')
            board_authority_signing = request.data.get('board_authority_signing')

            if client_name:
                client_obj.client_name = client_name
            if contact_number:
                client_obj.contact_number = contact_number
            if email:
                client_obj.email = email
            if gst:
                client_obj.gst = gst
            if pan_number:
                client_obj.pan_number = pan_number
            if captive_rec_nonrec_rpo:
                client_obj.captive_rec_nonrec_rpo = captive_rec_nonrec_rpo
            if declaration_of_getco:
                client_obj.declaration_of_getco = declaration_of_getco
            if undertaking_geda:
                client_obj.undertaking_geda = undertaking_geda
            if authorization_to_epc:
                client_obj.authorization_to_epc = authorization_to_epc
            if last_3_year_turn_over_details:
                client_obj.last_3_year_turn_over_details = last_3_year_turn_over_details
            if factory_end:
                client_obj.factory_end = factory_end
            if cin:
                client_obj.cin = cin
            if moa_partnership:
                client_obj.moa_partnership = moa_partnership
            if board_authority_signing:
                client_obj.board_authority_signing = board_authority_signing
        

            if msme_certificate:
                for file in msme_certificate:
                    attachment = MsMeCertificateAttachments.objects.create(user=request.user, msme_certificate_attachments=file)
                    client_obj.msme_certificate_attachments.add(attachment)

            if adhar_card:
                for file in adhar_card:
                    attachment = AdharCardAttachments.objects.create(user=request.user, adhar_card_attachments=file)
                    client_obj.adhar_card_attachments.add(attachment)

            if pan_card:
                for file in pan_card:
                    attachment = PanCardAttachments.objects.create(user=request.user, pan_card_attachments=file)
                    client_obj.pan_card_attachments.add(attachment)

            if third_authority_adhar_card_attachments:
                for file in third_authority_adhar_card_attachments:
                    attachment = ThirdAuthorityAdharCardAttachments.objects.create(user=request.user, third_authority_adhar_card_attachments=file)
                    client_obj.third_authority_adhar_card_attachments.add(attachment)

            if third_authortity_pan_card_attachments:
                for file in third_authortity_pan_card_attachments:
                    attachment = ThirdAuthorityPanCardAttachments.objects.create(user=request.user, third_authority_pan_card_attachments=file)
                    client_obj.third_authority_pan_card_attachments.add(attachment)

            if remove_msme_certificate:
                if isinstance(remove_msme_certificate, str):
                    remove_msme_certificate = [int(file_id) for file_id in remove_msme_certificate.split(',')]
                else:
                    remove_msme_certificate = [int(file_id) for file_id in remove_msme_certificate]
                for attachment_id in remove_msme_certificate:
                    attachment = MsMeCertificateAttachments.objects.get(id=attachment_id)
                    client_obj.msme_certificate_attachments.remove(attachment)
                    attachment.delete()

            if remove_adhar_card:
                if isinstance(remove_adhar_card, str):
                    remove_adhar_card = [int(file_id) for file_id in remove_adhar_card.split(',')]
                else:
                    remove_adhar_card = [int(file_id) for file_id in remove_adhar_card]
                for attachment_id in remove_adhar_card:
                    attachment = AdharCardAttachments.objects.get(id=attachment_id)
                    client_obj.adhar_card_attachments.remove(attachment)
                    attachment.delete()

            if remove_pan_card:
                if isinstance(remove_pan_card, str):
                    remove_pan_card = [int(file_id) for file_id in remove_pan_card.split(',')]
                else:
                    remove_pan_card = [int(file_id) for file_id in remove_pan_card]
                for attachment_id in remove_pan_card:
                    attachment = PanCardAttachments.objects.get(id=attachment_id)
                    client_obj.pan_card_attachments.remove(attachment)
                    attachment.delete()

            if remove_third_authority_adhar_card_attachments:
                if isinstance(remove_third_authority_adhar_card_attachments, str):
                    remove_third_authority_adhar_card_attachments = [int(file_id) for file_id in remove_third_authority_adhar_card_attachments.split(',')]
                else:
                    remove_third_authority_adhar_card_attachments = [int(file_id) for file_id in remove_third_authority_adhar_card_attachments]
                for attachment_id in remove_third_authority_adhar_card_attachments:
                    attachment = ThirdAuthorityAdharCardAttachments.objects.get(id=attachment_id)
                    client_obj.third_authority_adhar_card_attachments.remove(attachment)
                    attachment.delete()

            if remove_third_authortity_pan_card_attachments:
                if isinstance(remove_third_authortity_pan_card_attachments, str):
                    remove_third_authortity_pan_card_attachments = [int(file_id) for file_id in remove_third_authortity_pan_card_attachments.split(',')]
                else:
                    remove_third_authortity_pan_card_attachments = [int(file_id) for file_id in remove_third_authortity_pan_card_attachments]
                for attachment_id in remove_third_authortity_pan_card_attachments:
                    attachment = ThirdAuthorityPanCardAttachments.objects.get(id=attachment_id)
                    client_obj.third_authority_pan_card_attachments.remove(attachment)
                    attachment.delete()

            client_obj.save()

            serializer = self.serializer_class(client_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Client Updated Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class ProjectIdWIseGetClientDataViewSet(viewsets.ModelViewSet):
    queryset = ClientDetails.objects.all()
    serializer_class = ClientDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'project_id'

    def list(self, request, *args, **kwargs):
        try:
            project_id = kwargs.get("project_id")
            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})
            project_obj = Project.objects.get(id=project_id)
            if not project_obj:
                return Response({"status": False, "message": "Project not found", "data": []})
            client_obj = ClientDetails.objects.filter(project_id=project_id)
            if not client_obj:
                return Response({"status": False, "message": "Client not found", "data": []})
            serializer = self.serializer_class(client_obj, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Client data fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class Wo_Po_DataCreateViewset(viewsets.ModelViewSet):
    queryset = WO_PO.objects.all()
    serializer_class = Wo_PoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            project_id = request.data.get('project_id')
            loi_attachments = request.FILES.getlist('loi_attachments')
            loa_po_attachments = request.FILES.getlist('loa_po_attachments')
            epc_contract_attachments = request.FILES.getlist('epc_contract_attachments')
            omm_contact_attachments = request.FILES.getlist('omm_contact_attachments')

            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})

            if not loi_attachments:
                return Response({"status": False, "message": "LOI Attachments are required", "data": []})
            
            if not loa_po_attachments:
                return Response({"status": False, "message": "LOA/PO Attachments are required", "data": []})
            
            if not epc_contract_attachments:
                return Response({"status": False, "message": "EPC Contract Attachments are required", "data": []})
            
            if not omm_contact_attachments:
                return Response({"status": False, "message": "OMM Contact Attachments are required", "data": []})

            project_obj = Project.objects.get(id=project_id)

            if not project_obj:
                return Response({"status": False, "message": "Project not found", "data": []})

            wo_po_obj = WO_PO.objects.create(user=user, project=project_obj)

            if loi_attachments:
                for file in loi_attachments:
                    attachment = LOIAttachments.objects.create(user=request.user, loi_attachments=file)
                    wo_po_obj.loi_attachments.add(attachment)

            if loa_po_attachments:
                for file in loa_po_attachments:
                    attachment = Loa_PoAttachments.objects.create(user=request.user, loa_po_attachments=file)
                    wo_po_obj.loa_po_attachments.add(attachment)

            if epc_contract_attachments:
                for file in epc_contract_attachments:
                    attachment = Epc_ContractAttachments.objects.create(user=request.user, epc_contract_attachments=file)
                    wo_po_obj.epc_contract_attachments.add(attachment)

            if omm_contact_attachments:
                for file in omm_contact_attachments:
                    attachment = OMMContactAttachments.objects.create(user=request.user, omm_contact_attachments=file)
                    wo_po_obj.omm_contact_attachments.add(attachment)

            # Serialize and return response
            serializer = self.serializer_class(wo_po_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "WO/PO Updated Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
            

    def list(self, request, *args, **kwargs):
        try:
            project_id = request.query_params.get('project_id')
            if project_id:
                queryset = self.filter_queryset(self.get_queryset().filter(project_id=project_id)).order_by('-id')
            else:
                queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "WO/PO List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class Wo_Po_DataUpdateViewset(viewsets.ModelViewSet):
    queryset = WO_PO.objects.all()
    serializer_class = Wo_PoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'wo_po_id'
    
    def update(self, request, *args, **kwargs):
        try:
            wo_po_id = kwargs.get('wo_po_id')
            if not wo_po_id:
                return Response({"status": False, "message": "WO/PO Id is required", "data": []})
            loi_attachments = request.FILES.getlist('loi_attachments')
            loa_po_attachments = request.FILES.getlist('loa_po_attachments')
            epc_contract_attachments = request.FILES.getlist('epc_contract_attachments')
            omm_contact_attachments = request.FILES.getlist('omm_contact_attachments')

            if not loi_attachments:
                return Response({"status": False, "message": "LOI Attachments are required", "data": []})
            
            if not loa_po_attachments:
                return Response({"status": False, "message": "LOA/PO Attachments are required", "data": []})
            
            if not epc_contract_attachments:
                return Response({"status": False, "message": "EPC Contract Attachments are required", "data": []})
            
            if not omm_contact_attachments:
                return Response({"status": False, "message": "OMM Contact Attachments are required", "data": []})

            wo_po_obj = WO_PO.objects.get(id=wo_po_id)

            if not wo_po_obj:
                return Response({"status": False, "message": "WO/PO not found", "data": []})
            
            if loi_attachments:
                wo_po_obj.loi_attachments.clear()
                for file in loi_attachments:
                    attachment = LOIAttachments.objects.create(user=request.user, loi_attachments=file)
                    wo_po_obj.loi_attachments.add(attachment)

            if loa_po_attachments:
                wo_po_obj.loa_po_attachments.clear()
                for file in loa_po_attachments:
                    attachment = Loa_PoAttachments.objects.create(user=request.user, loa_po_attachments=file)
                    wo_po_obj.loa_po_attachments.add(attachment)

            if epc_contract_attachments:
                wo_po_obj.epc_contract_attachments.clear()
                for file in epc_contract_attachments:
                    attachment = Epc_ContractAttachments.objects.create(user=request.user, epc_contract_attachments=file)
                    wo_po_obj.epc_contract_attachments.add(attachment)

            if omm_contact_attachments:
                wo_po_obj.omm_contact_attachments.clear()
                for file in omm_contact_attachments:
                    attachment = OMMContactAttachments.objects.create(user=request.user, omm_contact_attachments=file)
                    wo_po_obj.omm_contact_attachments.add(attachment)

            serializer = self.serializer_class(wo_po_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "WO/PO Updated Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            wo_po_id = kwargs.get('wo_po_id')
            if not wo_po_id:
                return Response({"status": False, "message": "WO/PO Id is required", "data": []})
            wo_po_obj = WO_PO.objects.get(id=wo_po_id)
            if not wo_po_obj:
                return Response({"status": False, "message": "WO/PO not found", "data": []})
            wo_po_obj.delete()
            return Response({"status": True, "message": "WO/PO deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        user = self.request.user
        company_name = request.data.get('company_name')

        if not company_name:
            return Response({"status": False, "message": "company_name is required"})
        if Company.objects.filter(company_name=company_name).exists():
            return Response({"status": False, "message": "A company with this name already exists"})
        try:
            company_obj = Company.objects.create(user=user, company_name=company_name)

            serializer = self.serializer_class(company_obj)
            data = {'id':serializer.data['id'],
                    company_name:serializer.data['company_name'],
                    'created_at':serializer.data['created_at'],
                    }
            return Response({"status": True, "message": "Company Created Successfully", "data": data})
    
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return Response({"status": True, "message": "Company List Successfully", "data": data})
    
    def update(self, request, *args, **kwargs):
        
        try:

            company_id = self.kwargs.get('id')
            if not company_id:
                return Response({"status": False, "message": "companyid not found."})
            
            company_obj = self.get_object()
            company_name = request.data.get('company_name')

            if not company_name:
                return Response({"status": False, "message": "company_name is required"})
            
            if Company.objects.filter(company_name=company_name).exclude(id=company_obj.id).exists():
                return Response({"status": False, "message": "A company with this name already exists"})

            company_obj.company_name = company_name
            company_obj.save()

            serializer = self.serializer_class(company_obj)
            data = {'id':serializer.data['id'],
                    company_name:serializer.data['company_name'],
                    'updated_at':serializer.data['updated_at'],
                    }
            return Response({"status": True, "message": "Company Updated Successfully", "data": data})

        except Company.DoesNotExist:
            return Response({"status": False, "message": "Company not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def destroy(self, request, *args, **kwargs):
        try:
            company_obj = self.get_object()
            company_obj.delete()

            return Response({"status": True, "message": "Company Deleted Successfully"})

        except Company.DoesNotExist:
            return Response({"status": False, "message": "Company not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class ElectricityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer

    def create(self, request, *args, **kwargs):
        try:
            electricity_line = request.data.get('electricity_line')
            if not electricity_line:
                return Response({"status": False, "message": "Electricity Line is required"})
            
            electricity_obj = Electricity.objects.create(electricity_line=electricity_line)
            serializer = self.serializer_class(electricity_obj)
            data = serializer.data
            return Response({"status": True, "message": "Electricity Line Created Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Electricity Line List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class UpdateElectricityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer
    lookuo_field = 'id'
    def update(self, request, *args, **kwargs):
        try:
            electricity_id = self.kwargs.get('id')
            electricity_obj = Electricity.objects.get(id=electricity_id)
            electricity_line = request.data.get('electricity_line')

            if not electricity_line:
                return Response({"status": False, "message": "Electricity Line is required"})
            
            
            electricity_obj.electricity_line = electricity_line
            electricity_obj.save()

            return Response({"status": True, "message": "Electricity Line Updated Successfully"})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    def destroy(self, request, *args, **kwargs):
        try:
            electricity_id = self.kwargs.get('id')
            if not electricity_id:
                return Response({"status": False, "message": "Electricity Line Id is required"})
            
            electricity_obj = Electricity.objects.get(id=electricity_id)
            electricity_obj.delete()
            return Response({"status": True, "message": "Electricity Line deleted successfully"})
        except Electricity.DoesNotExist:
            return Response({"status": False, "message": "Electricity Line not found"})
        except Exception as e:
            return Response({"status": False, "message": str(e)})

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            user = self.request.user
            landbank_id = request.data.get('landbank_id')
            company_id = request.data.get('company_id')
            electricity_line_id = request.data.get('electricity_line_id')
            project_name = request.data.get('project_name')
            start_date = parse_date(request.data.get('start_date'))
            end_date = parse_date(request.data.get('end_date'))
            # location_id = request.data.get('location_id', '')
            # location_survey = request.data.get('location_survey', '')
            alloted_land_area = request.data.get('alloted_land_area')
            available_land_area = request.data.get('available_land_area')

            # if isinstance(location_survey, str):
            #     location_survey = [int(loc_id.strip()) for loc_id in location_survey.split(',') if loc_id.strip()]  

            cod_commission_date = parse_date(request.data.get('cod_commission_date'))
            # total_area_of_project = request.data.get('total_area_of_project')
            capacity = request.data.get('capacity')
            ci_or_utility = request.data.get('ci_or_utility')
            cpp_or_ipp = request.data.get('cpp_or_ipp')
            project_activity_id = request.data.get('project_activity_id')
            spoc_user = request.data.get('spoc_user')
            project_sub_activity_ids = request.data.get('project_sub_activity_ids', [])
            project_sub_sub_activity_ids = request.data.get('project_sub_sub_activity_ids', [])
            assigned_users = request.data.get('assigned_users', [])

            # Validate individual fields
            if not landbank_id:
                return Response({"status": False, "message": "Landbank ID is required."})

            if not company_id:
                return Response({"status": False, "message": "Company ID is required."})
            
            if not electricity_line_id:
                return Response({"status": False, "message": "Electricity line ID is required."})

            if not project_name:
                return Response({"status": False, "message": "Project name is required."})

            if not start_date:
                return Response({"status": False, "message": "Start date is required."})

            if not end_date:
                return Response({"status": False, "message": "End date is required."})

            # if not location_id:
            #     return Response({"status": False, "message": "Location is required."})

            if not cod_commission_date:
                return Response({"status": False, "message": "COD commission date is required."})

            # if not total_area_of_project:
                # return Response({"status": False, "message": "Total area of project is required."})

            if not capacity:
                return Response({"status": False, "message": "Capacity is required."})

            if not ci_or_utility:
                return Response({"status": False, "message": "CI or utility is required."})

            if not cpp_or_ipp:
                return Response({"status": False, "message": "CPP or IPP is required."})

            if not project_activity_id:
                return Response({"status": False, "message": "Project choice activity is required."})

            if not spoc_user:
                return Response({"status": False, "message": "SPOC user is required."})

            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response({"status": False, "message": "Invalid company."})
            
            try:
                electricity_line = Electricity.objects.get(id=electricity_line_id)
            except Electricity.DoesNotExist:
                return Response({"status": False, "message": "Invalid electricity line."})
            
            # try:
            #     location = LandBankLocation.objects.get(id=location_id)
            # except LandBankLocation.DoesNotExist:
            #     return Response({"status": False, "message": "Invalid location."})
            
            try:
                by_spoc_user = CustomUser.objects.get(id=spoc_user)
            except CustomUser.DoesNotExist:
                return Response({"status":False,"message":"User not found"})

            # Fetch the related ProjectActivity, SubActivityName, and SubSubActivityName
            try:
                project_activity = ProjectActivity.objects.get(id=project_activity_id)
            except ProjectActivity.DoesNotExist:
                return Response({"status": False, "message": "Invalid Project Activity."})

            try:
                sub_activity_names = SubActivityName.objects.filter(id__in=project_sub_activity_ids)
            except SubActivityName.DoesNotExist:
                return Response({"status": False, "message": "Invalid SubActivity names."})

            try:
                sub_sub_activity_names = SubSubActivityName.objects.filter(id__in = project_sub_sub_activity_ids)
            except SubSubActivityName.DoesNotExist:
                return Response({"status": False, "message": "Invalid SubSubActivity names."})
            try:
                landbank_ins = LandBankMaster.objects.get(id=landbank_id)
                print(landbank_id,"==")
            except LandBankMaster.DoesNotExist:
                return Response({"status": False, "message": "Invalid Landbank ID."})

            try:
                assigned_users = CustomUser.objects.filter(id__in=assigned_users)
            except CustomUser.DoesNotExist:
                return Response({"status": False, "message": "Invalid assigned users."})
            # Create the Project instance
            project = Project.objects.create(
                user=user,
                company=company,
                electricity_line=electricity_line,
                landbank=landbank_ins,
                project_name=project_name,
                start_date=start_date,
                end_date=end_date,
                project_predicted_date=end_date,
                cod_commission_date=cod_commission_date,
                # total_area_of_project=total_area_of_project,
                capacity=capacity,
                ci_or_utility=ci_or_utility,
                cpp_or_ipp=cpp_or_ipp,
                project_activity=project_activity,
                spoc_user_id=by_spoc_user.id,
                alloted_land_area=alloted_land_area,
                available_land_area=available_land_area
            )
            serializer = self.serializer_class(project)
            data = serializer.data
            land_remaining_area = landbank_ins.remaining_land_area
            print(land_remaining_area)
            if land_remaining_area is None:
                land_remaining_area = 0.0

            landbank_ins.remaining_land_area = land_remaining_area - float(alloted_land_area)
            landbank_ins.save()
            # Add ManyToMany relationships
            # if location_survey:
            #     project.location_survey.set(location_survey)

            # Set the Many-to-Many relationships for sub-activities and sub-sub-activities
            if sub_activity_names:
                project.project_sub_activity.set(sub_activity_names)

            if sub_sub_activity_names:
                project.project_sub_sub_activity.set(sub_sub_activity_names)

            if assigned_users:
                project.assigned_users.set(assigned_users)
                
            return Response({"status": True,"message": "Project created successfully","data": data})

        except Exception as e:
            return Response({"status": False,"message": f"Error creating project: {str(e)}","data": []})
        
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
        
    #     try:
    #         if queryset.exists():
    #             project_data = []
    #             for obj in queryset:
    #                 context = {'request': request}
    #                 serializer = ProjectSerializer(obj,context=context)
    #                 project_data.append(serializer.data)
                    
    #             count = len(project_data)
    #             return Response({
    #                 "status": True,
    #                 "message": "Project data fetched successfully",
    #                 'total_page': 1,
    #                 'total': count,
    #                 'data': project_data
    #             })
    #         else:
    #             return Response({
    #                 "status": True,
    #                 "message": "No milestone found",
    #                 "total_page": 0,
    #                 "total": 0,
    #                 "data": []
    #             })
    #     except Exception as e:
    #         return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

    def list(self, request, *args, **kwargs):
        company_id = request.query_params.get('company_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        user_id = request.query_params.get('user_id')
        project_activity_id = request.query_params.get('project_activity_id')

        try:
            projects = Project.objects.all().order_by('-created_at')

            if company_id and user_id:
                projects = projects.filter(company_id=company_id, user_id=user_id)

            elif company_id:
                projects = projects.filter(company_id=company_id)

            elif user_id:
                projects = projects.filter(user_id=user_id)

            if start_date and end_date:
                start_date_obj, end_date_obj, error = validate_dates(start_date, end_date)
                if error:
                    return Response({"status": False, "message": error, "data": []})
                if start_date_obj and end_date_obj:
                    projects = projects.filter(created_at__range=[start_date_obj, end_date_obj])

            if project_activity_id:
                projects = projects.filter(project_activity_id=project_activity_id)

            if not projects.exists():
                return Response({"status": True, "message": "No project found", "data": []})

            total_count = projects.count()

            context = {'request': request}
            serializer = ProjectSerializer(projects, context=context, many=True)

            return Response({"status": True,"message": "Project data fetched successfully","total_count": total_count,"data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})


class ProjectUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    def update(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_id")
            project_name = request.data.get('project_name')
            start_date = parse_date(request.data.get('start_date'))
            end_date = parse_date(request.data.get('end_date'))
            project_predicted_date = parse_date(request.data.get('project_predicted_date'))
            location_id = request.data.get('location_id', '')
            location_survey = request.data.get('location_survey', '')
            available_land_area = request.data.get('available_land_area')
            alloted_land_area = request.data.get('alloted_land_area')
            if isinstance(location_survey, str):
                location_survey = [int(loc_id.strip()) for loc_id in location_survey.split(',') if loc_id.strip()]
            cod_commission_date = parse_date(request.data.get('cod_commission_date'))
            # total_area_of_project = request.data.get('total_area_of_project')
            capacity = request.data.get('capacity')
            ci_or_utility = request.data.get('ci_or_utility')
            cpp_or_ipp = request.data.get('cpp_or_ipp')
            project_choice_activity = request.data.get('project_choice_activity')
            electricity_line_id = request.data.get('electricity_line_id')
            spoc_user = request.data.get('spoc_user')

            if not Project.objects.filter(id=project_id).exists():
                return Response({"status": False, "message": "Project ID not found"})

            project_object = Project.objects.get(id=project_id)

            if project_name:
                project_object.project_name = project_name
            if available_land_area:
                project_object.available_land_area = available_land_area
            if alloted_land_area:
                project_object.alloted_land_area = alloted_land_area
            if start_date:
                project_object.start_date = start_date
            if end_date:
                project_object.end_date = end_date
            if project_predicted_date:
                project_object.project_predicted_date = project_predicted_date
            if location_id:
                try:
                    location = LandBankLocation.objects.get(id=location_id)
                    project_object.location_name = location
                except LandBankLocation.DoesNotExist:
                    return Response({"status": False, "message": "Invalid location."})
            if cod_commission_date:
                project_object.cod_commission_date = cod_commission_date
            # if total_area_of_project:
                # project_object.total_area_of_project = total_area_of_project
            if capacity:
                project_object.capacity = capacity
            if ci_or_utility:
                project_object.ci_or_utility = ci_or_utility
            if cpp_or_ipp:
                project_object.cpp_or_ipp = cpp_or_ipp
            if project_choice_activity:
                project_object.project_choice_activity = project_choice_activity
            if electricity_line_id:
                try:
                    electricity_line = Electricity.objects.get(id=electricity_line_id)
                    project_object.electricity_line = electricity_line
                except Electricity.DoesNotExist:
                    return Response({"status": False, "message": "Electricity line not found"})
            if spoc_user:
                try:
                    spoc_user_object = CustomUser.objects.get(id=spoc_user)
                    project_object.spoc_user = spoc_user_object
                except CustomUser.DoesNotExist:
                    return Response({"status": False, "message": "User not found"})

            # Update the project instance
            project_object.save()

            # Update ManyToMany relationships
            if location_survey:
                project_object.location_survey.set(location_survey)

            return Response({"status": True, "message": "Project updated successfully"})

        except Exception as e:
            return Response({"status": False, "message": f"Error updating project: {str(e)}", "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_id")
            if not project_id:
                return Response({"status": False, "message": "Project ID is required."})
            
            project_data = Project.objects.get(id=project_id)
            
            if not project_data:
                return Response({"status": False, "message": "Project not found."})
            
            land_bank_instance = project_data.landbank
            alloted_area = project_data.alloted_land_area

            if land_bank_instance and alloted_area:
                updated_remaining_land_area = float(land_bank_instance.remaining_land_area) + float(alloted_area)
                land_bank_instance.remaining_land_area = updated_remaining_land_area
                land_bank_instance.save()

            project_data.delete()

            return Response({"status": True, "message": "Project deleted successfully."})

        except Exception as e:
            return Response({"status": False, "message": f"Error deleting project: {str(e)}", "data": []})
  
class ProjectIdWIseGetProjectDataViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    def list(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_id")
            if not project_id:
                return Response({"status": False, "message": "Project ID is required."})
            
            project_data = Project.objects.get(id=project_id)

            if not project_data:
                return Response({"status": False, "message": "Project not found."})
            
            
            serializer = ProjectSerializer(project_data,context = {'request': request})
            data = serializer.data
            
            return Response({"status": True, "message": "Project data fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": f"Error fetching project data: {str(e)}", "data": []})



class ActiveDeactiveProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'

    def update(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get("project_id")
            if not project_id:
                return Response({"status": False, "message": "Project ID is required."})
            
            project_data = Project.objects.get(id=project_id)

            if not project_data:
                return Response({"status": False, "message": "Project not found."})
            
            if project_data.is_active:
                project_data.is_active = False
                project_data.save()
                return Response({"status": True, "message": "Project deactivated successfully."})
            elif not project_data.is_active:
                project_data.is_active = True
                project_data.save()
                return Response({"status": True, "message": "Project activated successfully."})
            else:
                return Response({"status": False, "message": "Project status is not valid."})
        except Exception as e:
            return Response({"status": False, "message": f"Error updating project status: {str(e)}", "data": []})


class GetActiveProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = Project.objects.filter(is_active=True)
            project_data = []
            for obj in queryset:
                serializer = self.serializer_class(obj)
                project_data.append(serializer.data)
            
            count = len(project_data)
            return Response({
                "status": True,
                "message": "Active project data fetched successfully",
                'total': count,
                'data': project_data
            })
        except Exception as e:
            return Response({"status": False, "message": f"Error fetching active projects: {str(e)}", "data": []})

class NumberofProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = Project.objects.all()
            count = len(queryset)
            return Response({
                "status": True,
                "message": "Total number of projects fetched successfully",
                'total number of project': count
            })
        except Exception as e:
            return Response({"status": False, "message": f"Error fetching total number of projects: {str(e)}", "data": []})


class ProjectMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProjectMilestone.objects.all()
    serializer_class = ProjectMilestoneSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            milestone_name = request.data.get('milestone_name')
            project_id = request.data.get('project')
            project_main_activity = request.data.get('project_main_activity')
            project_sub_activity = request.data.get('project_sub_activity', [])
            project_sub_sub_activity = request.data.get('project_sub_sub_activity', [])
            start_date = parse_date(request.data.get('start_date'))
            end_date = parse_date(request.data.get('end_date'))
            milestone_description = request.data.get('milestone_description')
            is_depended = request.data.get('is_depended', None)
            if isinstance(is_depended, str):
                is_depended = is_depended.lower() == "true"

            if not milestone_name:
                return Response({"status": False, "message": "Milestone Name is required."})

            if not project_id:
                return Response({"status": False, "message": "Project ID is required."})

            if not start_date:
                return Response({"status": False, "message": "Start date is required."})

            if not end_date:
                return Response({"status": False, "message": "End date is required."})

            if not milestone_description:
                return Response({"status": False, "message": "Milestone description is required."})
            
            if is_depended is None:
                return Response({"status": False, "message": "Is Depended is required."})
            
            if is_depended == "true":
                if project_sub_sub_activity:
                    if project_main_activity is None:
                        return Response({"status": False, "message": "Project Main Activity is required when Project Sub Sub Activity is provided."})
                    if project_sub_activity is None:
                        return Response({"status": False, "message": "Project Sub Activity is required when Project Sub Sub Activity is provided."})
                elif project_sub_activity:
                    if not project_main_activity is None:
                        return Response({"status": False, "message": "Project Main Activity is required when Project Sub Activity is provided."})
                
            else:
                if not (project_sub_sub_activity or project_sub_activity or project_main_activity):
                    return Response({"status": False, "message": "Project Main Activity, Project Sub Activity, or Project Sub Sub Activity is required."})

            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({"status": False, "message": "Invalid project."})
            
            if project_main_activity:
                try:
                    project_main_activity = ProjectActivity.objects.get(id=project_main_activity)
                except ProjectActivity.DoesNotExist:
                    return Response({"status": False, "message": "Invalid Project Main Activity."})

            milestone = ProjectMilestone.objects.create(
                user=user,
                project=project,
                project_main_activity=project_main_activity,
                start_date=start_date,
                end_date=end_date,
                milestone_name = milestone_name,
                milestone_description=milestone_description,
                is_depended=is_depended,
            )
            if project_sub_activity:
                milestone.project_sub_activity.set(project_sub_activity)

            if project_sub_sub_activity:
                milestone.project_sub_sub_activity.set(project_sub_sub_activity)

            if project.project_predicted_date is None or end_date > project.project_predicted_date:
                project.project_predicted_date = end_date
                project.save()

            return Response(
                {
                    "status": True,
                    "message": "Milestone created successfully",
                })

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": f"Error creating milestone: {str(e)}",
                    "data": [],
                })
    
    def list(self, request, *args, **kwargs):
        try:
            project_id = request.query_params.get('project_id')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            queryset = self.filter_queryset(self.get_queryset())
            
            if project_id:
                queryset = queryset.filter(project_id=project_id)
            
            if start_date:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    queryset = queryset.filter(created_at__gte=start_date)
                except ValueError:
                    return Response({"status": False, "message": "Invalid start_date format. Please use YYYY-MM-DD."})
            
            if end_date:
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                    queryset = queryset.filter(created_at__lte=end_date)
                except ValueError:
                    return Response({"status": False, "message": "Invalid end_date format. Please use YYYY-MM-DD."})

            if queryset.exists():
                projectmilstone_data = []
                for obj in queryset:
                    context = {'request': request}
                    serializer = ProjectMilestoneSerializer(obj, context=context)
                    projectmilstone_data.append(serializer.data)

                count = len(projectmilstone_data)
                return Response({"status": True,"message": "milestones fetched successfully.",'total': count,'data': projectmilstone_data})
            else:
                return Response({"status": True, "message": "No milestones found."})

        except Exception as e:
            return Response({"status": False,'message': 'Something went wrong','error': str(e)})
        
class IdWiseProjectMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer

    def list(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get("milestone_id")
            if not milestone_id:
                return Response({"status": False, "message": "milestone_id ID is required."})
            
            queryset = ProjectMilestone.objects.filter(id=milestone_id)
            
            if queryset.exists():
                projectmilstone_data = []
                for obj in queryset:
                    context = {'request': request}
                    serializer = MilestonedataActivitySerializer(obj, context=context)
                    projectmilstone_data.append(serializer.data)
                    count = len(projectmilstone_data)
                return Response({"status": True,"message": "milestone data fetched successfully",'total': count,'data': projectmilstone_data})
            else:
                return Response({"status": True, "message": "No milestone found."})
        except Exception as e:
            return Response({"status": False,'message': 'Something went wrong','error': str(e)})


class ActiveDeactiveMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer

    def update(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get("milestone_id")
            if not milestone_id:
                return Response({"status": False, "message": "Milestone ID is required."})
            
            milestone_data = ProjectMilestone.objects.get(id=milestone_id)
            if not milestone_data:
                return Response({"status": False, "message": "Milestone not found."})
            
            if milestone_data.is_active:
                milestone_data.is_active = False
                milestone_data.save()
                return Response({"status": True, "message": "Milestone deactivated successfully."})
            elif not milestone_data.is_active:
                milestone_data.is_active = True
                milestone_data.save()
                return Response({"status": True, "message": "Milestone activated successfully."})
        except Exception as e:
            return Response({"status": False, "message": f"Error updating milestone status: {str(e)}", "data": []})
        

class GetActiveMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = ProjectMilestone.objects.filter(is_active=True)
            
            if queryset.exists():
                projectmilstone_data = []
                for obj in queryset:
                    context = {'request': request}
                    serializer = ProjectMilestoneSerializer(obj, context=context)
                    projectmilstone_data.append(serializer.data)
                    
                count = len(projectmilstone_data)
                return Response({"status": True,"message": "Milestone data fetched successfully",'total': count,'data': projectmilstone_data})
            else:
                return Response({"status": True,"message": "No active milestone found","total_page": 0,"total": 0,"data": []})
        except Exception as e:
            return Response({"status": False, "message": f"Error fetching active milestones: {str(e)}", "data": []})


class ProjectMilestoneUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'milestone_id'

    def update(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get("milestone_id")
            milestone_description = request.data.get('milestone_description')
            start_date = parse_date(request.data.get('start_date'))
            end_date = parse_date(request.data.get('end_date'))
            milestone_name = request.data.get('milestone_name')

            if not ProjectMilestone.objects.filter(id=milestone_id).exists():
                return Response({"status": False, "message": "Milestone id not found"})

            milestone_object = ProjectMilestone.objects.get(id=milestone_id)

            if milestone_name:
                milestone_object.milestone_name = milestone_name 
            if milestone_description:
                milestone_object.milestone_description = milestone_description
            if start_date:
                milestone_object.start_date = start_date
            if end_date:
                milestone_object.end_date = end_date

            milestone_object.save()

            return Response({"status": True, "message": "Milestone updated successfully"})

        except Exception as e:
            return Response({"status": False, "message": "Something went wrong", "error": str(e)})
        
class ProjectMilestoneCompletedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer

    def update(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get("milestone_id")
            milestone_data = ProjectMilestone.objects.get(id=milestone_id)
            
            if not milestone_data:
                return Response({"status": False, "message": "Milestone not found."})
            
            if not milestone_data.is_completed:
                milestone_data.is_completed = True
                milestone_data.completed_at = datetime.now()
                milestone_data.milestone_status = "completed"
                milestone_data.save()
                if milestone_data.end_date:
                    end_date_naive = milestone_data.end_date.replace(tzinfo=None) if milestone_data.end_date.tzinfo else milestone_data.end_date
                    completed_at_naive = milestone_data.completed_at.replace(tzinfo=None) if milestone_data.completed_at.tzinfo else milestone_data.completed_at
                    days_completed_before = (end_date_naive - completed_at_naive).days
                    days_completed_after = (completed_at_naive - end_date_naive).days
                    project = milestone_data.project
                    print(days_completed_before, "days_completed_before")
                    print(days_completed_after, "days_completed_after")
                    if days_completed_before > 0:
                        new_predicted_date = project.end_date - timedelta(days=days_completed_before)
                        print(new_predicted_date, "new_predicted_date")
                        project.project_predicted_date = new_predicted_date
                        project.save()
                    elif days_completed_after > 0:
                        new_predicted_date = project.end_date + timedelta(days=days_completed_after)
                        print("New predicted date (after):", new_predicted_date)
                        project.project_predicted_date = new_predicted_date
                        project.save()
                return Response({"status": True, "message": "Milestone status updated to Completed."})
            else:
                return Response({"status": False, "message": "Milestone is already marked as completed."})
        except Exception as e:
            return Response({"status": False, "message": f"Error updating milestone status: {str(e)}", "data": []})

class UpcomingMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = ProjectMilestone.objects.filter(start_date__gt=datetime.now())
            
            if queryset.exists():
                projectmilstone_data = []
                for obj in queryset:
                    context = {'request': request}
                    serializer = ProjectMilestoneSerializer(obj, context=context)
                    projectmilstone_data.append(serializer.data)
                    
                count = len(projectmilstone_data)
                return Response({"status": True,"message": "Milestone data fetched successfully",'total': count,'data': projectmilstone_data})
            else:
                return Response({"status": True,"message": "No upcoming milestone found","total_page": 0,"total": 0,"data": []})
        except Exception as e:
            return Response({"status": False, "message": f"Error fetching upcoming milestones: {str(e)}", "data": []})
        
class ProjectMilestoneStartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMilestoneSerializer

    def update(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get("milestone_id")
            milestone_data = ProjectMilestone.objects.get(id=milestone_id)
            
            if not milestone_data:
                return Response({"status": False, "message": "Milestone not found."})
            
            if milestone_data.is_started:
                return Response({"status": False, "message": "Milestone is already marked as started."})
            else:
                milestone_data.is_started = True
                milestone_data.started_at = datetime.now()
                milestone_data.milestone_status = "in_progress"
                milestone_data.save()
                return Response({"status": True, "message": "Milestone status updated to Started."})
        except Exception as e:
            return Response({"status": False, "message": f"Error updating milestone status: {str(e)}", "data": []})
        
        
class AddDrawingandDesignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all().order_by('-id')
    
#     def create(self, request, *args, **kwargs):
#         try:
#             user = self.request.user
#             project_id = request.data.get('project_id')
#             assign_to_user = request.data.get('assign_to_user')
#             drawing_and_design_attachments = request.data.getlist('drawing_and_design_attachments', []) or []
#             discipline = request.data.get('discipline')
#             block = request.data.get('block')
#             drawing_number = request.data.get('drawing_number')
#             auto_drawing_number = request.data.get('auto_drawing_number')
#             name_of_drawing = request.data.get('name_of_drawing')
#             drawing_category = request.data.get('drawing_category')
#             type_of_approval = request.data.get('type_of_approval')
#             approval_status = request.data.get('approval_status')
#             try:
#                 project = Project.objects.get(id=project_id)
#             except Project.DoesNotExist:
#                 return Response({"status": False, "message": "Project not found", "data": []})
            
#             try:
#                 if not assign_to_user:
#                     return Response({"status": False, "message": "Assign to user is required", "data": []})
#                 assign_to_user = CustomUser.objects.get(id=assign_to_user)
#             except CustomUser.DoesNotExist:
#                 return Response({"status": False, "message": "Assign to user not found", "data": []})
        
#             if not discipline:
#                 return Response({"status": False, "message": "Discipline is required", "data": []})
#             if not block:
#                 return Response({"status": False, "message": "Block is required", "data": []})
#             if not drawing_number:
#                 return Response({"status": False, "message": "Drawing number is required", "data": []})
#             if not auto_drawing_number:
#                 return Response({"status": False, "message": "Auto drawing number is required", "data": []})
#             if not name_of_drawing:
#                 return Response({"status": False, "message": "Name of drawing is required", "data": []})
#             if not drawing_category:
#                 return Response({"status": False, "message": "Drawing category is required", "data": []})
#             if not type_of_approval:
#                 return Response({"status": False, "message": "Type of approval is required", "data": []})
#             if not approval_status:
#                 return Response({"status": False, "message": "Approval status is required", "data": []})
            
#             drawing_and_design = DrawingAndDesignManagement.objects.create(
#                 project=project,
#                 user=user,
#                 assign_to_user=assign_to_user,
#                 discipline=discipline,
#                 block=block,
#                 drawing_number=drawing_number,
#                 auto_drawing_number=auto_drawing_number,
#                 name_of_drawing=name_of_drawing,
#                 drawing_category=drawing_category,
#                 type_of_approval=type_of_approval,
#                 approval_status=approval_status
#             )
            
#             for attachment in drawing_and_design_attachments:
#                 drawing_and_design_attachments = DrawingAndDesignAttachments.objects.create(project = project, user = user, drawing_and_design_attachments = attachment)
#                 drawing_and_design.drawing_and_design_attachments.add(drawing_and_design_attachments)
                
#             drawing_and_design.save()
#             return Response({"status": True, "message": "Drawing and design added successfully", "data": []})
#         except Exception as e:
#             return Response({"status": False, "message": str(e), "data": []})
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Drawing and design List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class UploadExcelDrawingDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Get uploaded file
            file = request.FILES.get('file')
            project_id = request.data.get('project_id')
            
            if not file:
                return Response({"status": False, "message": "No file uploaded"})
            
            if not project_id:
                return Response({"status": False, "message": "Project ID is required"})
            
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({"status": False, "message": "Invalid project ID"})
            
            # Save file temporarily
            file_path = default_storage.save(file.name, file)
            
            # Load Excel file
            xls = pd.ExcelFile(default_storage.path(file_path))
            sheet_name = xls.sheet_names[0]  # Read the first sheet dynamically
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Find the header row dynamically
            expected_headers = ['Discipline', 'Block', 'Drawing / Document Number', 'Name of the Drawing / Document', 'Document Catagories:', 'Type - Approval / Information', 'Approval Status']
            header_row = None
            for i, row in df.iterrows():
                if all(col in row.values for col in expected_headers):
                    header_row = i
                    break
            
            if header_row is None:
                return Response({"status": False, "message": "Could not find header row in the uploaded file"})
            
            # Read data from detected header row
            df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=header_row + 1)
            df = df.rename(columns={
                'Discipline': 'discipline',
                'Block': 'block',
                'Drawing / Document Number': 'drawing_number',
                'Name of the Drawing / Document': 'name_of_drawing',
                'Document Catagories:': 'drawing_category',
                'Type - Approval / Information': 'type_of_approval',
                'Approval Status': 'approval_status'
            })
            
            df = df[['discipline', 'block', 'drawing_number', 'name_of_drawing', 'drawing_category', 'type_of_approval', 'approval_status']]
            df = df.dropna(subset=['drawing_number', 'name_of_drawing']).reset_index(drop=True)
            
            # Save data to the database
            drawings = []
            for _, row in df.iterrows():
                drawing = DrawingAndDesignManagement(
                    project=project,
                    user=request.user,
                    assign_to_user=None,  # Will be assigned later
                    discipline=row['discipline'],
                    block=row['block'],
                    drawing_number=row['drawing_number'],
                    name_of_drawing=row['name_of_drawing'],
                    drawing_category=row['drawing_category'],
                    type_of_approval=row['type_of_approval'],
                    approval_status=row['approval_status']
                )
                drawings.append(drawing)
            
            DrawingAndDesignManagement.objects.bulk_create(drawings)
            
            return Response({"status": True, "message": "Data uploaded successfully", "total_records": len(drawings)})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})

    
    
        
        
class DrawingandDesignUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all()
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            drawing_and_design_id = self.kwargs.get('drawing_and_design_id')
            if not drawing_and_design_id:
                return Response({"status": False, "message": "Drawing and design not found."})
            
            drawing_and_design = DrawingAndDesignManagement.objects.get(id=drawing_and_design_id)
            
            if not drawing_and_design:
                return Response({"status": True, "message": "Drawing and design Data is not found"})
            
            # Retrieve the current approval status and submitted_count
            current_approval_status = drawing_and_design.approval_status
            current_submitted_count = int(drawing_and_design.submitted_count) if drawing_and_design.submitted_count else 0
            
            # Retrieve the request data
            project_id = request.data.get('project_id')
            drawing_and_design_attachments = request.data.getlist('drawing_and_design_attachments', []) or []
            remove_drawing_and_design_attachments = request.data.get('remove_drawing_and_design_attachments_id', []) or []
            other_drawing_and_design_attachments = request.data.getlist('other_drawing_and_design_attachments', []) or []
            remove_other_drawing_and_design_attachments = request.data.get('remove_other_drawing_and_design_attachments_id', []) or []
            assign_to_user = request.data.get('assign_to_user')
            discipline = request.data.get('discipline')
            block = request.data.get('block')
            drawing_number = request.data.get('drawing_number')
            auto_drawing_number = request.data.get('auto_drawing_number')
            name_of_drawing = request.data.get('name_of_drawing')
            drawing_category = request.data.get('drawing_category')
            type_of_approval = request.data.get('type_of_approval')
            approval_status = request.data.get('approval_status')
            remarks = request.data.get('remarks')
            if approval_status in ['commented', 'approved']:
                return Response({"status": False, "message": "You cannot update the approval status to commented or approved."})
            
            remove_drawing_and_design_attachments = process_file_ids(remove_drawing_and_design_attachments)
            remove_other_drawing_and_design_attachments = process_file_ids(remove_other_drawing_and_design_attachments)
            try:
                # Update fields only if they are provided in the request
                if project_id:
                    project = Project.objects.get(id=project_id)
                    drawing_and_design.project = project
                
                if drawing_and_design_attachments:
                    for attachment in drawing_and_design_attachments:
                        drawing_and_design_attachments = DrawingAndDesignAttachments.objects.create(
                            project=project, user=user, drawing_and_design_attachments=attachment)
                        drawing_and_design.drawing_and_design_attachments.add(drawing_and_design_attachments)
                        
                if remove_drawing_and_design_attachments:
                    for file_id in remove_drawing_and_design_attachments:
                        try:
                            file_instance = DrawingAndDesignAttachments.objects.get(id=file_id)
                            drawing_and_design.drawing_and_design_attachments.remove(file_instance)
                            file_instance.delete()
                        except DrawingAndDesignAttachments.DoesNotExist:
                            pass
                if other_drawing_and_design_attachments:
                    for attachment in other_drawing_and_design_attachments:
                        other_drawing_and_design_attachments = OtherDrawingAndDesignAttachments.objects.create(
                            project=project, user=user, other_drawing_and_design_attachments=attachment)
                        drawing_and_design.other_drawing_and_design_attachments.add(other_drawing_and_design_attachments)
                        
                if remove_other_drawing_and_design_attachments:
                    for file_id in remove_other_drawing_and_design_attachments:
                        try:
                            file_instance = OtherDrawingAndDesignAttachments.objects.get(id=file_id)
                            drawing_and_design.other_drawing_and_design_attachments.remove(file_instance)
                            file_instance.delete()
                        except OtherDrawingAndDesignAttachments.DoesNotExist:
                            pass
                        
                if assign_to_user:
                    assign_to_user = CustomUser.objects.get(id=assign_to_user)
                    drawing_and_design.assign_to_user = assign_to_user
                
                if discipline:
                    drawing_and_design.discipline = discipline
                
                if block:
                    drawing_and_design.block = block
                
                if drawing_number:
                    drawing_and_design.drawing_number = drawing_number
                
                if auto_drawing_number:
                    drawing_and_design.auto_drawing_number = auto_drawing_number
                
                if name_of_drawing:
                    drawing_and_design.name_of_drawing = name_of_drawing
                
                if drawing_category:
                    drawing_and_design.drawing_category = drawing_category
                
                if type_of_approval:
                    drawing_and_design.type_of_approval = type_of_approval
                
                if approval_status:
                    drawing_and_design.approval_status = approval_status
                
                # Only increment submitted_count if approval_status is 'submitted' 
                # if approval_status == 'submitted' and current_approval_status == 'commented':
                #     drawing_and_design.submitted_count = current_submitted_count + 1
                #     drawing_and_design.is_submitted = True
                #     resubmitted_actions = DrawingAndDesignReSubmittedActions.objects.create(drawing_and_design = drawing_and_design,project = project , user=user, remarks = remarks,submitted_count = current_submitted_count + 1)
                #     resubmitted_actions.save()
                    
                    
                # # Don't update submitted_count if approval_status is 'not_submitted'
                # if approval_status in ['not_submitted', 'commented', 'approved'] and current_approval_status == 'not_submitted':
                #     drawing_and_design.submitted_count = str(current_submitted_count)  # Keep it unchanged
                drawing_and_design.save()
                
                return Response({"status": True, "message": "Drawing and design updated successfully", "data": []})
            except Exception as e:
                return Response({"status": False, "message": str(e), "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

        

class ApprovalOrCommentedActionOnDrawingandDesignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all()
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            drawing_and_design_id = self.kwargs.get('drawing_and_design_id')
            if not drawing_and_design_id:
                return Response({"status": False, "message": "Drawing and design not found."})
            
            drawing_and_design = DrawingAndDesignManagement.objects.get(id=drawing_and_design_id)
            
            if not drawing_and_design:
                return Response({"status": True, "message": "Drawing and design Data is not found"})
            
            approval_status = request.data.get('approval_status')
            remarks = request.data.get('remarks')
            
            if approval_status == 'approved':
                drawing_and_design.approval_status = approval_status
                drawing_and_design.is_approved = True
                approval_acions = DrawingAndDesignApprovedActions.objects.create(drawing_and_design = drawing_and_design,project = drawing_and_design.project , user=user, remarks = remarks)
                approval_acions.save()
                drawing_and_design.save()
                return Response({"status": True, "message": "Drawing and design approved successfully", "data": []})
            elif approval_status == 'commented':
                drawing_and_design.approval_status = approval_status
                drawing_and_design.is_commented = True
                drawing_and_design.is_submitted = False
                commented_actions = DrawingAndDesignCommentedActions.objects.create(drawing_and_design = drawing_and_design,project = drawing_and_design.project , user=user, remarks = remarks)
                commented_actions.save()
                drawing_and_design.save()
                return Response({"status": True, "message": "Drawing and design commented successfully", "data": []})
            else:
                return Response({"status": False, "message": "Invalid approval status."})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class DrawingandDesignResubmittedActionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all()
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            drawing_and_design_id = self.kwargs.get('drawing_and_design_id')
            if not drawing_and_design_id:
                return Response({"status": False, "message": "Drawing and design not found."})
            
            drawing_and_design = DrawingAndDesignManagement.objects.get(id=drawing_and_design_id)
            
            if not drawing_and_design:
                return Response({"status": True, "message": "Drawing and design Data is not found"})
            current_submitted_count = int(drawing_and_design.submitted_count) if drawing_and_design.submitted_count else 0
            remarks = request.data.get('remarks')
            drawing_and_design.approval_status = 'submitted'
            drawing_and_design.submitted_count = current_submitted_count + 1
            re_submitted = DrawingAndDesignReSubmittedActions.objects.create(drawing_and_design = drawing_and_design,project = drawing_and_design.project , user=user, remarks = remarks,submitted_count = current_submitted_count + 1)
            re_submitted.save()
            drawing_and_design.save()
            return Response({"status": True, "message": "Drawing and design resubmitted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class ProjectIdwiseGetDrawingandDesignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all().order_by('-id')
    
    def list(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs.get('project_id')
            if not project_id:
                return Response({"status": False, "message": "Project Id is required", "data": []})
            drawing_and_design = DrawingAndDesignManagement.objects.filter(project=project_id).order_by('-id')
            serializer = DrawingandDesignSerializer(drawing_and_design, many=True, context={'request': request})
            return Response({"status": True, "message": "Drawing and design data fetched successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class DrawingIdWiseGetDrawingandDesignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DrawingandDesignSerializer
    queryset = DrawingAndDesignManagement.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            drawing_and_design_id = self.kwargs.get('drawing_and_design_id')
            if not drawing_and_design_id:
                return Response({"status": False, "message": "Drawing Id is required", "data": []})

            drawing_and_design = DrawingAndDesignManagement.objects.get(id=drawing_and_design_id)
            serializer = DrawingandDesignSerializer(drawing_and_design, context={'request': request})

            return Response({
                "status": True,
                "message": "Drawing and design data with related actions fetched successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})



class InFlowPaymentOnMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InFlowPaymentOnMilestoneSerializer
    queryset = InFlowPaymentOnMilestone.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            milestone_id = request.data.get('milestone_id')
            party_name = request.data.get('party_name')
            po_number = request.data.get('po_number')
            invoice_number = request.data.get('invoice_number')
            total_amount = request.data.get('total_amount')
            gst_amount = request.data.get('gst_amount')
            paid_amount = request.data.get('paid_amount')
            pending_amount = request.data.get('pending_amount')
            payment_date = parse_date(request.data.get('payment_date'))
            notes = request.data.get('notes')
            
            if not milestone_id:
                return Response({"status": False, "message": "Milestone Id is required", "data": []})
            if not party_name:
                return Response({"status": False, "message": "Party Name is required", "data": []})
            if not invoice_number:
                return Response({"status": False, "message": "Invoice Number is required", "data": []})
            if not total_amount:
                return Response({"status": False, "message": "Total Amount is required", "data": []})
            if not gst_amount:
                return Response({"status": False, "message": "GST Amount is required", "data": []})
            if not paid_amount:
                return Response({"status": False, "message": "Paid Amount is required", "data": []})
            if not pending_amount:
                return Response({"status": False, "message": "Pending Amount is required", "data": []})
            if not payment_date:
                return Response({"status": False, "message": "Payment Date is required", "data": []})
            milestone = ProjectMilestone.objects.get(id=milestone_id)
            if not milestone:
                return Response({"status": False, "message": "Milestone not found", "data": []})
            
            in_flow_payment = InFlowPaymentOnMilestone.objects.create(
                project = milestone.project,
                milestone=milestone,
                party_name=party_name,
                po_number=po_number,
                invoice_number=invoice_number,
                total_amount=total_amount,
                gst_amount=gst_amount,
                paid_amount=paid_amount,
                pending_amount=pending_amount,
                payment_date=payment_date,
                notes=notes
            )
            in_flow_payment.save()
            return Response({"status": True, "message": "Payment data created successfully", "data": []})
        
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = InFlowPaymentOnMilestoneSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Payment data fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
            
class UpdateInflowPaymentMiletoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InFlowPaymentOnMilestoneSerializer
    queryset = InFlowPaymentOnMilestone.objects.all()
    
    def update(self, request, *args, **kwargs):
        try:
            inflow_payment_on_milestone_id = self.kwargs.get('inflow_payment_on_milestone_id')
            if not inflow_payment_on_milestone_id:
                return Response({"status": False, "message": "Payment Id is required", "data": []})
            payment = InFlowPaymentOnMilestone.objects.get(id=inflow_payment_on_milestone_id)
            if not payment:
                return Response({"status": False, "message": "Payment not found", "data": []})
            party_name = request.data.get('party_name')
            po_number = request.data.get('po_number')
            invoice_number = request.data.get('invoice_number')
            total_amount = request.data.get('total_amount')
            gst_amount = request.data.get('gst_amount')
            paid_amount = request.data.get('paid_amount')
            pending_amount = request.data.get('pending_amount')
            payment_date = parse_date(request.data.get('payment_date'))
            notes = request.data.get('notes')
            
            if party_name:
                payment.party_name = party_name
            if po_number:
                payment.po_number = po_number
            if invoice_number:
                payment.invoice_number = invoice_number
            if total_amount:
                payment.total_amount = total_amount
            if gst_amount:
                payment.gst_amount = gst_amount
            if paid_amount:
                payment.paid_amount = paid_amount
            if pending_amount:
                payment.pending_amount = pending_amount
            if payment_date:
                payment.payment_date = payment_date
            if notes:
                payment.notes = notes
            payment.save()
            
            return Response({"status": True, "message": "Payment data updated successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class MilestoneIdWiseGetInflowPaymentOnMilestoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InFlowPaymentOnMilestoneSerializer
    queryset = InFlowPaymentOnMilestone.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            milestone_id = self.kwargs.get('milestone_id')
            if not milestone_id:
                return Response({"status": False, "message": "Milestone Id is required", "data": []})
            queryset = self.filter_queryset(self.get_queryset()).filter(milestone=milestone_id)
            serializer = InFlowPaymentOnMilestoneSerializer(queryset, many=True)
            data = serializer.data
            return Response({"status": True, "message": "Payment data fetched successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
            

          