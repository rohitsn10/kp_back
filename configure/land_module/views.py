from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from land_module.models import *
from land_module.serializers import *
import ipdb
from user_profile.function_call import *
import ast
from django.db.models import Q

class CreateLandCategoryViewSet(viewsets.ModelViewSet):
    queryset = LandCategory.objects.all()
    serializer_class = LandCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            category_name = request.data.get('category_name')

            if not category_name:
                return Response({"status": False, "message": "Category name is required", "data": []})

            category = LandCategory.objects.create(user=user, category_name=category_name)
            serializer = LandCategorySerializer(category)
            return Response({"status": True, "message": "Land category created successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            if self.request.user.groups.filter(name='Admin').exists():
                categories = LandCategory.objects.all()
                serializer = LandCategorySerializer(categories, many=True)
                return Response({"status": True, "message": "Land categories retrieved successfully", "data": serializer.data})
            else:
                categories = LandCategory.objects.filter(user=user)
                serializer = LandCategorySerializer(categories, many=True)
                return Response({"status": True, "message": "Land categories retrieved successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class UpdateLandCategoryViewSet(viewsets.ModelViewSet):
    queryset = LandCategory.objects.all()
    serializer_class = LandCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'land_category_id'

    def update(self, request, *args, **kwargs):
        try:
            land_category_id = kwargs.get('land_category_id')
            category_name = request.data.get('category_name')

            if not land_category_id:
                return Response({"status": False, "message": "Category ID is required", "data": []})

            category = LandCategory.objects.get(id=land_category_id)

            if not category:
                return Response({"status": False, "message": "Category not found", "data": []})

            category.category_name = category_name
            category.save()

            serializer = LandCategorySerializer(category)
            return Response({"status": True, "message": "Land category updated successfully", "data": serializer.data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            land_category_id = kwargs.get('land_category_id')

            if not land_category_id:
                return Response({"status": False, "message": "Category ID is required", "data": []})

            category = LandCategory.objects.get(id=land_category_id)

            if not category:
                return Response({"status": False, "message": "Category not found", "data": []})

            category.delete()

            return Response({"status": True, "message": "Land category deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class LandBankMasterCreateViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = request.data.get('land_bank_id')
            land_category_id = request.data.get('land_category_id')
            land_name = request.data.get('land_name')
            survey_number = request.data.get('survey_number')
            village_name = request.data.get('village_name')
            taluka_name = request.data.get('taluka_name')
            tahshil_name = request.data.get('tahshil_name')
            total_land_area = request.data.get('total_land_area')

            land_location_files = request.FILES.getlist('land_location_files') or []
            land_survey_number_files = request.FILES.getlist('land_survey_number_files') or []
            land_key_plan_files = request.FILES.getlist('land_key_plan_files') or []
            land_attach_approval_report_files = request.FILES.getlist('land_attach_approval_report_files') or []
            land_approach_road_files = request.FILES.getlist('land_approach_road_files') or []
            land_co_ordinates_files = request.FILES.getlist('land_co_ordinates_files') or []
            land_proposed_gss_files = request.FILES.getlist('land_proposed_gss_files') or []
            land_transmission_line_files = request.FILES.getlist('land_transmission_line_files') or []

            if not land_bank_id:
                return Response({"status": False, "message": "Land bank id is required", "data": []})
            
            if not land_category_id:
                return Response({"status": False, "message": "Land category is required", "data": []})

            if not land_name:
                return Response({"status": False, "message": "Land name is required", "data": []})

            if not survey_number:
                return Response({"status": False, "message": "Survey number is required", "data": []})

            if not village_name:
                return Response({"status": False, "message": "Village name is required", "data": []})

            if not taluka_name:
                return Response({"status": False, "message": "Taluka name is required", "data": []})

            if not tahshil_name:
                return Response({"status": False, "message": "Tahshil name is required", "data": []})
            
            if not total_land_area:
                return Response({"status": False, "message": "Total land area is required", "data": []})

            if land_category_id:
                land_category = LandCategory.objects.get(id=land_category_id)
                if not land_category:
                    return Response({"status": False, "message": "Land category not found", "data": []})
            
            if not land_key_plan_files:
                return Response({"status": False, "message": "Land key plan files are required", "data": []})
            
            if not land_approach_road_files:
                return Response({"status": False, "message": "Land approach road files are required", "data": []})
            
            if not land_co_ordinates_files:
                return Response({"status": False, "message": "Land co-ordinates files are required", "data": []})
            
            if not land_proposed_gss_files:
                return Response({"status": False, "message": "Land proposed GSS files are required", "data": []})
            
            land = LandBankMaster.objects.get(id=land_bank_id)
            if not land:
                return Response({"status": False, "message": "Land not found", "data": []})

            land.land_category = land_category
            land.land_name = land_name
            land.survey_number = survey_number
            land.village_name = village_name
            land.taluka_name = taluka_name
            land.total_land_area = total_land_area
            land.tahshil_name = tahshil_name

            # Attach the files if provided
            if land_location_files:
                for file in land_location_files:
                    land_location_attachments = LandLocationAttachment.objects.create(user=user, land_location_file=file)
                    land.land_location_file.add(land_location_attachments)
            if land_survey_number_files:
                for file in land_survey_number_files:
                    land_survey_number_attachments = LandSurveyNumbeAttachment.objects.create(user=user, land_survey_number_file=file)
                    land.land_survey_number_file.add(land_survey_number_attachments)
            if land_key_plan_files:
                for file in land_key_plan_files:
                    land_key_plan_attachments = LandKeyPlanAttachment.objects.create(user=user, land_key_plan_file=file)
                    land.land_key_plan_file.add(land_key_plan_attachments)
            if land_attach_approval_report_files:
                for file in land_attach_approval_report_files:
                    land_attach_approval_report_attachments = LandAttachApprovalReportAttachment.objects.create(user=user, land_attach_approval_report_file=file)
                    land.land_attach_approval_report_file.add(land_attach_approval_report_attachments)
            if land_approach_road_files:
                for file in land_approach_road_files:
                    land_approach_road_attachments = LandApproachRoadAttachment.objects.create(user=user, land_approach_road_file=file)
                    land.land_approach_road_file.add(land_approach_road_attachments)
            if land_co_ordinates_files:
                for file in land_co_ordinates_files:
                    land_co_ordinates_attachments = LandCoOrdinatesAttachment.objects.create(user=user, land_co_ordinates_file=file)
                    land.land_co_ordinates_file.add(land_co_ordinates_attachments)
            if land_proposed_gss_files:
                for file in land_proposed_gss_files:
                    land_proposed_gss_attachments = LandProposedGssAttachment.objects.create(user=user, land_proposed_gss_file=file)
                    land.land_proposed_gss_file.add(land_proposed_gss_attachments)
            if land_transmission_line_files:
                for file in land_transmission_line_files:
                    land_transmission_line_attachments = LandTransmissionLineAttachment.objects.create(user=user, land_transmission_line_file=file)
                    land.land_transmission_line_file.add(land_transmission_line_attachments)

            land.save()
            # Serialize the created LandBankMaster instance
            # serializer = LandBankSerializer(land, context={'request': request})
            # data = serializer.data

            return Response({"status": True, "message": "Land Bank created successfully", "data": []})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            if not queryset.exists():
                return Response({"status": False, "message": "No data found", "data": []})

            serializer = LandBankSerializer(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land Bank List Successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class ApproveRejectLandbankStatus(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = self.kwargs.get('land_bank_id')
            land_bank_status = request.data.get('land_bank_status')
            
            if not land_bank_id:
                return Response({"status": False, "message": "Land bank id is required", "data": []})

            if not land_bank_status:
                return Response({"status": False, "message": "Status is required", "data": []})
            
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            if not land_bank:
                return Response({"status":False, "message":" land_bank not found"})
            if land_bank_status == "Approved":
                land_bank.land_bank_status = land_bank_status
                approved_obj = LandBankApproveAction.objects.create(land_bank=land_bank, approved_by=user, land_bank_status=land_bank_status)
                approved_obj.save()
                land_bank.save()

            if land_bank_status == "Rejected":
                land_bank.land_bank_status = land_bank_status
                rejected_obj = LandBankRejectAction.objects.create(land_bank=land_bank, rejected_by=user, land_bank_status=land_bank_status)
                rejected_obj.save()
                land_bank.save()
                
            serializer = LandBankSerializer(land_bank, context={'request': request})
            data = serializer.data

            return Response({"status": True, "message": "Land Bank status updated successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class LandBankMasterUpdateViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            land_bank_id = self.kwargs.get('land_bank_id')
            land_category_id = request.data.get('land_category_id')
            land_name = request.data.get('land_name')
            solar_or_winds = request.data.get('solar_or_winds')
            survey_number = request.data.get('survey_number')
            taluka_name = village_name = request.data.get('taluka_name')
            tahshil_name = village_name = request.data.get('tahshil_name')
            total_land_area = village_name = request.data.get('total_land_area')

            land_location_files = request.FILES.getlist('land_location_files') or []
            land_survey_number_files = request.FILES.getlist('land_survey_number_files') or []
            land_key_plan_files = request.FILES.getlist('land_key_plan_files') or []
            land_attach_approval_report_files = request.FILES.getlist('land_attach_approval_report_files') or []
            land_approach_road_files = request.FILES.getlist('land_approach_road_files') or []
            land_co_ordinates_files = request.FILES.getlist('land_co_ordinates_files') or []
            land_proposed_gss_files = request.FILES.getlist('land_proposed_gss_files') or []
            land_transmission_line_files = request.FILES.getlist('land_transmission_line_files') or []
            

            land_location_files_to_remove = request.data.get('land_location_files_to_remove', [])
            land_survey_number_files_to_remove = request.data.get('land_survey_number_files_to_remove', [])
            land_key_plan_files_to_remove = request.data.get('land_key_plan_files_to_remove', [])
            land_attach_approval_report_files_to_remove = request.data.get('land_attach_approval_report_files_to_remove', [])
            land_approach_road_files_to_remove = request.data.get('land_approach_road_files_to_remove', [])
            land_co_ordinates_files_to_remove = request.data.get('land_co_ordinates_files_to_remove', [])
            land_proposed_gss_files_to_remove = request.data.get('land_proposed_gss_files_to_remove', [])
            land_transmission_line_files_to_remove = request.data.get('land_transmission_line_files_to_remove', [])
            approved_report_files_to_remove = request.data.get('approved_report_files_to_remove', [])

            land_location_files_to_remove = process_file_ids(land_location_files_to_remove)
            land_survey_number_files_to_remove = process_file_ids(land_survey_number_files_to_remove)
            land_key_plan_files_to_remove = process_file_ids(land_key_plan_files_to_remove)
            land_attach_approval_report_files_to_remove = process_file_ids(land_attach_approval_report_files_to_remove)
            land_approach_road_files_to_remove = process_file_ids(land_approach_road_files_to_remove)
            land_co_ordinates_files_to_remove = process_file_ids(land_co_ordinates_files_to_remove)
            land_proposed_gss_files_to_remove = process_file_ids(land_proposed_gss_files_to_remove)
            land_transmission_line_files_to_remove = process_file_ids(land_transmission_line_files_to_remove)
            approved_report_files_to_remove = process_file_ids(approved_report_files_to_remove)

            if not land_category_id:
                return Response({"status": False, "message": "Land category is required", "data": []})

            if not land_name:
                return Response({"status": False, "message": "Land name is required", "data": []})

            if not solar_or_winds:
                return Response({"status": False, "message": "Please select solar or wind", "data": []})
            
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            if not land_bank:
                return Response({"status": False, "message": "Land Bank data not found", "data": []})
            
            if land_category_id:
                land_category = LandCategory.objects.get(id=land_category_id)
                land_bank.land_category = land_category
            if land_name:
                land_bank.land_name = land_name
            if solar_or_winds:
                land_bank.solar_or_winds = solar_or_winds
            if survey_number:
                land_bank.survey_number = survey_number
            if village_name:
                land_bank.village_name = village_name
            if taluka_name:
                land_bank.taluka_name = taluka_name
            if tahshil_name:
                land_bank.tahshil_name = tahshil_name
            if total_land_area:
                land_bank.total_land_area = total_land_area

            land_bank.save()
                
            if land_location_files_to_remove:
                for file_id in land_location_files_to_remove:
                    try:
                        file_instance = LandLocationAttachment.objects.get(id=file_id)
                        land_bank.land_location_file.remove(file_instance)
                        file_instance.delete()
                    except LandLocationAttachment.DoesNotExist:
                        continue

            if land_survey_number_files_to_remove:
                for file_id in land_survey_number_files_to_remove:
                    try:
                        file_instance = LandSurveyNumbeAttachment.objects.get(id=file_id)
                        land_bank.land_survey_number_file.remove(file_instance)
                        file_instance.delete()  
                    except LandSurveyNumbeAttachment.DoesNotExist:
                        continue  

            if land_key_plan_files_to_remove:
                for file_id in land_key_plan_files_to_remove:
                    try:
                        file_instance = LandKeyPlanAttachment.objects.get(id=file_id)
                        land_bank.land_key_plan_file.remove(file_instance) 
                        file_instance.delete()  
                    except LandKeyPlanAttachment.DoesNotExist:
                        continue  

            if land_attach_approval_report_files_to_remove:
                for file_id in land_attach_approval_report_files_to_remove:
                    try:
                        file_instance = LandAttachApprovalReportAttachment.objects.get(id=file_id)
                        land_bank.land_attach_approval_report_file.remove(file_instance) 
                        file_instance.delete() 
                    except LandAttachApprovalReportAttachment.DoesNotExist:
                        continue 

            if land_approach_road_files_to_remove:
                for file_id in land_approach_road_files_to_remove:
                    try:
                        file_instance = LandApproachRoadAttachment.objects.get(id=file_id)
                        land_bank.land_approach_road_file.remove(file_instance)
                        file_instance.delete()  
                    except LandApproachRoadAttachment.DoesNotExist:
                        continue  

            if land_co_ordinates_files_to_remove:
                for file_id in land_co_ordinates_files_to_remove:
                    try:
                        file_instance = LandCoOrdinatesAttachment.objects.get(id=file_id)
                        land_bank.land_co_ordinates_file.remove(file_instance)
                        file_instance.delete()  
                    except LandCoOrdinatesAttachment.DoesNotExist:
                        continue  

            if land_proposed_gss_files_to_remove:
                for file_id in land_proposed_gss_files_to_remove:
                    try:
                        file_instance = LandProposedGssAttachment.objects.get(id=file_id)
                        land_bank.land_proposed_gss_file.remove(file_instance)
                        file_instance.delete()
                    except LandProposedGssAttachment.DoesNotExist:
                        continue

            if land_transmission_line_files_to_remove:
                for file_id in land_transmission_line_files_to_remove:
                    try:
                        file_instance = LandTransmissionLineAttachment.objects.get(id=file_id)
                        land_bank.land_transmission_line_file.remove(file_instance)
                        file_instance.delete()  
                    except LandTransmissionLineAttachment.DoesNotExist:
                        continue  
            
            if approved_report_files_to_remove:
                for file_id in approved_report_files_to_remove:
                    try:
                        file_instance = LandApprovedReportAttachment.objects.get(id=file_id)
                        land_bank.approved_report_file.remove(file_instance)
                        file_instance.delete()  
                    except LandApprovedReportAttachment.DoesNotExist:
                        continue

            if land_location_files:
                for file in land_location_files:
                    land_location_attachments = LandLocationAttachment.objects.create(user=land_bank.user, land_location_file=file)
                    land_bank.land_location_file.add(land_location_attachments)

            if land_survey_number_files:
                for file in land_survey_number_files:
                    land_survey_number_attachments = LandSurveyNumbeAttachment.objects.create(user=land_bank.user, land_survey_number_file=file)
                    land_bank.land_survey_number_file.add(land_survey_number_attachments)

            if land_key_plan_files:
                for file in land_key_plan_files:
                    land_key_plan_attachments = LandKeyPlanAttachment.objects.create(user=land_bank.user, land_key_plan_file=file)
                    land_bank.land_key_plan_file.add(land_key_plan_attachments)

            if land_attach_approval_report_files:
                for file in land_attach_approval_report_files:
                    land_attach_approval_report_attachments = LandAttachApprovalReportAttachment.objects.create(user=land_bank.user, land_attach_approval_report_file=file)
                    land_bank.land_attach_approval_report_file.add(land_attach_approval_report_attachments)

            if land_approach_road_files:
                for file in land_approach_road_files:
                    land_approach_road_attachments = LandApproachRoadAttachment.objects.create(user=land_bank.user, land_approach_road_file=file)
                    land_bank.land_approach_road_file.add(land_approach_road_attachments)

            if land_co_ordinates_files:
                for file in land_co_ordinates_files:
                    land_co_ordinates_attachments = LandCoOrdinatesAttachment.objects.create(user=land_bank.user, land_co_ordinates_file=file)
                    land_bank.land_co_ordinates_file.add(land_co_ordinates_attachments)

            if land_proposed_gss_files:
                for file in land_proposed_gss_files:
                    land_proposed_gss_attachments = LandProposedGssAttachment.objects.create(user=land_bank.user, land_proposed_gss_file=file)
                    land_bank.land_proposed_gss_file.add(land_proposed_gss_attachments)

            if land_transmission_line_files:
                for file in land_transmission_line_files:
                    land_transmission_line_attachments = LandTransmissionLineAttachment.objects.create(user=land_bank.user, land_transmission_line_file=file)
                    land_bank.land_transmission_line_file.add(land_transmission_line_attachments)

            land_bank.save()
            serializer = LandBankSerializer(land_bank, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def delete(self, request, *args, **kwargs):
        try:
            land_bank_id = self.kwargs.get('land_bank_id')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            land_bank.delete()
            return Response({"status": True, "message": "Land deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
 
class AddFSALandBankDataViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            # land_bank_id = self.kwargs.get('land_bank_id')
            # land_bank = LandBankMaster.objects.get(id=land_bank_id)

            # Extract data from the request
            sfa_name = request.data.get('sfa_name')
            land_sfa_file = request.FILES.getlist('land_sfa_file') or []
            sfa_for_transmission_line_gss_files = request.FILES.getlist('sfa_for_transmission_line_gss_files') or []
            timeline = request.data.get('timeline')
            solar_or_winds = request.data.get('solar_or_winds')
            date_of_assessment = request.data.get('date_of_assessment')
            site_visit_date = request.data.get('site_visit_date')
            
            if not sfa_name:
                return Response({"status": False, "message": "SFA name is required", "data": []})
            if not land_sfa_file:
                return Response({"status": False, "message": "Land SFA file is required", "data": []})
            if not sfa_for_transmission_line_gss_files:
                return Response({"status": False, "message": "SFA for transmission line GSS files are required", "data": []})
            if not timeline:
                return Response({"status": False, "message": "Timeline is required", "data": []})
            if not solar_or_winds:
                return Response({"status": False, "message": "Solar or Winds is required", "data": []})
            if not date_of_assessment:
                return Response({"status": False, "message": "Date of assessment is required", "data": []})
            if not site_visit_date:
                return Response({"status": False, "message": "Site visit date is required", "data": []})

            created = LandBankMaster.objects.create(user = user, sfa_name = sfa_name, timeline = timeline, solar_or_winds = solar_or_winds,date_of_assessment = date_of_assessment,site_visit_date = site_visit_date,sfa_checked_by_user = user)
            for file in land_sfa_file:
                land_sfa_attachments = SFAAttachment.objects.create(user=user, land_sfa_file=file)
                created.land_sfa_file.add(land_sfa_attachments)

            for file in sfa_for_transmission_line_gss_files:
                sfa_for_transmission_line_gss_attachments = SFAforTransmissionLineGSSAttachment.objects.create(user=user, sfa_for_transmission_line_gss_files=file)
                created.sfa_for_transmission_line_gss_files.add(sfa_for_transmission_line_gss_attachments)

            serializer = LandBankSerializer(created, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            user = self.request.user
            department = user.department
            queryset = queryset.filter(Q(user=user) | Q(user__department=department))
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land Bank List Successfully", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})



class UpdateFSALandBankDataViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'land_bank_id'
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = self.kwargs.get('land_bank_id')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            sfa_name = request.data.get('sfa_name')
            land_sfa_file = request.FILES.getlist('land_sfa_file') or []
            sfa_for_transmission_line_gss_files = request.FILES.getlist('sfa_for_transmission_line_gss_files') or []
            timeline = request.data.get('timeline')
            land_sfa_assigned_to_users = request.data.get('land_sfa_assigned_to_users') or []  # Use getlist here for list data
            remove_land_sfa_file = request.data.get('remove_land_sfa_file') or []
            remove_sfa_for_transmission_line_gss_files = request.data.get('remove_sfa_for_transmission_line_gss_files') or []
            solar_or_winds = request.data.get('solar_or_winds')

            if isinstance(land_sfa_assigned_to_users, str):
                land_sfa_assigned_to_users = [int(user_id) for user_id in land_sfa_assigned_to_users.split(',')]
            else:
                land_sfa_assigned_to_users = [int(user_id) for user_id in land_sfa_assigned_to_users]

            users = CustomUser.objects.filter(id__in=land_sfa_assigned_to_users)
            if len(users) != len(land_sfa_assigned_to_users):
                return Response({"status": False, "message": "Some of the provided user IDs are invalid", "data": []})
            
            # if not sfa_name:
            #     return Response({"status": False, "message": "SFA name is required", "data": []})
            # if not timeline:
            #     return Response({"status": False, "message": "Timeline is required", "data": []})

            
            if sfa_name:
                land_bank.sfa_name = sfa_name
            if timeline:
                land_bank.timeline = timeline
            if solar_or_winds:
                land_bank.solar_or_winds = solar_or_winds

            if land_sfa_file:
                # land_bank.land_sfa_file.clear()
                for file in land_sfa_file:
                    land_sfa_attachments = SFAAttachment.objects.create(user=user, land_sfa_file=file)
                    land_bank.land_sfa_file.add(land_sfa_attachments)

            if sfa_for_transmission_line_gss_files:
                # land_bank.sfa_for_transmission_line_gss_files.clear()
                for file in sfa_for_transmission_line_gss_files:
                    sfa_for_transmission_line_gss_attachments = SFAforTransmissionLineGSSAttachment.objects.create(user=user, sfa_for_transmission_line_gss_files=file)
                    land_bank.sfa_for_transmission_line_gss_files.add(sfa_for_transmission_line_gss_attachments)


            if remove_land_sfa_file:
                if isinstance(remove_land_sfa_file, str):
                    remove_land_sfa_file = [int(file_id) for file_id in remove_land_sfa_file.split(',')]
                else:
                    remove_land_sfa_file = [int(file_id) for file_id in remove_land_sfa_file]

                for file_id in remove_land_sfa_file:
                    try:
                        land_sfa_attachments = SFAAttachment.objects.get(id=file_id)
                        land_sfa_attachments.delete()
                    except SFAAttachment.DoesNotExist:
                        pass

            if remove_sfa_for_transmission_line_gss_files:
                if isinstance(remove_sfa_for_transmission_line_gss_files, str):
                    remove_sfa_for_transmission_line_gss_files = [int(file_id) for file_id in remove_sfa_for_transmission_line_gss_files.split(',')]
                else:
                    remove_sfa_for_transmission_line_gss_files = [int(file_id) for file_id in remove_sfa_for_transmission_line_gss_files]
                
                for file_id in remove_sfa_for_transmission_line_gss_files:
                    try:
                        sfa_for_transmission_line_gss_attachments = SFAforTransmissionLineGSSAttachment.objects.get(id=file_id)
                        sfa_for_transmission_line_gss_attachments.delete()
                    except SFAforTransmissionLineGSSAttachment.DoesNotExist:
                        pass

            land_bank.save()
            serializer = LandBankSerializer(land_bank, context={'request': request})
            return Response({"status": True, "message": "Land updated successfully", "data": serializer.data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


class ApproveRejectLandBankDataByHODViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = self.kwargs.get('land_bank_id')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            status_of_site_visit = request.data.get('status_of_site_visit')
            approved_report_files = request.FILES.getlist('approved_report_files') or []
            if not status_of_site_visit:
                return Response({"status": False, "message": "Land bank status is required", "data": []})
            if not approved_report_files:
                return Response({"status": False, "message": "Approval Report Files are required", "data": []})
            
            if status_of_site_visit == "Approved":
                land_bank.status_of_site_visit = status_of_site_visit
                land_bank.sfa_approved_by_user = user
                
                for file in approved_report_files:
                    approved_report_attachments = LandApprovedReportAttachment.objects.create(user=land_bank.user, approved_report_file=file)
                    land_bank.approved_report_file.add(approved_report_attachments)
                    land_bank.save()
                approved_obj = SaveApprovalDataOfStatusOfSiteVisit.objects.create(land_bank=land_bank, user=user, status_of_site_visit=status_of_site_visit)
                approved_obj.save()
                land_bank.save()
                serializer = LandBankSerializer(land_bank, context={'request': request})
                data = serializer.data
                return Response({"status": True, "message": "Land approved successfully", "data": data})
            
            if status_of_site_visit == "Rejected":
                land_bank.status_of_site_visit = status_of_site_visit
                land_bank.sfa_rejected_by_user = user
                approved_obj = SaveRejectDataOfStatusOfSiteVisit.objects.create(land_bank=land_bank, user=user, status_of_site_visit=status_of_site_visit)
                approved_obj.save()
                land_bank.save()
                serializer = LandBankSerializer(land_bank, context={'request': request})
                data = serializer.data
                return Response({"status": True, "message": "Land rejected successfully", "data": data})
            
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class AddDataAfterApprovalLandBankViewset(viewsets.ModelViewSet):
    queryset = LandBankAfterApprovedData.objects.all()
    serializer_class = LandBankAfterApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = request.data.get('land_bank_id')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            dilr_attachment_file = request.FILES.getlist('dilr_attachment_file') or []
            na_65b_permission_attachment_file = request.FILES.getlist('na_65b_permission_attachment_file') or []
            revenue_7_12_records_attachment = request.FILES.getlist('revenue_7_12_records_attachment') or []
            noc_from_forest_and_amp_attachment_file = request.FILES.getlist('noc_from_forest_and_amp_attachment_file') or []
            noc_from_geology_and_mining_office_attachment_file = request.FILES.getlist('noc_from_geology_and_mining_office_attachment_file') or []
            approvals_required_for_transmission_attachment_file = request.FILES.getlist('approvals_required_for_transmission_attachment_file') or []
            canal_crossing_attachment_file = request.FILES.getlist('canal_crossing_attachment_file') or []
            lease_deed_attachment_file = request.FILES.getlist('lease_deed_attachment_file') or []
            railway_crossing_attachment_file = request.FILES.getlist('railway_crossing_attachment_file') or []
            any_gas_pipeline_crossing_attachment_file = request.FILES.getlist('any_gas_pipeline_crossing_attachment_file') or []
            road_crossing_permission_attachment_file = request.FILES.getlist('road_crossing_permission_attachment_file') or []
            any_transmission_line_crossing_permission_attachment_file = request.FILES.getlist('any_transmission_line_crossing_permission_attachment_file') or []
            any_transmission_line_shifting_permission_attachment_file = request.FILES.getlist('any_transmission_line_shifting_permission_attachment_file') or []
            gram_panchayat_permission_attachment_file = request.FILES.getlist('gram_panchayat_permission_attachment_file') or []
             # New ManyToMany fields
            municipal_corporation_permission_file = request.FILES.getlist('municipal_corporation_permission_file') or []
            list_of_other_approvals_land_file = request.FILES.getlist('list_of_other_approvals_land_file') or []
            title_search_report_file = request.FILES.getlist('title_search_report_file') or []
            coordinate_verification_file = request.FILES.getlist('coordinate_verification_file') or []
            encumbrance_noc_file = request.FILES.getlist('encumbrance_noc_file') or []
            developer_permission_file = request.FILES.getlist('developer_permission_file') or []
            noc_from_ministry_of_defence_file = request.FILES.getlist('noc_from_ministry_of_defence_file') or []
            list_of_approvals_required_for_transmission_line_file = request.FILES.getlist('list_of_approvals_required_for_transmission_line_file') or []

            land_bank_after_approved_data = LandBankAfterApprovedData.objects.create(land_bank=land_bank, user=user)
            if not land_bank_id:
                return Response({"status": False, "message": "Land bank id is required", "data": []})
            if not land_bank:
                return Response({"status": False, "message": "Land bank not found", "data": []})

            if dilr_attachment_file:
                for file in dilr_attachment_file:
                    dilr_attachments = DILRAttachment.objects.create(user=user, dilr_attachment_file=file)
                    land_bank_after_approved_data.dilr_attachment_file.add(dilr_attachments)

            if na_65b_permission_attachment_file:
                for file in na_65b_permission_attachment_file:
                    na_65b_permission_attachments = NA_65B_Permission_Attachment.objects.create(user=user, na_65b_permission_attachment_file=file)
                    land_bank_after_approved_data.na_65b_permission_attachment_file.add(na_65b_permission_attachments)

            if revenue_7_12_records_attachment:
                for file in revenue_7_12_records_attachment:
                    revenue_7_12_records_attachments = Revenue_7_12_Records_Attachment.objects.create(user=user, revenue_7_12_records_attachment=file)
                    land_bank_after_approved_data.revenue_7_12_records_attachment.add(revenue_7_12_records_attachments)

            if noc_from_forest_and_amp_attachment_file:
                for file in noc_from_forest_and_amp_attachment_file:
                    noc_from_forest_and_amp_attachments = NOCfromForestAndAmpAttachment.objects.create(user=user, noc_from_forest_and_amp_attachment_file=file)
                    land_bank_after_approved_data.noc_from_forest_and_amp_attachment_file.add(noc_from_forest_and_amp_attachments)

            if noc_from_geology_and_mining_office_attachment_file:
                for file in noc_from_geology_and_mining_office_attachment_file:
                    noc_from_geology_and_mining_office_attachments = NOCfromGeologyAndMiningOfficeAttachment.objects.create(user=user, noc_from_geology_and_mining_office_attachment_file=file)
                    land_bank_after_approved_data.noc_from_geology_and_mining_office_attachment_file.add(noc_from_geology_and_mining_office_attachments)

            if approvals_required_for_transmission_attachment_file:
                for file in approvals_required_for_transmission_attachment_file:
                    approvals_required_for_transmission_attachments = ApprovalsRequiredForTransmissionAttachment.objects.create(user=user, approvals_required_for_transmission_attachment_file=file)
                    land_bank_after_approved_data.approvals_required_for_transmission_attachment_file.add(approvals_required_for_transmission_attachments)

            if canal_crossing_attachment_file:
                for file in canal_crossing_attachment_file:
                    canal_crossing_attachments = CanalCrossingAttachment.objects.create(user=user, canal_crossing_attachment_file=file)
                    land_bank_after_approved_data.canal_crossing_attachment_file.add(canal_crossing_attachments)

            if lease_deed_attachment_file:
                for file in lease_deed_attachment_file:
                    lease_deed_attachments = LeaseDeedAttachment.objects.create(user=user, lease_deed_attachment_file=file)
                    land_bank_after_approved_data.lease_deed_attachment_file.add(lease_deed_attachments)

            if railway_crossing_attachment_file:
                for file in railway_crossing_attachment_file:
                    railway_crossing_attachments = RailwayCrossingAttachment.objects.create(user=user, railway_crossing_attachment_file=file)
                    land_bank_after_approved_data.railway_crossing_attachment_file.add(railway_crossing_attachments)

            if any_gas_pipeline_crossing_attachment_file:
                for file in any_gas_pipeline_crossing_attachment_file:
                    any_gas_pipeline_crossing_attachments = AnyGasPipelineCrossingAttachment.objects.create(user=user, any_gas_pipeline_crossing_attachment_file=file)
                    land_bank_after_approved_data.any_gas_pipeline_crossing_attachment_file.add(any_gas_pipeline_crossing_attachments)

            if road_crossing_permission_attachment_file:
                for file in road_crossing_permission_attachment_file:
                    road_crossing_permission_attachments = RoadCrossingPermissionAttachment.objects.create(user=user, road_crossing_permission_attachment_file=file)
                    land_bank_after_approved_data.road_crossing_permission_attachment_file.add(road_crossing_permission_attachments)

            if any_transmission_line_crossing_permission_attachment_file:
                for file in any_transmission_line_crossing_permission_attachment_file:
                    any_transmission_line_crossing_permission_attachment_files = AnyTransmissionLineCrossingPermissionAttachment.objects.create(user=user, any_transmission_line_crossing_permission_attachment_file=file)
                    land_bank_after_approved_data.any_transmission_line_crossing_permission_attachment_file.add(any_transmission_line_crossing_permission_attachment_files)
            
            if any_transmission_line_shifting_permission_attachment_file:
                for file in any_transmission_line_shifting_permission_attachment_file:
                    any_transmission_line_shifting_permission_attachment_files = AnyTransmissionLineShiftingPermissionAttachment.objects.create(user = user,any_transmission_line_shifting_permission_attachment_file = file)
                    land_bank_after_approved_data.any_transmission_line_shifting_permission_attachment_file.add(any_transmission_line_shifting_permission_attachment_files)

            if gram_panchayat_permission_attachment_file:
                for file in gram_panchayat_permission_attachment_file:
                    gram_panchayat_permission_attachments = GramPanchayatPermissionAttachment.objects.create(user=user, gram_panchayat_permission_attachment_file=file)
                    land_bank_after_approved_data.gram_panchayat_permission_attachment_file.add(gram_panchayat_permission_attachments)

             # Save attachments for new fields
            if municipal_corporation_permission_file:
                for file in municipal_corporation_permission_file:
                    municipal_corporation_permission_files = MunicipalCorporationPermissionAttachment.objects.create(user=user, municipal_corporation_permission_file=file)
                    land_bank_after_approved_data.municipal_corporation_permission_file.add(municipal_corporation_permission_files)

            if list_of_other_approvals_land_file:
                for file in list_of_other_approvals_land_file:
                    list_of_other_approvals_land_files = ListOfOtherApprovalsLandAttachment.objects.create(user=user, list_of_other_approvals_land_file=file)
                    land_bank_after_approved_data.list_of_other_approvals_land_file.add(list_of_other_approvals_land_files)

            if title_search_report_file:
                for file in title_search_report_file:
                    title_search_report_files = TSRAttachment.objects.create(user=user, title_search_report_file=file)
                    land_bank_after_approved_data.title_search_report_file.add(title_search_report_files)

            if coordinate_verification_file:
                for file in coordinate_verification_file:
                    coordinate_verification_files = CoordinateVerificationAttachment.objects.create(user=user, coordinate_verification_file=file)
                    land_bank_after_approved_data.coordinate_verification_file.add(coordinate_verification_files)

            if encumbrance_noc_file:
                for file in encumbrance_noc_file:
                    encumbrance_noc_files = EncumbranceNOCAttachment.objects.create(user=user, encumbrance_noc_file=file)
                    land_bank_after_approved_data.encumbrance_noc_file.add(encumbrance_noc_files)

            if developer_permission_file:
                for file in developer_permission_file:
                    developer_permission_files = DeveloperPermissionAttachment.objects.create(user=user, developer_permission_file=file)
                    land_bank_after_approved_data.developer_permission_file.add(developer_permission_files)

            if noc_from_ministry_of_defence_file:
                for file in noc_from_ministry_of_defence_file:
                    noc_from_ministry_of_defence_files = NOCfromMinistryofDefenceAttachment.objects.create(user=user, noc_from_ministry_of_defence_file=file)
                    land_bank_after_approved_data.noc_from_ministry_of_defence_file.add(noc_from_ministry_of_defence_files)

            if list_of_approvals_required_for_transmission_line_file:
                for file in list_of_approvals_required_for_transmission_line_file:
                    list_of_approvals_required_for_transmission_line_files = ListOfApprovalsRequiredForTransmissionLineAttachment.objects.create(user=user, list_of_approvals_required_for_transmission_line_file=file)
                    land_bank_after_approved_data.list_of_approvals_required_for_transmission_line_file.add(list_of_approvals_required_for_transmission_line_files)        

            land_bank_after_approved_data.save()
            serializer = LandBankAfterApprovalSerializer(land_bank_after_approved_data, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank after approval updated successfully!", "data": data})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})


    def list(self,request,*args,**kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank after approval list successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

class GetLandBankIdWise22FormsDataViewset(viewsets.ModelViewSet):
    queryset = LandBankAfterApprovedData.objects.all().order_by('-id')
    serializer_class = LandBankAfterApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'land_bank_id'
    def list(self,request,*args,**kwargs):
        try:
            land_bank_id = self.kwargs.get('land_bank_id')
            if not land_bank_id:
                return Response({"status": False, "message": "Land bank id is required", "data": []})
            
            if not LandBankMaster.objects.filter(id=land_bank_id).exists():
                return Response({"status": False, "message": "Entered land bank id is Unavailable", "data": []})
            
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            queryset = queryset.filter(land_bank=land_bank_id)
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank after approval list successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class UpdateDateAfterApprovalLandBankViewset(viewsets.ModelViewSet):
    queryset = LandBankAfterApprovedData.objects.all().order_by('-id')
    serializer_class = LandBankAfterApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'land_bank_after_approved_data_id'
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_after_approved_data_id = self.kwargs.get('land_bank_after_approved_data_id')
            land_bank_after_approved_data = LandBankAfterApprovedData.objects.get(id=land_bank_after_approved_data_id)

            dilr_attachment_file = request.FILES.getlist('dilr_attachment_file') or []
            na_65b_permission_attachment_file = request.FILES.getlist('na_65b_permission_attachment_file') or []
            revenue_7_12_records_attachment = request.FILES.getlist('revenue_7_12_records_attachment') or []
            noc_from_forest_and_amp_attachment_file = request.FILES.getlist('noc_from_forest_and_amp_attachment_file') or []
            noc_from_geology_and_mining_office_attachment_file = request.FILES.getlist('noc_from_geology_and_mining_office_attachment_file') or []
            approvals_required_for_transmission_attachment_file = request.FILES.getlist('approvals_required_for_transmission_attachment_file') or []
            canal_crossing_attachment_file = request.FILES.getlist('canal_crossing_attachment_file') or []
            lease_deed_attachment_file = request.FILES.getlist('lease_deed_attachment_file') or []
            railway_crossing_attachment_file = request.FILES.getlist('railway_crossing_attachment_file') or []
            any_gas_pipeline_crossing_attachment_file = request.FILES.getlist('any_gas_pipeline_crossing_attachment_file') or []
            road_crossing_permission_attachment_file = request.FILES.getlist('road_crossing_permission_attachment_file') or []
            any_transmission_line_crossing_permission_attachment_file = request.FILES.getlist('any_transmission_line_crossing_permission_attachment_file') or []
            any_transmission_line_shifting_permission_attachment_file = request.FILES.getlist('any_transmission_line_shifting_permission_attachment_file') or []
            gram_panchayat_permission_attachment_file = request.FILES.getlist('gram_panchayat_permission_attachment_file') or []
            municipal_corporation_permission_file = request.FILES.getlist('municipal_corporation_permission_file') or []
            list_of_other_approvals_land_file = request.FILES.getlist('list_of_other_approvals_land_file') or []
            title_search_report_file = request.FILES.getlist('title_search_report_file') or []
            coordinate_verification_file = request.FILES.getlist('coordinate_verification_file') or []
            encumbrance_noc_file = request.FILES.getlist('encumbrance_noc_file') or []
            developer_permission_file = request.FILES.getlist('developer_permission_file') or []
            noc_from_ministry_of_defence_file = request.FILES.getlist('noc_from_ministry_of_defence_file') or []
            list_of_approvals_required_for_transmission_line_file = request.FILES.getlist('list_of_approvals_required_for_transmission_line_file') or []

            remove_dilr_attachment_file = request.data.get('remove_dilr_attachment_file', [])
            remove_na_65b_permission_attachment_file = request.data.get('remove_na_65b_permission_attachment_file', [])
            remove_revenue_7_12_records_attachment = request.data.get('remove_revenue_7_12_records_attachment')
            remove_noc_from_forest_and_amp_attachment_file = request.data.get('remove_noc_from_forest_and_amp_attachment_file', [])
            remove_noc_from_geology_and_mining_office_attachment_file = request.data.get('remove_noc_from_geology_and_mining_office_attachment_file', [])
            remove_approvals_required_for_transmission_attachment_file = request.data.get('remove_approvals_required_for_transmission_attachment_file', [])
            remove_canal_crossing_attachment_file = request.data.get('remove_canal_crossing_attachment_file', [])
            remove_lease_deed_attachment_file = request.data.get('remove_lease_deed_attachment_file', [])
            remove_railway_crossing_attachment_file = request.data.get('remove_railway_crossing_attachment_file', [])
            remove_any_gas_pipeline_crossing_attachment_file = request.data.get('remove_any_gas_pipeline_crossing_attachment_file', [])
            remove_road_crossing_permission_attachment_file = request.data.get('remove_road_crossing_permission_attachment_file', [])
            remove_any_transmission_line_crossing_permission_attachment_file = request.data.get('remove_any_transmission_line_crossing_permission_attachment_file', [])
            remove_any_transmission_line_shifting_permission_attachment_file = request.data.get('remove_any_transmission_line_shifting_permission_attachment_file', [])
            remove_gram_panchayat_permission_attachment_file = request.data.get('remove_gram_panchayat_permission_attachment_file', [])
            remove_municipal_corporation_permission_file = request.data.get('remove_municipal_corporation_permission_file', [])
            remove_list_of_other_approvals_land_file = request.data.get('remove_list_of_other_approvals_land_file', [])
            remove_title_search_report_file = request.data.get('remove_title_search_report_file', [])
            remove_coordinate_verification_file = request.data.get('remove_coordinate_verification_file', [])
            remove_encumbrance_noc_file = request.data.get('remove_encumbrance_noc_file', [])
            remove_developer_permission_file = request.data.get('remove_developer_permission_file', [])
            remove_noc_from_ministry_of_defence_file = request.data.get('remove_noc_from_ministry_of_defence_file', [])
            remove_list_of_approvals_required_for_transmission_line_file = request.data.get('remove_list_of_approvals_required_for_transmission_line_file', [])
            
            remove_dilr_attachment_file = process_file_ids(remove_dilr_attachment_file)
            remove_na_65b_permission_attachment_file = process_file_ids(remove_na_65b_permission_attachment_file)
            remove_revenue_7_12_records_attachment = process_file_ids(remove_revenue_7_12_records_attachment)
            remove_noc_from_forest_and_amp_attachment_file = process_file_ids(remove_noc_from_forest_and_amp_attachment_file)
            remove_noc_from_geology_and_mining_office_attachment_file = process_file_ids(remove_noc_from_geology_and_mining_office_attachment_file)
            remove_approvals_required_for_transmission_attachment_file = process_file_ids(remove_approvals_required_for_transmission_attachment_file)
            remove_canal_crossing_attachment_file = process_file_ids(remove_canal_crossing_attachment_file)
            remove_lease_deed_attachment_file = process_file_ids(remove_lease_deed_attachment_file)
            remove_railway_crossing_attachment_file = process_file_ids(remove_railway_crossing_attachment_file)
            remove_any_gas_pipeline_crossing_attachment_file = process_file_ids(remove_any_gas_pipeline_crossing_attachment_file)
            remove_road_crossing_permission_attachment_file = process_file_ids(remove_road_crossing_permission_attachment_file)
            remove_any_transmission_line_crossing_permission_attachment_file = process_file_ids(remove_any_transmission_line_crossing_permission_attachment_file)
            remove_any_transmission_line_shifting_permission_attachment_file = process_file_ids(remove_any_transmission_line_shifting_permission_attachment_file)
            remove_gram_panchayat_permission_attachment_file = process_file_ids(remove_gram_panchayat_permission_attachment_file)
            remove_municipal_corporation_permission_file = process_file_ids(remove_municipal_corporation_permission_file)
            remove_list_of_other_approvals_land_file = process_file_ids(remove_list_of_other_approvals_land_file)
            remove_title_search_report_file = process_file_ids(remove_title_search_report_file)
            remove_coordinate_verification_file = process_file_ids(remove_coordinate_verification_file)
            remove_encumbrance_noc_file = process_file_ids(remove_encumbrance_noc_file)
            remove_developer_permission_file = process_file_ids(remove_developer_permission_file)
            remove_noc_from_ministry_of_defence_file = process_file_ids(remove_noc_from_ministry_of_defence_file)
            remove_list_of_approvals_required_for_transmission_line_file = process_file_ids(remove_list_of_approvals_required_for_transmission_line_file)
            
            
        
            if dilr_attachment_file:
                for file in dilr_attachment_file:
                    dilr_attachment_files = DILRAttachment.objects.create(user=user, dilr_attachment_file=file)
                    land_bank_after_approved_data.dilr_attachment_file.add(dilr_attachment_files)

            if na_65b_permission_attachment_file:
                for file in na_65b_permission_attachment_file:
                    na_65b_permission_attachment_files = NA_65B_Permission_Attachment.objects.create(user=user, na_65b_permission_attachment_file=file)
                    land_bank_after_approved_data.na_65b_permission_attachment_file.add(na_65b_permission_attachment_files)

            if revenue_7_12_records_attachment:
                for file in revenue_7_12_records_attachment:
                    revenue_7_12_records_attachment_files = Revenue_7_12_Records_Attachment.objects.create(user=user, revenue_7_12_records_attachment=file)
                    land_bank_after_approved_data.revenue_7_12_records_attachment.add(revenue_7_12_records_attachment_files)

            if noc_from_forest_and_amp_attachment_file:
                for file in noc_from_forest_and_amp_attachment_file:
                    noc_from_forest_and_amp_attachment_files = NOCfromForestAndAmpAttachment.objects.create(user=user, noc_from_forest_and_amp_attachment_file=file)
                    land_bank_after_approved_data.noc_from_forest_and_amp_attachment_file.add(noc_from_forest_and_amp_attachment_files)

            if noc_from_geology_and_mining_office_attachment_file:
                for file in noc_from_geology_and_mining_office_attachment_file:
                    noc_from_geology_and_mining_office_attachment_files = NOCfromGeologyAndMiningOfficeAttachment.objects.create(user=user, noc_from_geology_and_mining_office_attachment_file=file)
                    land_bank_after_approved_data.noc_from_geology_and_mining_office_attachment_file.add(noc_from_geology_and_mining_office_attachment_files)

            if approvals_required_for_transmission_attachment_file:
                for file in approvals_required_for_transmission_attachment_file:
                    approvals_required_for_transmission_attachment_files = ApprovalsRequiredForTransmissionAttachment.objects.create(user=user, approvals_required_for_transmission_attachment_file=file)
                    land_bank_after_approved_data.approvals_required_for_transmission_attachment_file.add(approvals_required_for_transmission_attachment_files)

            if canal_crossing_attachment_file:
                for file in canal_crossing_attachment_file:
                    canal_crossing_attachment_files = CanalCrossingAttachment.objects.create(user=user, canal_crossing_attachment_file=file)
                    land_bank_after_approved_data.canal_crossing_attachment_file.add(canal_crossing_attachment_files)

            if lease_deed_attachment_file:
                for file in lease_deed_attachment_file:
                    lease_deed_attachment_files = LeaseDeedAttachment.objects.create(user=user, lease_deed_attachment_file=file)
                    land_bank_after_approved_data.lease_deed_attachment_file.add(lease_deed_attachment_files)

            if railway_crossing_attachment_file:                
                for file in railway_crossing_attachment_file:
                    railway_crossing_attachment_files = RailwayCrossingAttachment.objects.create(user=user, railway_crossing_attachment_file=file)
                    land_bank_after_approved_data.railway_crossing_attachment_file.add(railway_crossing_attachment_files)

            if any_gas_pipeline_crossing_attachment_file:
                for file in any_gas_pipeline_crossing_attachment_file:
                    any_gas_pipeline_crossing_attachment_files = AnyGasPipelineCrossingAttachment.objects.create(user=user, any_gas_pipeline_crossing_attachment_file=file)
                    land_bank_after_approved_data.any_gas_pipeline_crossing_attachment_file.add(any_gas_pipeline_crossing_attachment_files)

            if road_crossing_permission_attachment_file:
                for file in road_crossing_permission_attachment_file:
                    road_crossing_permission_attachment_files = RoadCrossingPermissionAttachment.objects.create(user=user, road_crossing_permission_attachment_file=file)
                    land_bank_after_approved_data.road_crossing_permission_attachment_file.add(road_crossing_permission_attachment_files)

            if any_transmission_line_crossing_permission_attachment_file:
                for file in any_transmission_line_crossing_permission_attachment_file:
                    any_transmission_line_crossing_permission_attachment_files = AnyTransmissionLineCrossingPermissionAttachment.objects.create(user=user, any_transmission_line_crossing_permission_attachment_file=file)
                    land_bank_after_approved_data.any_transmission_line_crossing_permission_attachment_file.add(any_transmission_line_crossing_permission_attachment_files)

            if any_transmission_line_shifting_permission_attachment_file:
                for file in any_transmission_line_shifting_permission_attachment_file:
                    any_transmission_line_shifting_permission_attachment_files = AnyTransmissionLineShiftingPermissionAttachment.objects.create(user=user, any_transmission_line_shifting_permission_attachment_file=file)
                    land_bank_after_approved_data.any_transmission_line_shifting_permission_attachment_file.add(any_transmission_line_shifting_permission_attachment_files)

            if gram_panchayat_permission_attachment_file:
                for file in gram_panchayat_permission_attachment_file:
                    gram_panchayat_permission_attachment_files = GramPanchayatPermissionAttachment.objects.create(user=user, gram_panchayat_permission_attachment_file=file)
                    land_bank_after_approved_data.gram_panchayat_permission_attachment_file.add(gram_panchayat_permission_attachment_files)
            
            if municipal_corporation_permission_file:
                for file in municipal_corporation_permission_file:
                    municipal_corporation_permission_files = MunicipalCorporationPermissionAttachment.objects.create(user=user, municipal_corporation_permission_file=file)
                    land_bank_after_approved_data.municipal_corporation_permission_file.add(municipal_corporation_permission_files)
            
            if list_of_other_approvals_land_file:
                for file in list_of_other_approvals_land_file:
                    list_of_other_approvals_land_files = ListOfOtherApprovalsLandAttachment.objects.create(user=user, list_of_other_approvals_land_file=file)
                    land_bank_after_approved_data.list_of_other_approvals_land_file.add(list_of_other_approvals_land_files)
            
            if title_search_report_file:
                for file in title_search_report_file:
                    title_search_report_files = TSRAttachment.objects.create(user=user, title_search_report_file=file)
                    land_bank_after_approved_data.title_search_report_file.add(title_search_report_files)

            if coordinate_verification_file:
                for file in coordinate_verification_file:
                    coordinate_verification_files = CoordinateVerificationAttachment.objects.create(user=user, coordinate_verification_file=file)
                    land_bank_after_approved_data.coordinate_verification_file.add(coordinate_verification_files)

            if encumbrance_noc_file:
                for file in encumbrance_noc_file:
                    encumbrance_noc_files = EncumbranceNOCAttachment.objects.create(user=user, encumbrance_noc_file=file)
                    land_bank_after_approved_data.encumbrance_noc_file.add(encumbrance_noc_files)

            if developer_permission_file:
                for file in developer_permission_file:
                    developer_permission_files = DeveloperPermissionAttachment.objects.create(user=user, developer_permission_file=file)
                    land_bank_after_approved_data.developer_permission_file.add(developer_permission_files)

            if noc_from_ministry_of_defence_file:
                for file in noc_from_ministry_of_defence_file:
                    noc_from_ministry_of_defence_files = NOCfromMinistryofDefenceAttachment.objects.create(user=user, noc_from_ministry_of_defence_file=file)
                    land_bank_after_approved_data.noc_from_ministry_of_defence_file.add(noc_from_ministry_of_defence_files)

            if list_of_approvals_required_for_transmission_line_file:
                for file in list_of_approvals_required_for_transmission_line_file:
                    list_of_approvals_required_for_transmission_line_files = ListOfApprovalsRequiredForTransmissionLineAttachment.objects.create(user=user, list_of_approvals_required_for_transmission_line_file=file)
                    land_bank_after_approved_data.list_of_approvals_required_for_transmission_line_file.add(list_of_approvals_required_for_transmission_line_files)

            if remove_dilr_attachment_file:
                for file_id in remove_dilr_attachment_file:
                    try:    
                        file_instance = DILRAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.dilr_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except DILRAttachment.DoesNotExist:
                        continue

            if remove_na_65b_permission_attachment_file:
                for file_id in remove_na_65b_permission_attachment_file:
                    try:    
                        file_instance = NA_65B_Permission_Attachment.objects.get(id=file_id)
                        land_bank_after_approved_data.na_65b_permission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except NA_65B_Permission_Attachment.DoesNotExist:
                        continue

            if remove_revenue_7_12_records_attachment:
                for file_id in remove_revenue_7_12_records_attachment:
                    try:    
                        file_instance = Revenue_7_12_Records_Attachment.objects.get(id=file_id)
                        land_bank_after_approved_data.revenue_7_12_records_attachment.remove(file_instance)
                        file_instance.delete()
                    except Revenue_7_12_Records_Attachment.DoesNotExist:
                        continue

            if remove_noc_from_forest_and_amp_attachment_file:
                for file_id in remove_noc_from_forest_and_amp_attachment_file:
                    try:    
                        file_instance = NOCfromForestAndAmpAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.noc_from_forest_and_amp_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except NOCfromForestAndAmpAttachment.DoesNotExist:
                        continue

            if remove_noc_from_geology_and_mining_office_attachment_file:
                for file_id in remove_noc_from_geology_and_mining_office_attachment_file:
                    try:    
                        file_instance = NOCfromGeologyAndMiningOfficeAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.noc_from_geology_and_mining_office_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except NOCfromGeologyAndMiningOfficeAttachment.DoesNotExist:
                        continue

            if remove_approvals_required_for_transmission_attachment_file:
                for file_id in remove_approvals_required_for_transmission_attachment_file:
                    try:
                        file_instance = ApprovalsRequiredForTransmissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.approvals_required_for_transmission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except ApprovalsRequiredForTransmissionAttachment.DoesNotExist:
                        continue

            if remove_canal_crossing_attachment_file:
                for file_id in remove_canal_crossing_attachment_file:
                    try:
                        file_instance = CanalCrossingAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.canal_crossing_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except CanalCrossingAttachment.DoesNotExist:
                        continue

            if remove_lease_deed_attachment_file:
                for file_id in remove_lease_deed_attachment_file:
                    try:
                        file_instance = LeaseDeedAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.lease_deed_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except LeaseDeedAttachment.DoesNotExist:
                        continue

            if remove_railway_crossing_attachment_file:
                for file_id in remove_railway_crossing_attachment_file:
                    try:
                        file_instance = RailwayCrossingAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.railway_crossing_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except RailwayCrossingAttachment.DoesNotExist:
                        continue

            if remove_any_gas_pipeline_crossing_attachment_file:
                for file_id in remove_any_gas_pipeline_crossing_attachment_file:
                    try:
                        file_instance = AnyGasPipelineCrossingAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.any_gas_pipeline_crossing_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except AnyGasPipelineCrossingAttachment.DoesNotExist:
                        continue

            if remove_road_crossing_permission_attachment_file:
                for file_id in remove_road_crossing_permission_attachment_file:
                    try:
                        file_instance = RoadCrossingPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.road_crossing_permission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except RoadCrossingPermissionAttachment.DoesNotExist:
                        continue

            if remove_any_transmission_line_crossing_permission_attachment_file:
                for file_id in remove_any_transmission_line_crossing_permission_attachment_file:
                    try:
                        file_instance = AnyTransmissionLineCrossingPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.any_transmission_line_crossing_permission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except AnyTransmissionLineCrossingPermissionAttachment.DoesNotExist:
                        continue

            if remove_any_transmission_line_shifting_permission_attachment_file:
                for file_id in remove_any_transmission_line_shifting_permission_attachment_file:
                    try:
                        file_instance = AnyTransmissionLineShiftingPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.any_transmission_line_shifting_permission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except AnyTransmissionLineShiftingPermissionAttachment.DoesNotExist:
                        continue

            if remove_gram_panchayat_permission_attachment_file:
                for file_id in remove_gram_panchayat_permission_attachment_file:
                    try:
                        file_instance = GramPanchayatPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.gram_panchayat_permission_attachment_file.remove(file_instance)
                        file_instance.delete()
                    except GramPanchayatPermissionAttachment.DoesNotExist:
                        continue

            if remove_municipal_corporation_permission_file:
                for file_id in remove_municipal_corporation_permission_file:
                    try:
                        file_instance = MunicipalCorporationPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.municipal_corporation_permission_file.remove(file_instance)
                        file_instance.delete()
                    except MunicipalCorporationPermissionAttachment.DoesNotExist:
                        continue
            
            if remove_list_of_other_approvals_land_file:
                for file_id in remove_list_of_other_approvals_land_file:
                    try:
                        file_instance = ListOfOtherApprovalsLandAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.list_of_other_approvals_land_file.remove(file_instance)
                        file_instance.delete()
                    except ListOfOtherApprovalsLandAttachment.DoesNotExist:
                        continue

            if remove_title_search_report_file:
                for file_id in remove_title_search_report_file:
                    try:
                        file_instance = TSRAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.title_search_report_file.remove(file_instance)
                        file_instance.delete()
                    except TSRAttachment.DoesNotExist:
                        continue

            if remove_coordinate_verification_file:
                for file_id in remove_coordinate_verification_file:
                    try:
                        file_instance = CoordinateVerificationAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.coordinate_verification_file.remove(file_instance)
                        file_instance.delete()
                    except CoordinateVerificationAttachment.DoesNotExist:
                        continue

            if remove_encumbrance_noc_file:
                for file_id in remove_encumbrance_noc_file:
                    try:
                        file_instance = EncumbranceNOCAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.encumbrance_noc_file.remove(file_instance)
                        file_instance.delete()
                    except EncumbranceNOCAttachment.DoesNotExist:
                        continue

            if remove_developer_permission_file:
                for file_id in remove_developer_permission_file:
                    try:
                        file_instance = DeveloperPermissionAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.developer_permission_file.remove(file_instance)
                        file_instance.delete()
                    except DeveloperPermissionAttachment.DoesNotExist:
                        continue

            if remove_noc_from_ministry_of_defence_file:
                for file_id in remove_noc_from_ministry_of_defence_file:
                    try:
                        file_instance = NOCfromMinistryofDefenceAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.noc_from_ministry_of_defence_file.remove(file_instance)
                        file_instance.delete()
                    except NOCfromMinistryofDefenceAttachment.DoesNotExist:
                        continue

            if remove_list_of_approvals_required_for_transmission_line_file:
                for file_id in remove_list_of_approvals_required_for_transmission_line_file:
                    try:
                        file_instance = ListOfApprovalsRequiredForTransmissionLineAttachment.objects.get(id=file_id)
                        land_bank_after_approved_data.list_of_approvals_required_for_transmission_line_file.remove(file_instance)
                        file_instance.delete()
                    except ListOfApprovalsRequiredForTransmissionLineAttachment.DoesNotExist:
                        continue

            land_bank_after_approved_data.save()
            serializer = LandBankAfterApprovalSerializer(land_bank_after_approved_data, context={'request': request})
            data = serializer.data

            return Response({"status": True, "message": "Land bank approved successfully", "data":data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class CrateLandBankLocationViewset(viewsets.ModelViewSet):
    queryset = LandBankLocation.objects.all().order_by('-id')
    serializer_class = LandBankLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = request.data.get('land_bank_id')
            land_bank_location_name = request.data.get('land_bank_location_name')
            near_by_area = request.data.get('near_by_area')
            total_land_area = request.data.get('total_land_area')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)

            if not land_bank:
                return Response({"status": False, "message": "Land bank not found", "data": []})
            if not total_land_area:
                return Response({"status": False, "message": "Total Land Area is required"})
            
            land_bank_location = LandBankLocation.objects.create(user=user, land_bank=land_bank, land_bank_location_name = land_bank_location_name,total_land_area=total_land_area,near_by_area = near_by_area)
            serializer = LandBankLocationSerializer(land_bank_location, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank location created successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank location list successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
        
class LandBankIdWiseLocationViewset(viewsets.ModelViewSet):
    queryset = LandBankLocation.objects.all().order_by('-id')
    serializer_class = LandBankLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'land_bank_id'

    def list(self, request, *args, **kwargs):
        try:
            land_bank_id = self.kwargs.get('land_bank_id')
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(land_bank=land_bank_id)
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank location list successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

class UpdateLandBankLocationViewset(viewsets.ModelViewSet):
    queryset = LandBankLocation.objects.all().order_by('-id')
    serializer_class = LandBankLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_location_id = self.kwargs.get('land_bank_location_id')
            land_bank_location = LandBankLocation.objects.get(id=land_bank_location_id)
            land_bank_location_name = request.data.get('land_bank_location_name')
            land_survey_number = request.data.get('land_survey_number')
            total_land_area = request.data.get('total_land_area')
            land_bank = land_bank_location.land_bank
            if total_land_area:
                land_bank_location.total_land_area = total_land_area
            if land_bank_location_name:
                land_bank_location.land_bank_location_name = land_bank_location_name
            if land_survey_number:
                land_survey_obj = LandSurveyNumber.objects.create(user = user,land_survey_number = land_survey_number,location_name = land_bank_location,land_bank = land_bank)
                land_survey_obj.save()
            land_bank_location.save()
            
            serializer = LandBankLocationSerializer(land_bank_location, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land bank location updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
        try:
            land_bank_location_id = self.kwargs.get('land_bank_location_id')
            land_bank_location = LandBankLocation.objects.get(id=land_bank_location_id)
            land_bank_location.delete()
            return Response({"status": True, "message": "Land bank location deleted successfully", "data": []})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
class LandLocationIdWiseLandSurveyNumberViewset(viewsets.ModelViewSet):
    queryset = LandSurveyNumber.objects.all().order_by('-id')
    serializer_class = LandSurveyNumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'location_name_id'

    def list(self, request, *args, **kwargs):
        try:
            location_name_id = self.kwargs.get('location_name_id')
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(location_name=location_name_id)
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land survey number list successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})