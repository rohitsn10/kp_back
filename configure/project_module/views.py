from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from project_module.models import *
from project_module.serializers import *
import ipdb
from user_profile.function_call import *
from datetime import datetime

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

            if msme_certificate:
                client_obj.msme_certificate.clear()
                for file in msme_certificate:
                    attachment = MsMeCertificateAttachments.objects.create(user=request.user, msme_certificate_attachments=file)
                    client_obj.msme_certificate.add(attachment)

            if adhar_card:
                client_obj.adhar_card.clear()
                for file in adhar_card:
                    attachment = AdharCardAttachments.objects.create(user=request.user, adhar_card_attachments=file)
                    client_obj.adhar_card.add(attachment)

            if pan_card:
                client_obj.pan_card.clear()
                for file in pan_card:
                    attachment = PanCardAttachments.objects.create(user=request.user, pan_card_attachments=file)
                    client_obj.pan_card.add(attachment)

            if third_authority_adhar_card_attachments:
                client_obj.third_authority_adhar_card_attachments.clear()
                for file in third_authority_adhar_card_attachments:
                    attachment = ThirdAuthorityAdharCardAttachments.objects.create(user=request.user, third_authority_adhar_card_attachments=file)
                    client_obj.third_authority_adhar_card_attachments.add(attachment)

            if third_authortity_pan_card_attachments:
                client_obj.third_authortity_pan_card_attachments.clear()
                for file in third_authortity_pan_card_attachments:
                    attachment = ThirdAuthorityPanCardAttachments.objects.create(user=request.user, third_authority_pan_card_attachments=file)
                    client_obj.third_authortity_pan_card_attachments.add(attachment)

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
            electricity_line = request.data.get('electricity_line')
            spoc_user = request.data.get('spoc_user')
            project_predication_date = parse_date(request.data.get('project_predication_date'))
            project_sub_activity_ids = request.data.get('project_sub_activity_ids', [])
            project_sub_sub_activity_ids = request.data.get('project_sub_sub_activity_ids', [])

            # Validate individual fields
            if not landbank_id:
                return Response({"status": False, "message": "Landbank ID is required."})

            if not company_id:
                return Response({"status": False, "message": "Company ID is required."})

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

            if not electricity_line:
                return Response({"status": False, "message": "Electricity line is required."})

            if not spoc_user:
                return Response({"status": False, "message": "SPOC user is required."})

            if not project_predication_date:
                return Response({"status": False, "message": "Project predication date is required."})

            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response({"status": False, "message": "Invalid company."})
            
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

            # Create the Project instance
            project = Project.objects.create(
                user=user,
                company=company,
                landbank=landbank_ins,
                project_name=project_name,
                start_date=start_date,
                end_date=end_date,
                cod_commission_date=cod_commission_date,
                # total_area_of_project=total_area_of_project,
                capacity=capacity,
                ci_or_utility=ci_or_utility,
                cpp_or_ipp=cpp_or_ipp,
                project_activity=project_activity,
                electricity_line=electricity_line,
                spoc_user_id=by_spoc_user.id,
                project_predication_date=project_predication_date,
                alloted_land_area=alloted_land_area,
                available_land_area=available_land_area
            )

            # Add ManyToMany relationships
            # if location_survey:
            #     project.location_survey.set(location_survey)

            # Set the Many-to-Many relationships for sub-activities and sub-sub-activities
            if sub_activity_names:
                project.project_sub_activity.set(sub_activity_names)

            if sub_sub_activity_names:
                project.project_sub_sub_activity.set(sub_sub_activity_names)

            return Response({"status": True,"message": "Project created successfully","data": []})

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
            electricity_line = request.data.get('electricity_line')
            spoc_user = request.data.get('spoc_user')
            project_predication_date = parse_date(request.data.get('project_predication_date'))

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
            if electricity_line:
                project_object.electricity_line = electricity_line
            if spoc_user:
                try:
                    spoc_user_object = CustomUser.objects.get(id=spoc_user)
                    project_object.spoc_user = spoc_user_object
                except CustomUser.DoesNotExist:
                    return Response({"status": False, "message": "User not found"})

            if project_predication_date:
                project_object.project_predication_date = project_predication_date

            # Update the project instance
            project_object.save()

            # Update ManyToMany relationships
            if location_survey:
                project_object.location_survey.set(location_survey)

            return Response({"status": True, "message": "Project updated successfully"})

        except Exception as e:
            return Response({"status": False, "message": f"Error updating project: {str(e)}", "data": []})



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
            start_date = parse_date(request.data.get('start_date'))
            end_date = parse_date(request.data.get('end_date'))
            milestone_description = request.data.get('milestone_description')

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

            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({"status": False, "message": "Invalid project."})

            milestone = ProjectMilestone.objects.create(
                user=user,
                project=project,
                start_date=start_date,
                end_date=end_date,
                milestone_name = milestone_name,
                milestone_description=milestone_description,
            )

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