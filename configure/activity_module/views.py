from django.shortcuts import render
from user_profile.models import *
from activity_module.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from activity_module.serializers import *
from rest_framework.permissions import IsAuthenticated



class ProjectActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProjectActivity.objects.all()
    serializer_class = ProjectMainActivitySerializer

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            solar_or_wind = request.data.get('solar_or_wind')
            activity_name = request.data.get('activity_name')

            if not activity_name:
                return Response({"status": False, "message": "activity_name is required."})

            activity = ProjectActivity.objects.create(
                user=user,
                solar_or_wind=solar_or_wind,
                activity_name=activity_name,
            )

            return Response(
                {"status": True, "message": "Activity created successfully."})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            if queryset.exists():
                serializer_data = []
                for obj in queryset:
                    context = {'request' : request}
                    serializer = ProjectMainActivitySerializer(obj,context=context)
                    serializer_data.append(serializer.data)
                    
                count = len(serializer_data)
                return Response({
                    "status": True,
                    "message": "Department data fetched successfully",
                    'total_page': 1,
                    'total': count,
                    'data': serializer_data
                })
            else:
                return Response({
                    "status": True,
                    "message": "No Department found",
                    "total_page": 0,
                    "total": 0,
                    "data": []
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})
        
class ProjectActivityUpdateViewSet(viewsets.ModelViewSet):
    queryset = ProjectActivity.objects.all()

    def update(self, request, *args, **kwargs):

        try:
            # Get the activity ID from the URL kwargs
            activity_id = self.kwargs.get('activity_id')
            if not activity_id:
                return Response({"status": False, "message": "Activity not found."})
            
            activity = ProjectActivity.objects.filter(id=activity_id).first()
            solar_or_wind = request.data.get('solar_or_wind')
            activity_name = request.data.get('activity_name')
            
            # Retrieve the activity object
            
            # Update the activity object
            if solar_or_wind :
                activity.solar_or_wind = solar_or_wind
            if activity_name :
                activity.activity_name = activity_name
            activity.save()

            return Response({"status": True, "message": "Activity updated successfully."})
        except Exception as e:
            return Response({"status": False, "message": str(e)})