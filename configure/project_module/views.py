from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from project_module.models import *
from project_module.serializers import *
import ipdb
from user_profile.function_call import *

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

            expense_document_attachments = request.FILES.getlist('expense_document_attachments')  # Handle multiple files
            # Validation checks
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

            expense_obj.user = user
            expense_obj.project = project
            expense_obj.category = category
            expense_obj.expense_name = expense_name
            expense_obj.expense_amount = expense_amount
            expense_obj.notes = notes
            expense_obj.save()

            if expense_document_attachments:
                expense_obj.expense_document_attachments.clear()
                for file in expense_document_attachments:
                    attachment = ExpenseProjectAttachments.objects.create(
                        user=user, expense_project_attachments=file
                    )
                    expense_obj.expense_document_attachments.add(attachment)

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
            )

            if msme_certificate:
                for file in msme_certificate:
                    if hasattr(file, 'name'):
                        # Use the correct field name 'msme_certificate_attachments'
                        attachment = MsMeCertificateAttachments.objects.create(user=user, msme_certificate_attachments=file)
                        client_obj.msme_certificate.add(attachment)

            if adhar_card:
                if hasattr(file, 'name'):
                    # Use the correct field name 'adhar_card_attachments'
                    attachment = AdharCardAttachments.objects.create(user=user, adhar_card_attachments=file)
                    client_obj.adhar_card.add(attachment)

            if pan_card:
                if hasattr(file, 'name'):
                    # Use the correct field name 'pan_card_attachments'
                    attachment = PanCardAttachments.objects.create(user=user, pan_card_attachments=file)
                    client_obj.pan_card.add(attachment)

            if third_authority_adhar_card_attachments:
                if hasattr(file, 'name'):
                    # Use the correct field name 'third_authority_adhar_card_attachments'
                    attachment = ThirdAuthorityAdharCardAttachments.objects.create(user=user, third_authority_adhar_card_attachments=file)
                    client_obj.third_authority_adhar_card_attachments.add(attachment)

            if third_authortity_pan_card_attachments:
                if hasattr(file, 'name'):
                    # Use the correct field name 'third_authority_pan_card_attachments'
                    attachment = ThirdAuthorityPanCardAttachments.objects.create(user=user, third_authority_pan_card_attachments=file)
                    client_obj.third_authortity_pan_card_attachments.add(attachment)


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

            # Fields from request data
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

            captive_rec_nonrec_rpo = request.data.get('captive_rec_nonrec_rpo')
            declaration_of_getco = request.data.get('declaration_of_getco')
            undertaking_geda = request.data.get('undertaking_geda')
            authorization_to_epc = request.data.get('authorization_to_epc')
            last_3_year_turn_over_details = request.data.get('last_3_year_turn_over_details')
            factory_end = request.data.get('factory_end')
            cin = request.data.get('cin')
            moa_partnership = request.data.get('moa_partnership')
            board_authority_signing = request.data.get('board_authority_signing')

            # Update regular fields
            client_obj.client_name = client_name
            client_obj.contact_number = contact_number
            client_obj.email = email
            client_obj.gst = gst
            client_obj.pan_number = pan_number
            client_obj.captive_rec_nonrec_rpo = captive_rec_nonrec_rpo
            client_obj.declaration_of_getco = declaration_of_getco
            client_obj.undertaking_geda = undertaking_geda
            client_obj.authorization_to_epc = authorization_to_epc
            client_obj.last_3_year_turn_over_details = last_3_year_turn_over_details
            client_obj.factory_end = factory_end
            client_obj.cin = cin
            client_obj.moa_partnership = moa_partnership
            client_obj.board_authority_signing = board_authority_signing
            client_obj.save()

            # Handle file field updates
            # Update msme_certificate files
            if msme_certificate:
                # Clear existing files
                client_obj.msme_certificate.clear()
                # Add new files
                for file in msme_certificate:
                    attachment = MsMeCertificateAttachments.objects.create(user=request.user, msme_certificate_attachments=file)
                    client_obj.msme_certificate.add(attachment)

            # Update adhar_card files
            if adhar_card:
                # Clear existing files
                client_obj.adhar_card.clear()
                # Add new files
                for file in adhar_card:
                    attachment = AdharCardAttachments.objects.create(user=request.user, adhar_card_attachments=file)
                    client_obj.adhar_card.add(attachment)

            # Update pan_card files
            if pan_card:
                # Clear existing files
                client_obj.pan_card.clear()
                # Add new files
                for file in pan_card:
                    attachment = PanCardAttachments.objects.create(user=request.user, pan_card_attachments=file)
                    client_obj.pan_card.add(attachment)

            # Update third_authority_adhar_card_attachments
            if third_authority_adhar_card_attachments:
                # Clear existing files
                client_obj.third_authority_adhar_card_attachments.clear()
                # Add new files
                for file in third_authority_adhar_card_attachments:
                    attachment = ThirdAuthorityAdharCardAttachments.objects.create(user=request.user, third_authority_adhar_card_attachments=file)
                    client_obj.third_authority_adhar_card_attachments.add(attachment)

            # Update third_authortity_pan_card_attachments
            if third_authortity_pan_card_attachments:
                # Clear existing files
                client_obj.third_authortity_pan_card_attachments.clear()
                # Add new files
                for file in third_authortity_pan_card_attachments:
                    attachment = ThirdAuthorityPanCardAttachments.objects.create(user=request.user, third_authority_pan_card_attachments=file)
                    client_obj.third_authortity_pan_card_attachments.add(attachment)

            # Serialize and return response
            serializer = self.serializer_class(client_obj, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Client Updated Successfully", "data": data})
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

            # Update loi_attachments files
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
            
            # Update loi_attachments files
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

            # Serialize and return response
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
