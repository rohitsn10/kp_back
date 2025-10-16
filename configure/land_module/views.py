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
from django.shortcuts import get_object_or_404

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
            # user = self.request.user
            # if self.request.user.groups.filter(name='Admin').exists():
            categories = LandCategory.objects.all()
            serializer = LandCategorySerializer(categories, many=True)
            return Response({"status": True, "message": "Land categories retrieved successfully", "data": serializer.data})
            # else:
            #     categories = LandCategory.objects.filter(user=user)
            #     serializer = LandCategorySerializer(categories, many=True)
            #     return Response({"status": True, "message": "Land categories retrieved successfully", "data": serializer.data})
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

import json
class LandBankMasterCreateViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = request.data.get('land_bank_id')
            land_name = request.data.get('land_name')
            block_number = request.data.get('block_number')
            land_type=request.data.get('land_type')
            sale_deed_date = request.data.get('sale_deed_date') or None
            sale_deed_number=request.data.get('sale_deed_number') or None
            lease_deed_date = request.data.get('lease_deed_date') or None
            lease_deed_number = request.data.get('lease_deed_number') or None

            survey_number = request.data.get('survey_number')
            village_name = request.data.get('village_name')
            district_name = request.data.get('district_name')
            taluka_tahshil_name = request.data.get('taluka_tahshil_name')
            propose_gss_number = request.data.get('propose_gss_number')
            land_co_ordinates = request.data.get('land_co_ordinates')
            land_status = request.data.get('land_status')
            area_meters = request.data.get('area_meters')
            area_acres = request.data.get('area_acres')
            industrial_jantri = request.data.get('industrial_jantri')
            jantri_value = request.data.get('jantri_value')
            mort_gaged = request.data.get('mort_gaged')
            seller_name = request.data.get('seller_name')
            buyer_name = request.data.get('buyer_name')
            actual_bucket = request.data.get('actual_bucket')
            remarks = request.data.get('remarks')
            index_number = request.data.get('index_number')
            tsr = request.data.get('tsr')
            advocate_name = request.data.get('advocate_name')
            total_land_area = request.data.get('total_land_area')
            # keypoints = request.data.getlist('keypoints[]') or request.data.get('keypoints') or []
            keypoints_raw = request.data.get('keypoints') or '[]'
            # Parse it into a Python list
            if isinstance(keypoints_raw, str):
                try:
                    keypoints = json.loads(keypoints_raw)
                except json.JSONDecodeError:
                    keypoints = []
            else:
                keypoints = keypoints_raw if isinstance(keypoints_raw, list) else []
            land_location_files = request.FILES.getlist('land_location_files') or []
            land_survey_number_files = request.FILES.getlist('land_survey_number_files') or []
            land_key_plan_files = request.FILES.getlist('land_key_plan_files') or []
            land_attach_approval_report_files = request.FILES.getlist('land_attach_approval_report_files') or []
            land_approach_road_files = request.FILES.getlist('land_approach_road_files') or []
            land_co_ordinates_files = request.FILES.getlist('land_co_ordinates_files') or []
            land_lease_deed_files = request.FILES.getlist('land_lease_deed_files') or []
            land_transmission_line_files = request.FILES.getlist('land_transmission_line_files') or []

            if not land_bank_id:
                return Response({"status": False, "message": "Land bank id is required", "data": []})
            

            if not land_name:
                return Response({"status": False, "message": "Land name is required", "data": []})

            if not block_number:
                return Response({"status": False, "message": "Block number is required", "data": []})

            if land_type =='buy' and not sale_deed_date:
                return Response({"status": False, "message": "Sale deed date is required", "data": []})
            
            if land_type =='buy' and not sale_deed_number:
                return Response({"status": False, "message": "Sale deed number is required", "data": []})

            if land_type =='lease' and not lease_deed_number:
                return Response({"status": False, "message": "Lease deed number is required", "data": []})
           
            if land_type =='lease' and not lease_deed_date:
                return Response({"status": False, "message": "Lease deed date is required", "data": []})

            if not survey_number:
                return Response({"status": False, "message": "Survey number is required", "data": []})

            if not village_name:
                return Response({"status": False, "message": "Village name is required", "data": []})
            
            if not district_name:
                return Response({"status": False, "message": "District name is required", "data": []})

            if not taluka_tahshil_name:
                return Response({"status": False, "message": "Taluka Tahsil name is required", "data": []})
            
            if not propose_gss_number:
                return Response({"status": False, "message": "Propose GSS number is required", "data": []})
            
            if not land_co_ordinates:
                return Response({"status": False, "message": "Land co-ordinates are required", "data": []})
            
            if not land_status:
                return Response({"status": False, "message": "Land status is required", "data": []})
            
            if not area_meters:
                return Response({"status": False, "message": "Area in meters is required", "data": []})
            
            if not area_acres:
                return Response({"status": False, "message": "Area in acres is required", "data": []})
            
            if not industrial_jantri:
                return Response({"status": False, "message": "Industrial Jantri is required", "data": []})
            
            if not jantri_value:
                return Response({"status": False, "message": "Jantri value is required", "data": []})
            
            if not mort_gaged:
                return Response({"status": False, "message": "Mort gaged is required", "data": []})
            
            if not seller_name:
                return Response({"status": False, "message": "Seller name is required", "data": []})
            
            if not buyer_name:
                return Response({"status": False, "message": "Buyer name is required", "data": []})
            
            if not actual_bucket:
                return Response({"status": False, "message": "Actual bucket is required", "data": []})
            
            if not remarks:
                return Response({"status": False, "message": "Remarks are required", "data": []})
            
            if not index_number:
                return Response({"status": False, "message": "Index number is required", "data": []})

            if not tsr:
                return Response({"status": False, "message": "TSR is required", "data": []})

            if not advocate_name:
                return Response({"status": False, "message": "Advocate name is required", "data": []})
            
            if not total_land_area:
                return Response({"status": False, "message": "Total land area is required", "data": []})            
           
            
            land = LandBankMaster.objects.get(id=land_bank_id)
            if not land:
                return Response({"status": False, "message": "Land not found", "data": []})

            land.land_name = land_name
            land.block_number = block_number
            land.land_type=land_type
            land.sale_deed_date = sale_deed_date
            land.sale_deed_number=sale_deed_number
            land.lease_deed_date = lease_deed_date
            land.lease_deed_number = lease_deed_number
            land.survey_number = survey_number
            land.village_name = village_name
            land.district_name = district_name
            land.taluka_tahshil_name = taluka_tahshil_name
            land.propose_gss_number = propose_gss_number
            land.land_co_ordinates = land_co_ordinates
            land.land_status = land_status
            land.area_meters = area_meters
            land.area_acres = area_acres
            land.industrial_jantri = industrial_jantri
            land.jantri_value = jantri_value
            land.mort_gaged = mort_gaged
            land.seller_name = seller_name
            land.buyer_name = buyer_name
            land.actual_bucket = actual_bucket
            land.remarks = remarks
            land.index_number = index_number
            land.tsr = tsr
            land.advocate_name = advocate_name
            land.total_land_area = total_land_area
            land.remaining_land_area = total_land_area
            land.keypoints = keypoints

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
            if land_lease_deed_files:
                for file in land_lease_deed_files:
                    land_lease_deed_attachments = LandLeaseDeedAttachment.objects.create(user=user, land_lease_deed_file=file)
                    land.lease_deed_file.add(land_lease_deed_attachments)
            if land_transmission_line_files:
                for file in land_transmission_line_files:
                    land_transmission_line_attachments = LandTransmissionLineAttachment.objects.create(user=user, land_transmission_line_file=file)
                    land.land_transmission_line_file.add(land_transmission_line_attachments)
            if (
                land_location_files and
                land_survey_number_files and
                land_key_plan_files and
                land_attach_approval_report_files and
                land_approach_road_files and
                land_co_ordinates_files and
                land_lease_deed_files and
                land_transmission_line_files
            ):
                land.is_land_bank_created = True
            else:
                land.is_land_bank_created = False
            land.is_land_bank_started = True

            land.save()
            # Serialize the created LandBankMaster instance
            # serializer = LandBankSerializer(land, context={'request': request})
            # data = serializer.data

            return Response({"status": True, "message": "Land Bank created successfully", "data": []})

        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            # Filter the queryset to include only records with is_land_bank_created=True
            queryset = self.filter_queryset(self.get_queryset().filter(is_land_bank_created=True)).order_by('-id')
            
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
            land_name = request.data.get('land_name')
            block_number = request.data.get('block_number')
            land_type=request.data.get('land_type')
            sale_deed_date = request.data.get('sale_deed_date')
            sale_deed_number=request.data.get('sale_deed_number')
            lease_deed_date = request.data.get('lease_deed_date')

            lease_deed_number = request.data.get('lease_deed_number')
            survey_number = request.data.get('survey_number')
            taluka_tahshil_name = request.data.get('taluka_tahshil_name')
            total_land_area = request.data.get('total_land_area')
            village_name = request.data.get('village_name')
            district_name = request.data.get('district_name')
            taluka_tahshil_name = request.data.get('taluka_tahshil_name')
            propose_gss_number = request.data.get('propose_gss_number')
            land_co_ordinates = request.data.get('land_co_ordinates')
            land_status = request.data.get('land_status')
            area_meters = request.data.get('area_meters')
            area_acres = request.data.get('area_acres')
            industrial_jantri = request.data.get('industrial_jantri')
            jantri_value = request.data.get('jantri_value')
            mort_gaged = request.data.get('mort_gaged')
            seller_name = request.data.get('seller_name')
            buyer_name = request.data.get('buyer_name')
            actual_bucket = request.data.get('actual_bucket')
            remarks = request.data.get('remarks')
            index_number = request.data.get('index_number')
            tsr = request.data.get('tsr')
            advocate_name = request.data.get('advocate_name')
            land_location_files = request.FILES.getlist('land_location_files') or []
            land_survey_number_files = request.FILES.getlist('land_survey_number_files') or []
            land_key_plan_files = request.FILES.getlist('land_key_plan_files') or []
            land_attach_approval_report_files = request.FILES.getlist('land_attach_approval_report_files') or []
            land_approach_road_files = request.FILES.getlist('land_approach_road_files') or []
            land_co_ordinates_files = request.FILES.getlist('land_co_ordinates_files') or []
            land_lease_deed_files = request.FILES.getlist('land_lease_deed_files') or []
            land_transmission_line_files = request.FILES.getlist('land_transmission_line_files') or []
            

            land_location_files_to_remove = request.data.get('land_location_files_to_remove', [])
            land_survey_number_files_to_remove = request.data.get('land_survey_number_files_to_remove', [])
            land_key_plan_files_to_remove = request.data.get('land_key_plan_files_to_remove', [])
            land_attach_approval_report_files_to_remove = request.data.get('land_attach_approval_report_files_to_remove', [])
            land_approach_road_files_to_remove = request.data.get('land_approach_road_files_to_remove', [])
            land_co_ordinates_files_to_remove = request.data.get('land_co_ordinates_files_to_remove', [])
            land_lease_deed_files_to_remove = request.data.get('land_lease_deed_files_to_remove', [])
            land_transmission_line_files_to_remove = request.data.get('land_transmission_line_files_to_remove', [])
            approved_report_files_to_remove = request.data.get('approved_report_files_to_remove', [])

            land_location_files_to_remove = process_file_ids(land_location_files_to_remove)
            land_survey_number_files_to_remove = process_file_ids(land_survey_number_files_to_remove)
            land_key_plan_files_to_remove = process_file_ids(land_key_plan_files_to_remove)
            land_attach_approval_report_files_to_remove = process_file_ids(land_attach_approval_report_files_to_remove)
            land_approach_road_files_to_remove = process_file_ids(land_approach_road_files_to_remove)
            land_co_ordinates_files_to_remove = process_file_ids(land_co_ordinates_files_to_remove)
            land_lease_deed_files_to_remove = process_file_ids(land_lease_deed_files_to_remove)
            land_transmission_line_files_to_remove = process_file_ids(land_transmission_line_files_to_remove)
            approved_report_files_to_remove = process_file_ids(approved_report_files_to_remove)

        

            if not land_name:
                return Response({"status": False, "message": "Land name is required", "data": []})
            
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            if not land_bank:
                return Response({"status": False, "message": "Land Bank data not found", "data": []})
            if land_name:
                land_bank.land_name = land_name
        
            if survey_number:
                land_bank.survey_number = survey_number
            if taluka_tahshil_name:
                land_bank.taluka_tahshil_name = taluka_tahshil_name
            if total_land_area:
                land_bank.total_land_area = total_land_area
                land_bank.remaining_land_area = total_land_area
            if village_name:
                land_bank.village_name = village_name
            if district_name:
                land_bank.district_name = district_name
            if taluka_tahshil_name:
                land_bank.taluka_tahshil_name = taluka_tahshil_name
            if propose_gss_number:
                land_bank.propose_gss_number = propose_gss_number
            if land_co_ordinates:
                land_bank.land_co_ordinates = land_co_ordinates
            if land_status:
                land_bank.land_status = land_status
            if area_meters:
                land_bank.area_meters = area_meters
            if area_acres:
                land_bank.area_acres = area_acres
            if industrial_jantri:
                land_bank.industrial_jantri = industrial_jantri
            if jantri_value:
                land_bank.jantri_value = jantri_value
            if mort_gaged:
                land_bank.mort_gaged = mort_gaged
            if seller_name:
                land_bank.seller_name = seller_name
            if buyer_name:
                land_bank.buyer_name = buyer_name
            if remarks:
                land_bank.remarks = remarks
            if advocate_name:
                land_bank.advocate_name = advocate_name
            if tsr:
                land_bank.tsr = tsr

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

            if land_lease_deed_files_to_remove:
                for file_id in land_lease_deed_files_to_remove:
                    try:
                        file_instance = LandLeaseDeedAttachment.objects.get(id=file_id)
                        land_bank.lease_deed_file.remove(file_instance)
                        file_instance.delete()
                    except LandLeaseDeedAttachment.DoesNotExist:
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

            if land_lease_deed_files:
                for file in land_lease_deed_files:
                    land_lease_deed_attachments = LandLeaseDeedAttachment.objects.create(user=land_bank.user, land_lease_deed_file=file)
                    land_bank.lease_deed_file.add(land_lease_deed_attachments)

            if land_transmission_line_files:
                for file in land_transmission_line_files:
                    land_transmission_line_attachments = LandTransmissionLineAttachment.objects.create(user=land_bank.user, land_transmission_line_file=file)
                    land_bank.land_transmission_line_file.add(land_transmission_line_attachments)
            if (
                land_location_files and
                land_survey_number_files and
                land_key_plan_files and
                land_attach_approval_report_files and
                land_approach_road_files and
                land_co_ordinates_files and
                land_lease_deed_files and
                land_transmission_line_files
            ):
                land_bank.is_land_bank_created = True
            else:
                land_bank.is_land_bank_created = False
            land_bank.save()
            serializer = LandBankSerializer(land_bank, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def destroy(self, request, *args, **kwargs):
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
            land_category = request.data.get('land_category')
            land_category_id = request.data.get('land_category_id')
            date_of_assessment = request.data.get('date_of_assessment')
            site_visit_date = request.data.get('site_visit_date')
            land_address = request.data.get('land_address')
            client_consultant = request.data.get("client_consultant", "")
            palnt_capacity = request.data.get('palnt_capacity')
            land_owner = request.data.get('land_owner')
            sfa_available_area_acres = request.data.get('sfa_available_area_acres')
            distance_from_main_road = request.data.get('distance_from_main_road')
            road_highway_details = request.data.get('road_highway_details')
            land_title = request.data.get('land_title')
            sfa_land_category = request.data.get('sfa_land_category')
            sfa_land_profile = request.data.get('sfa_land_profile')
            sfa_land_orientation = request.data.get('sfa_land_orientation')
            sfa_land_soil_testing_availability = request.data.get('sfa_land_soil_testing_availability')
            sfa_soil_bearing_capacity_files = request.FILES.getlist('sfa_soil_bearing_capacity_files') or []
            any_shadow_casting_buildings_or_hill = request.data.get('any_shadow_casting_buildings_or_hill')
            any_water_ponds_or_nalas_within_the_proposed_location = request.data.get('any_water_ponds_or_nalas_within_the_proposed_location')
            any_roads_or_bridge_within_the_proposed_location = request.data.get('any_roads_or_bridge_within_the_proposed_location')
            any_railway_lane_within_the_proposed_location = request.data.get('any_railway_lane_within_the_proposed_location')
            is_the_proposed_site_is_of_natural_contour_or_filled_up_area = request.data.get('is_the_proposed_site_is_of_natural_contour_or_filled_up_area')
            land_co_ordinates = request.data.get('land_co_cordinates')
            substation_cordinates = request.data.get('substation_cordinates')
            solar_isolation_data = request.data.get('solar_isolation_data')
            rain_fall_pattern = request.data.get('rain_fall_pattern')
            communication_network_availability = request.data.get('communication_network_availability')
            permission_required_for_power_generation = request.data.get('permission_required_for_power_generation')
            transmission_network_availabilty_above_400_220_33kv = request.data.get('transmission_network_availabilty_above_400_220_33kv')
            distance_of_supply_point_from_proposed_site = request.data.get('distance_of_supply_point_from_proposed_site')
            distance_of_nearest_substation_from_proposed_site = request.data.get('distance_of_nearest_substation_from_proposed_site')
            transmission_line_load_carrying_or_evacuation_capacity = request.data.get('transmission_line_load_carrying_or_evacuation_capacity')
            right_of_way_requirement_up_to_the_delivery_point = request.data.get('right_of_way_requirement_up_to_the_delivery_point')
            construction_power_availability_and_identify_source_distance = request.data.get('construction_power_availability_and_identify_source_distance')
            grid_availability_data_outage_pattern = request.data.get('grid_availability_data_outage_pattern')
            substation_capacity_mva = request.data.get('substation_capacity_mva')
            substation_load_side_voltage_level_kv = request.data.get('substation_load_side_voltage_level_kv')
            kv_grid_voltage_variation = request.data.get('kv_grid_voltage_variation')
            hz_grid_voltage_variation = request.data.get('hz_grid_voltage_variation')
            check_space_availability_in_substation_to_conct_power_by_area = request.data.get('check_space_availability_in_substation_to_conct_power_by_area')
            transformer_rating_in_substation = request.data.get('transformer_rating_in_substation')
            check_protection_system_details_of_substation = request.data.get('check_protection_system_details_of_substation')
            any_future_plan_for_expansion_of_substation = request.data.get('any_future_plan_for_expansion_of_substation')
            is_there_any_power_export_happening_at_substation = request.data.get('is_there_any_power_export_happening_at_substation')
            any_specific_requirements_of_eb_for_double_pole_structure = request.data.get('any_specific_requirements_of_eb_for_double_pole_structure')
            any_transmission_communication_line_passing_through_site = request.data.get('any_transmission_communication_line_passing_through_site')
            neighboring_area_or_vicinity_details = request.data.get('neighboring_area_or_vicinity_details')
            nearest_industry_category_and_distance = request.data.get('nearest_industry_category_and_distance')
            nearest_village_or_district_name_and_distance = request.data.get('nearest_village_or_district_name_and_distance')
            nearest_highway_or_airport_name_and_distance = request.data.get('nearest_highway_or_airport_name_and_distance')
            availability_of_labor_and_cost_of_labor = request.data.get('availability_of_labor_and_cost_of_labor')
            logistics = request.data.get('logistics')
            is_there_an_approach_road_available_to_the_site = request.data.get('is_there_an_approach_road_available_to_the_site')
            can_truck_of_Multi_axel_with_40_foot_container_reach_site = request.data.get('can_truck_of_Multi_axel_with_40_foot_container_reach_site')
            availability_of_vehicle_for_hiring_or_cost_per_km = request.data.get('availability_of_vehicle_for_hiring_or_cost_per_km')

            list_the_risks_including_journey = request.data.get('list_the_risks_including_journey')

            nearest_police_station_and_distance = request.data.get('nearest_police_station_and_distance')
            nearest_hospital_and_distance = request.data.get('nearest_hospital_and_distance')
            nearest_fire_station_and_distance = request.data.get('nearest_fire_station_and_distance')
            nearest_seashore_and_distance = request.data.get('nearest_seashore_and_distance')
            availability_of_accommodation_to_site_approximate_cost = request.data.get('availability_of_accommodation_to_site_approximate_cost')
            provide_near_by_civil_electrical_contractors = request.data.get('provide_near_by_civil_electrical_contractors')
            availability_of_construction_material_nearby = request.data.get('availability_of_construction_material_nearby')
            any_weather_station_nearby = request.data.get('any_weather_station_nearby')

            water_belt_profile_of_the_area = request.data.get('water_belt_profile_of_the_area')
            water_availability = request.data.get('water_availability')
            construction_water_availability = request.data.get('construction_water_availability')
            details_of_local_drainage_scheme = request.data.get('details_of_local_drainage_scheme')
            availability_of_potable_water = request.data.get('availability_of_potable_water')
    
            any_other_general_observation = request.data.get('any_other_general_observation')

            geo_coordinate_format = request.data.get('geo_coordinate_format')
            geo_easting = request.data.get('geo_graphical_easting')
            geo_northing = request.data.get('geo_graphical_northing')
            geo_zone = request.data.get('geo_graphical_zone')

            land_coordinate_format = request.data.get('land_co_coordinate_format')

            land_easting = request.data.get('land_co_easting')
            land_northing = request.data.get('land_co_northing')
            land_zone = request.data.get('land_co_zone')

            substation_coordinate_format = request.data.get('substation_coordinate_format')
            substation_easting = request.data.get('substation_easting')
            substation_northing = request.data.get('substation_northing')
            substation_zone = request.data.get('substation_zone')
            
            if not sfa_name:
                return Response({"status": False, "message": "SFA name is required", "data": []})
            if not land_sfa_file:
                return Response({"status": False, "message": "Land SFA file is required", "data": []})
            if not sfa_for_transmission_line_gss_files:
                return Response({"status": False, "message": "SFA for transmission line GSS files are required", "data": []})
        
            if not land_category_id:
                return Response({"status": False, "message": "Land category is required", "data": []})
            if not date_of_assessment:
                return Response({"status": False, "message": "Date of assessment is required", "data": []})
            if not site_visit_date:
                return Response({"status": False, "message": "Site visit date is required", "data": []})
            land_category_id = request.data.get('land_category_id')

            if not land_category_id:
                return Response({"status": False, "message": "Land category ID is required", "data": []})

            # Fetch the LandCategory instance
            land_category = get_object_or_404(LandCategory, id=land_category_id)

            created = LandBankMaster.objects.create(user = user, sfa_name = sfa_name, land_category = land_category,date_of_assessment = date_of_assessment,site_visit_date = site_visit_date,sfa_checked_by_user = user, 
                                                    land_address = land_address, client_consultant = client_consultant, palnt_capacity=palnt_capacity, land_owner = land_owner, sfa_available_area_acres = sfa_available_area_acres, distance_from_main_road = distance_from_main_road, road_highway_details = road_highway_details, land_title=land_title, sfa_land_category=sfa_land_category,
                                                    sfa_land_profile=sfa_land_profile, sfa_land_orientation=sfa_land_orientation, sfa_land_soil_testing_availability=sfa_land_soil_testing_availability, any_shadow_casting_buildings_or_hill=any_shadow_casting_buildings_or_hill, any_water_ponds_or_nalas_within_the_proposed_location=any_water_ponds_or_nalas_within_the_proposed_location, any_roads_or_bridge_within_the_proposed_location=any_roads_or_bridge_within_the_proposed_location, any_railway_lane_within_the_proposed_location=any_railway_lane_within_the_proposed_location, is_the_proposed_site_is_of_natural_contour_or_filled_up_area=is_the_proposed_site_is_of_natural_contour_or_filled_up_area,
                                                    land_co_ordinates=land_co_ordinates, substation_cordinates=substation_cordinates, solar_isolation_data=solar_isolation_data, rain_fall_pattern=rain_fall_pattern, communication_network_availability=communication_network_availability, permission_required_for_power_generation=permission_required_for_power_generation,
                                                    transmission_network_availabilty_above_400_220_33kv=transmission_network_availabilty_above_400_220_33kv, distance_of_supply_point_from_proposed_site=distance_of_supply_point_from_proposed_site, distance_of_nearest_substation_from_proposed_site=distance_of_nearest_substation_from_proposed_site, transmission_line_load_carrying_or_evacuation_capacity=transmission_line_load_carrying_or_evacuation_capacity, right_of_way_requirement_up_to_the_delivery_point=right_of_way_requirement_up_to_the_delivery_point, construction_power_availability_and_identify_source_distance=construction_power_availability_and_identify_source_distance, grid_availability_data_outage_pattern=grid_availability_data_outage_pattern, substation_capacity_mva=substation_capacity_mva, substation_load_side_voltage_level_kv=substation_load_side_voltage_level_kv,
                                                    kv_grid_voltage_variation=kv_grid_voltage_variation, hz_grid_voltage_variation=hz_grid_voltage_variation, check_space_availability_in_substation_to_conct_power_by_area=check_space_availability_in_substation_to_conct_power_by_area, transformer_rating_in_substation=transformer_rating_in_substation, check_protection_system_details_of_substation=check_protection_system_details_of_substation, any_future_plan_for_expansion_of_substation=any_future_plan_for_expansion_of_substation, is_there_any_power_export_happening_at_substation=is_there_any_power_export_happening_at_substation, any_specific_requirements_of_eb_for_double_pole_structure=any_specific_requirements_of_eb_for_double_pole_structure, any_transmission_communication_line_passing_through_site = any_transmission_communication_line_passing_through_site, neighboring_area_or_vicinity_details=neighboring_area_or_vicinity_details, nearest_industry_category_and_distance=nearest_industry_category_and_distance, nearest_village_or_district_name_and_distance = nearest_village_or_district_name_and_distance, nearest_highway_or_airport_name_and_distance=nearest_highway_or_airport_name_and_distance, availability_of_labor_and_cost_of_labor=availability_of_labor_and_cost_of_labor, logistics=logistics, 
                                                    is_there_an_approach_road_available_to_the_site=is_there_an_approach_road_available_to_the_site, can_truck_of_Multi_axel_with_40_foot_container_reach_site=can_truck_of_Multi_axel_with_40_foot_container_reach_site, availability_of_vehicle_for_hiring_or_cost_per_km=availability_of_vehicle_for_hiring_or_cost_per_km, list_the_risks_including_journey=list_the_risks_including_journey, nearest_police_station_and_distance=nearest_police_station_and_distance, nearest_hospital_and_distance=nearest_hospital_and_distance, nearest_fire_station_and_distance=nearest_fire_station_and_distance, nearest_seashore_and_distance=nearest_seashore_and_distance, availability_of_accommodation_to_site_approximate_cost=availability_of_accommodation_to_site_approximate_cost, provide_near_by_civil_electrical_contractors=provide_near_by_civil_electrical_contractors, availability_of_construction_material_nearby=availability_of_construction_material_nearby, any_weather_station_nearby=any_weather_station_nearby, water_belt_profile_of_the_area=water_belt_profile_of_the_area, water_availability=water_availability, construction_water_availability=construction_water_availability, details_of_local_drainage_scheme=details_of_local_drainage_scheme, availability_of_potable_water=availability_of_potable_water,
                                                    any_other_general_observation=any_other_general_observation,geo_coordinate_format=geo_coordinate_format,geo_easting=geo_easting,geo_northing=geo_northing,geo_zone=geo_zone,land_coordinate_format=land_coordinate_format,land_easting=land_easting,land_northing=land_northing,land_zone=land_zone,substation_coordinate_format=substation_coordinate_format,substation_easting=substation_easting,substation_northing=substation_northing,substation_zone=substation_zone,)
            for file in land_sfa_file:
                land_sfa_attachments = SFAAttachment.objects.create(user=user, land_sfa_file=file)
                created.land_sfa_file.add(land_sfa_attachments)

            for file in sfa_for_transmission_line_gss_files:
                sfa_for_transmission_line_gss_attachments = SFAforTransmissionLineGSSAttachment.objects.create(user=user, sfa_for_transmission_line_gss_files=file)
                created.sfa_for_transmission_line_gss_files.add(sfa_for_transmission_line_gss_attachments)

            for file in sfa_soil_bearing_capacity_files:
                sfa_soil_bearing_capacity_attachments = SfaSoilBearingCapacityAttachment.objects.create(user=user, sfa_soil_bearing_capacity_files=file)
                created.sfa_soil_bearing_capacity_files.add(sfa_soil_bearing_capacity_attachments)

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
            land_address = request.data.get('land_address')
            client_consultant = request.data.get("client_consultant", None)
            palnt_capacity = request.data.get('palnt_capacity')
            land_owner = request.data.get('land_owner')
            sfa_available_area_acres = request.data.get('sfa_available_area_acres')
            distance_from_main_road = request.data.get('distance_from_main_road')
            road_highway_details = request.data.get('road_highway_details')
            land_title = request.data.get('land_title', None)
            sfa_land_category = request.data.get('sfa_land_category')
            sfa_land_profile = request.data.get('sfa_land_profile')
            sfa_land_orientation = request.data.get('sfa_land_orientation', None)
            sfa_land_soil_testing_availability = request.data.get('sfa_land_soil_testing_availability')
            sfa_soil_bearing_capacity_files = request.FILES.getlist('sfa_soil_bearing_capacity_files') or []
            remove_sfa_soil_bearing_capacity_files = request.FILES.getlist('remove_sfa_soil_bearing_capacity_files') or []
            any_shadow_casting_buildings_or_hill = request.data.get('any_shadow_casting_buildings_or_hill')
            any_water_ponds_or_nalas_within_the_proposed_location = request.data.get('any_water_ponds_or_nalas_within_the_proposed_location')
            any_roads_or_bridge_within_the_proposed_location = request.data.get('any_roads_or_bridge_within_the_proposed_location')
            any_railway_lane_within_the_proposed_location = request.data.get('any_railway_lane_within_the_proposed_location')
            is_the_proposed_site_is_of_natural_contour_or_filled_up_area = request.data.get('is_the_proposed_site_is_of_natural_contour_or_filled_up_area')
            land_co_ordinates = request.data.get('land_co_ordinates')
            substation_cordinates = request.data.get('substation_cordinates')
            solar_isolation_data = request.data.get('solar_isolation_data')
            rain_fall_pattern = request.data.get('rain_fall_pattern')
            communication_network_availability = request.data.get('communication_network_availability')
            permission_required_for_power_generation = request.data.get('permission_required_for_power_generation')
            transmission_network_availabilty_above_400_220_33kv = request.data.get('transmission_network_availabilty_above_400_220_33kv')
            distance_of_supply_point_from_proposed_site = request.data.get('distance_of_supply_point_from_proposed_site')
            distance_of_nearest_substation_from_proposed_site = request.data.get('distance_of_nearest_substation_from_proposed_site')
            transmission_line_load_carrying_or_evacuation_capacity = request.data.get('transmission_line_load_carrying_or_evacuation_capacity',None)
            right_of_way_requirement_up_to_the_delivery_point = request.data.get('right_of_way_requirement_up_to_the_delivery_point')
            construction_power_availability_and_identify_source_distance = request.data.get('construction_power_availability_and_identify_source_distance',None)
            grid_availability_data_outage_pattern = request.data.get('grid_availability_data_outage_pattern',None)
            substation_capacity_mva = request.data.get('substation_capacity_mva')
            substation_load_side_voltage_level_kv = request.data.get('substation_load_side_voltage_level_kv')
            kv_grid_voltage_variation = request.data.get('kv_grid_voltage_variation',None)
            hz_grid_voltage_variation = request.data.get('hz_grid_voltage_variation',None)
            check_space_availability_in_substation_to_conct_power_by_area = request.data.get('check_space_availability_in_substation_to_conct_power_by_area')
            transformer_rating_in_substation = request.data.get('transformer_rating_in_substation')
            check_protection_system_details_of_substation = request.data.get('check_protection_system_details_of_substation',None)
            any_future_plan_for_expansion_of_substation = request.data.get('any_future_plan_for_expansion_of_substation',None)
            is_there_any_power_export_happening_at_substation = request.data.get('is_there_any_power_export_happening_at_substation',None)
            any_specific_requirements_of_eb_for_double_pole_structure = request.data.get('any_specific_requirements_of_eb_for_double_pole_structure',None)
            any_transmission_communication_line_passing_through_site = request.data.get('any_transmission_communication_line_passing_through_site')
            neighboring_area_or_vicinity_details = request.data.get('neighboring_area_or_vicinity_details')
            nearest_industry_category_and_distance = request.data.get('nearest_industry_category_and_distance',None)
            nearest_village_or_district_name_and_distance = request.data.get('nearest_village_or_district_name_and_distance')
            nearest_highway_or_airport_name_and_distance = request.data.get('nearest_highway_or_airport_name_and_distance')
            availability_of_labor_and_cost_of_labor = request.data.get('availability_of_labor_and_cost_of_labor',None)
            logistics = request.data.get('logistics')
            is_there_an_approach_road_available_to_the_site = request.data.get('is_there_an_approach_road_available_to_the_site')
            can_truck_of_Multi_axel_with_40_foot_container_reach_site = request.data.get('can_truck_of_Multi_axel_with_40_foot_container_reach_site')
            availability_of_vehicle_for_hiring_or_cost_per_km = request.data.get('availability_of_vehicle_for_hiring_or_cost_per_km')

            list_the_risks_including_journey = request.data.get('list_the_risks_including_journey')

            nearest_police_station_and_distance = request.data.get('nearest_police_station_and_distance')
            nearest_hospital_and_distance = request.data.get('nearest_hospital_and_distance')
            nearest_fire_station_and_distance = request.data.get('nearest_fire_station_and_distance')
            nearest_seashore_and_distance = request.data.get('nearest_seashore_and_distance')
            availability_of_accommodation_to_site_approximate_cost = request.data.get('availability_of_accommodation_to_site_approximate_cost')
            provide_near_by_civil_electrical_contractors = request.data.get('provide_near_by_civil_electrical_contractors',None)
            availability_of_construction_material_nearby = request.data.get('availability_of_construction_material_nearby',None)
            any_weather_station_nearby = request.data.get('any_weather_station_nearby',None)

            water_belt_profile_of_the_area = request.data.get('water_belt_profile_of_the_area',None)
            water_availability = request.data.get('water_availability',None)
            construction_water_availability = request.data.get('construction_water_availability',None)
            details_of_local_drainage_scheme = request.data.get('details_of_local_drainage_scheme',None)
            availability_of_potable_water = request.data.get('availability_of_potable_water',None)

            geo_coordinate_format = request.data.get('geo_coordinate_format')
            geo_easting = request.data.get('geo_easting')
            geo_northing = request.data.get('geo_northing')
            geo_zone = request.data.get('geo_zone')

            land_coordinate_format = request.data.get('land_coordinate_format')
            land_easting = request.data.get('land_easting')
            land_northing = request.data.get('land_northing')
            land_zone = request.data.get('land_zone')

            substation_coordinate_format = request.data.get('substation_coordinate_format')
            substation_easting = request.data.get('substation_easting')
            substation_northing = request.data.get('substation_northing')
            substation_zone = request.data.get('substation_zone')
    
            any_other_general_observation = request.data.get('any_other_general_observation')

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
            if land_address:
                land_bank.land_address = land_address
            if client_consultant:
                land_bank.client_consultant = client_consultant
            if palnt_capacity:
                land_bank.palnt_capacity = palnt_capacity
            if land_owner:
                land_bank.land_owner = land_owner
            if sfa_available_area_acres:
                land_bank.sfa_available_area_acres = sfa_available_area_acres
            if distance_from_main_road:
                land_bank.distance_from_main_road = distance_from_main_road
            if road_highway_details:
                land_bank.road_highway_details = road_highway_details
            if land_title:
                land_bank.land_title = land_title
            if sfa_land_category:
                land_bank.sfa_land_category = sfa_land_category
            if sfa_land_profile:
                land_bank.sfa_land_profile = sfa_land_profile
            if sfa_land_orientation:
                land_bank.sfa_land_orientation = sfa_land_orientation
            if sfa_land_soil_testing_availability:
                land_bank.sfa_land_soil_testing_availability = sfa_land_soil_testing_availability
            if any_shadow_casting_buildings_or_hill:
                land_bank.any_shadow_casting_buildings_or_hill = any_shadow_casting_buildings_or_hill
            if any_water_ponds_or_nalas_within_the_proposed_location:
                land_bank.any_water_ponds_or_nalas_within_the_proposed_location = any_water_ponds_or_nalas_within_the_proposed_location
            if any_roads_or_bridge_within_the_proposed_location:
                land_bank.any_roads_or_bridge_within_the_proposed_location = any_roads_or_bridge_within_the_proposed_location
            if any_railway_lane_within_the_proposed_location:
                land_bank.any_railway_lane_within_the_proposed_location = any_railway_lane_within_the_proposed_location
            if is_the_proposed_site_is_of_natural_contour_or_filled_up_area:
                land_bank.is_the_proposed_site_is_of_natural_contour_or_filled_up_area = is_the_proposed_site_is_of_natural_contour_or_filled_up_area
            
            if land_co_ordinates:
                land_bank.land_co_ordinates = land_co_ordinates
            if substation_cordinates:
                land_bank.substation_cordinates = substation_cordinates
            if solar_isolation_data:
                land_bank.solar_isolation_data = solar_isolation_data
            if rain_fall_pattern:
                land_bank.rain_fall_pattern = rain_fall_pattern
            if communication_network_availability:
                land_bank.communication_network_availability = communication_network_availability
            if permission_required_for_power_generation:
                land_bank.permission_required_for_power_generation = permission_required_for_power_generation
            if transmission_network_availabilty_above_400_220_33kv:
                land_bank.transmission_network_availabilty_above_400_220_33kv = transmission_network_availabilty_above_400_220_33kv
            if distance_of_supply_point_from_proposed_site:
                land_bank.distance_of_supply_point_from_proposed_site = distance_of_supply_point_from_proposed_site
            if distance_of_nearest_substation_from_proposed_site:
                land_bank.distance_of_nearest_substation_from_proposed_site = distance_of_nearest_substation_from_proposed_site
            if transmission_line_load_carrying_or_evacuation_capacity:
                land_bank.transmission_line_load_carrying_or_evacuation_capacity = transmission_line_load_carrying_or_evacuation_capacity
            if right_of_way_requirement_up_to_the_delivery_point:
                land_bank.right_of_way_requirement_up_to_the_delivery_point = right_of_way_requirement_up_to_the_delivery_point
            if construction_power_availability_and_identify_source_distance:
                land_bank.construction_power_availability_and_identify_source_distance = construction_power_availability_and_identify_source_distance
            if grid_availability_data_outage_pattern:
                land_bank.grid_availability_data_outage_pattern = grid_availability_data_outage_pattern
            if substation_capacity_mva:
                land_bank.substation_capacity_mva = substation_capacity_mva
            if substation_load_side_voltage_level_kv:
                land_bank.substation_load_side_voltage_level_kv = substation_load_side_voltage_level_kv
            if kv_grid_voltage_variation:
                land_bank.kv_grid_voltage_variation = kv_grid_voltage_variation
            if hz_grid_voltage_variation:
                land_bank.hz_grid_voltage_variation = hz_grid_voltage_variation
            if check_space_availability_in_substation_to_conct_power_by_area:
                land_bank.check_space_availability_in_substation_to_conct_power_by_area = check_space_availability_in_substation_to_conct_power_by_area
            if transformer_rating_in_substation:
                land_bank.transformer_rating_in_substation = transformer_rating_in_substation
            if check_protection_system_details_of_substation:
                land_bank.check_protection_system_details_of_substation = check_protection_system_details_of_substation
            if any_future_plan_for_expansion_of_substation:
                land_bank.any_future_plan_for_expansion_of_substation = any_future_plan_for_expansion_of_substation
            if is_there_any_power_export_happening_at_substation:
                land_bank.is_there_any_power_export_happening_at_substation = is_there_any_power_export_happening_at_substation
            if any_specific_requirements_of_eb_for_double_pole_structure:
                land_bank.any_specific_requirements_of_eb_for_double_pole_structure = any_specific_requirements_of_eb_for_double_pole_structure
            if any_transmission_communication_line_passing_through_site:
                land_bank.any_transmission_communication_line_passing_through_site = any_transmission_communication_line_passing_through_site
            if neighboring_area_or_vicinity_details:
                land_bank.neighboring_area_or_vicinity_details = neighboring_area_or_vicinity_details
            if nearest_industry_category_and_distance:
                land_bank.nearest_industry_category_and_distance = nearest_industry_category_and_distance
            if nearest_village_or_district_name_and_distance:
                land_bank.nearest_village_or_district_name_and_distance = nearest_village_or_district_name_and_distance
            if nearest_highway_or_airport_name_and_distance:
                land_bank.nearest_highway_or_airport_name_and_distance = nearest_highway_or_airport_name_and_distance
            if availability_of_labor_and_cost_of_labor:
                land_bank.availability_of_labor_and_cost_of_labor = availability_of_labor_and_cost_of_labor
            if logistics:
                land_bank.logistics = logistics
            if is_there_an_approach_road_available_to_the_site:
                land_bank.is_there_an_approach_road_available_to_the_site = is_there_an_approach_road_available_to_the_site
            if can_truck_of_Multi_axel_with_40_foot_container_reach_site:
                land_bank.can_truck_of_Multi_axel_with_40_foot_container_reach_site = can_truck_of_Multi_axel_with_40_foot_container_reach_site
            if availability_of_vehicle_for_hiring_or_cost_per_km:
                land_bank.availability_of_vehicle_for_hiring_or_cost_per_km = availability_of_vehicle_for_hiring_or_cost_per_km
            if list_the_risks_including_journey:
                land_bank.list_the_risks_including_journey = list_the_risks_including_journey
            if nearest_police_station_and_distance:
                land_bank.nearest_police_station_and_distance = nearest_police_station_and_distance
            if nearest_hospital_and_distance:
                land_bank.nearest_hospital_and_distance = nearest_hospital_and_distance
            if nearest_fire_station_and_distance:
                land_bank.nearest_fire_station_and_distance = nearest_fire_station_and_distance
            if nearest_seashore_and_distance:
                land_bank.nearest_seashore_and_distance = nearest_seashore_and_distance
            if availability_of_accommodation_to_site_approximate_cost:
                land_bank.availability_of_accommodation_to_site_approximate_cost = availability_of_accommodation_to_site_approximate_cost
            if provide_near_by_civil_electrical_contractors:
                land_bank.provide_near_by_civil_electrical_contractors = provide_near_by_civil_electrical_contractors
            if availability_of_construction_material_nearby is not None:
                land_bank.availability_of_construction_material_nearby = availability_of_construction_material_nearby
            if any_weather_station_nearby:
                land_bank.any_weather_station_nearby = any_weather_station_nearby
            if water_belt_profile_of_the_area:
                land_bank.water_belt_profile_of_the_area = water_belt_profile_of_the_area
            if water_availability:
                land_bank.water_availability = water_availability
            if construction_water_availability:
                land_bank.construction_water_availability = construction_water_availability
            if details_of_local_drainage_scheme:
                land_bank.details_of_local_drainage_scheme = details_of_local_drainage_scheme
            if availability_of_potable_water:
                land_bank.availability_of_potable_water = availability_of_potable_water
            if any_other_general_observation:
                land_bank.any_other_general_observation = any_other_general_observation

            if geo_coordinate_format:
                land_bank.geo_coordinate_format = geo_coordinate_format
            if geo_easting:
                land_bank.geo_easting = geo_easting
            if geo_northing:
                land_bank.geo_northing = geo_northing
            if geo_zone:
                land_bank.geo_zone = geo_zone

            if land_coordinate_format:
                land_bank.land_coordinate_format = land_coordinate_format
            if land_easting:
                land_bank.land_easting = land_easting
            if land_northing:
                land_bank.land_northing = land_northing
            if land_zone:
                land_bank.land_zone = land_zone

            if substation_coordinate_format:
                land_bank.substation_coordinate_format = substation_coordinate_format
            if substation_easting:
                land_bank.substation_easting = substation_easting
            if substation_northing:
                land_bank.substation_northing = substation_northing
            if substation_zone:
                land_bank.substation_zone = substation_zone    


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

            if sfa_soil_bearing_capacity_files:
                for file in sfa_soil_bearing_capacity_files:
                    sfa_soil_bearing_capacity_attachments = SfaSoilBearingCapacityAttachment.objects.create(user=user, sfa_soil_bearing_capacity_files=file)
                    land_bank.sfa_soil_bearing_capacity_files.add(sfa_soil_bearing_capacity_attachments)

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
            if remove_sfa_soil_bearing_capacity_files:
                if isinstance(remove_sfa_soil_bearing_capacity_files, str):
                    remove_sfa_soil_bearing_capacity_files = [int(file_id) for file_id in remove_sfa_soil_bearing_capacity_files.split(',')]
                else:
                    remove_sfa_soil_bearing_capacity_files = [int(file_id) for file_id in remove_sfa_soil_bearing_capacity_files]
                
                for file_id in remove_sfa_soil_bearing_capacity_files:
                    try:
                        sfa_soil_bearing_capacity_attachments = SfaSoilBearingCapacityAttachment.objects.get(id=file_id)
                        sfa_soil_bearing_capacity_attachments.delete()
                    except SfaSoilBearingCapacityAttachment.DoesNotExist:
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
        
class ApproveRejectLandBankDataByProjectHODViewset(viewsets.ModelViewSet):
    queryset = LandBankMaster.objects.all()
    serializer_class = LandBankSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_bank_id = self.kwargs.get('land_bank_id')
            land_bank = LandBankMaster.objects.get(id=land_bank_id)
            is_land_bank_approved_by_project_hod = request.data.get('is_land_bank_approved_by_project_hod')
            approved_report_files = request.FILES.getlist('approved_report_files') or []
            if not is_land_bank_approved_by_project_hod:
                return Response({"status": False, "message": "Land bank approval status is required", "data": []})
            if not approved_report_files:
                return Response({"status": False, "message": "Approval Report Files are required", "data": []})

            if is_land_bank_approved_by_project_hod== "Approved":
                land_bank.is_land_bank_approved_by_project_hod = is_land_bank_approved_by_project_hod
                land_bank.land_bank_approved_by_user = user
                
                for file in approved_report_files:
                    approved_report_attachments = LandApprovedReportAttachment.objects.create(user=land_bank.user, approved_report_file=file)
                    land_bank.approved_report_file.add(approved_report_attachments)
                    land_bank.save()
                approved_obj = SaveApprovalDataOfStatusOfSiteVisit.objects.create(land_bank=land_bank, user=user, is_land_bank_approved_by_project_hod=is_land_bank_approved_by_project_hod)
                approved_obj.save()
                land_bank.save()
                serializer = LandBankSerializer(land_bank, context={'request': request})
                data = serializer.data
                return Response({"status": True, "message": "Land approved successfully", "data": data})
            
            if is_land_bank_approved_by_project_hod == "Rejected":
                land_bank.is_land_bank_approved_by_project_hod = is_land_bank_approved_by_project_hod
                land_bank.land_bank_rejected_by_user = user
                approved_obj = SaveRejectDataOfStatusOfSiteVisit.objects.create(land_bank=land_bank, user=user, is_land_bank_approved_by_project_hod=is_land_bank_approved_by_project_hod)
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
            # if LandBankAfterApprovedData.objects.filter(land_bank=land_bank, is_filled_22_forms=True).exists():
            #     return Response({"status": False, "message": "You have already filled this form", "data": []})
            
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

            land_bank_after_approved_data = LandBankAfterApprovedData.objects.create(land_bank=land_bank, user=user,is_filled_22_forms=True)
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
            land_bank.is_land_bank_added_attachment=True
            land_bank_after_approved_data.save()
            land_bank.save()
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

            remove_dilr_attachment_file = request.data.get('remove_dilr_attachment_file', []) or []
            remove_na_65b_permission_attachment_file = request.data.get('remove_na_65b_permission_attachment_file', []) or []
            remove_revenue_7_12_records_attachment = request.data.get('remove_revenue_7_12_records_attachment') or []
            remove_noc_from_forest_and_amp_attachment_file = request.data.get('remove_noc_from_forest_and_amp_attachment_file', []) or []
            remove_noc_from_geology_and_mining_office_attachment_file = request.data.get('remove_noc_from_geology_and_mining_office_attachment_file', []) or []
            remove_approvals_required_for_transmission_attachment_file = request.data.get('remove_approvals_required_for_transmission_attachment_file', []) or []
            remove_canal_crossing_attachment_file = request.data.get('remove_canal_crossing_attachment_file', []) or []
            remove_lease_deed_attachment_file = request.data.get('remove_lease_deed_attachment_file', []) or []
            remove_railway_crossing_attachment_file = request.data.get('remove_railway_crossing_attachment_file', []) or []
            remove_any_gas_pipeline_crossing_attachment_file = request.data.get('remove_any_gas_pipeline_crossing_attachment_file', []) or []
            remove_road_crossing_permission_attachment_file = request.data.get('remove_road_crossing_permission_attachment_file', []) or []
            remove_any_transmission_line_crossing_permission_attachment_file = request.data.get('remove_any_transmission_line_crossing_permission_attachment_file', []) or []
            remove_any_transmission_line_shifting_permission_attachment_file = request.data.get('remove_any_transmission_line_shifting_permission_attachment_file', []) or []
            remove_gram_panchayat_permission_attachment_file = request.data.get('remove_gram_panchayat_permission_attachment_file', []) or []
            remove_municipal_corporation_permission_file = request.data.get('remove_municipal_corporation_permission_file', []) or []
            remove_list_of_other_approvals_land_file = request.data.get('remove_list_of_other_approvals_land_file', []) or []
            remove_title_search_report_file = request.data.get('remove_title_search_report_file', []) or []
            remove_coordinate_verification_file = request.data.get('remove_coordinate_verification_file', []) or []
            remove_encumbrance_noc_file = request.data.get('remove_encumbrance_noc_file', []) or []
            remove_developer_permission_file = request.data.get('remove_developer_permission_file', []) or []
            remove_noc_from_ministry_of_defence_file = request.data.get('remove_noc_from_ministry_of_defence_file', []) or []
            remove_list_of_approvals_required_for_transmission_line_file = request.data.get('remove_list_of_approvals_required_for_transmission_line_file', []) or []
            
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
        
class UpdateLandSurvetNumberViewset(viewsets.ModelViewSet):
    queryset = LandSurveyNumber.objects.all().order_by('-id')
    serializer_class = LandSurveyNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            land_survey_number_id = self.kwargs.get('land_survey_number_id')
            land_survey_number = LandSurveyNumber.objects.get(id=land_survey_number_id)
            land_survey_number_new = request.data.get('land_survey_number')
            land_survey_number.land_survey_number = land_survey_number_new
            land_survey_number.save()
            
            serializer = LandSurveyNumberSerializer(land_survey_number, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land survey number updated successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

from openpyxl import Workbook
from openpyxl.styles import Font
from django.http import HttpResponse
class LandbankExcelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Land Bank Data'

        headers = [
            "Sn", "Land Bank Name", "Area- Acre", "Survey No", "Village", "Taluka",
            "District", "Land Lease Date",
            "Leaser", "Leasee", "Lease Rate/Acre", "ROW if any",
            "Connectivity Voltage"
        ]
        sheet.append(headers)

        for cell in sheet[1]:
            cell.font = Font(bold=True)

        landbanks = LandBankMaster.objects.all()
        for i, land in enumerate(landbanks, start=1):
            row = [
                i,
                land.land_name,
                land.area_acres,
                land.survey_number,
                land.village_name,
                land.taluka_tahshil_name,
                land.district_name,
                land.sale_deed_date.strftime('%Y-%m-%d') if land.sale_deed_date else '',
                land.seller_name,
                land.buyer_name,
                land.industrial_jantri,
                land.right_of_way_requirement_up_to_the_delivery_point,
                land.substation_load_side_voltage_level_kv,
            ]
            sheet.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=LandBankData.xlsx'
        workbook.save(response)
        return response