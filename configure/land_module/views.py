from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from user_profile.models import *
from land_module.models import *
from land_module.serializers import *

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
            land_category_id = request.data.get('land_category_id')
            land_name = request.data.get('land_name')
            solar_or_winds = request.data.get('solar_or_winds')
            land_location_files = request.FILES.getlist('land_location_files',[])
            land_survey_number_files = request.FILES.getlist('land_survey_number_files',[])
            land_key_plan_files = request.FILES.getlist('land_key_plan_files',[])
            land_attach_approval_report_files = request.FILES.getlist('land_attach_approval_report_files',[])
            land_approach_road_files = request.FILES.getlist('land_approach_road_files',[])
            land_co_ordinates_files = request.FILES.getlist('land_co_ordinates_files',[])
            land_proposed_gss_files = request.FILES.getlist('land_proposed_gss_files',[])
            land_transmission_line_files = request.FILES.getlist('land_transmission_line_files',[])

            if not land_category_id:
                return Response({"status": False, "message": "Land category is required", "data": []})

            if not land_name:
                return Response({"status": False, "message": "Land name is required", "data": []})

            if not solar_or_winds:
                return Response({"status": False, "message": "please select solar or winds", "data": []})
            
            if land_category_id:
                land_category = LandCategory.objects.get(id=land_category_id)

            land = LandBankMaster.objects.create(user=user, land_category=land_category, land_name=land_name, solar_or_winds=solar_or_winds)
            if land_location_files:
                for file in land_location_files:
                    land_location_attachments = LandLocationAttachment.objects.create(user=user, land_location_file=file)
                    land.land_location_file.add(land_location_attachments)
            if land_survey_number_files:
                for file in land_key_plan_files:
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

            serializer = LandBankSerializer(land, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Land created successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
