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
        

class ActiveDeactiveActivityProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectActivity.objects.all()
    serializer_class = ProjectMainActivitySerializer

    def update(self, request, *args, **kwargs):
        try:
            activity_id = self.kwargs.get('activity_id')
            if not activity_id:
                return Response({"status": False, "message": "Activity not found."})
            
            project_activity_data = ProjectActivity.objects.get(id=activity_id)
            if not project_activity_data:
                return Response({"status": False, "message": "Activity not found."})
            
            if project_activity_data.is_active:
                project_activity_data.is_active = False
                project_activity_data.save()
                
                project_sub_activity_data = SubActivityName.objects.filter(project_main_activity=project_activity_data)
                if project_sub_activity_data.exists():
                    for sub_activity in project_sub_activity_data:
                        sub_activity.is_active = False
                        sub_activity.save()
                    
                    project_sub_sub_activity_data = SubSubActivityName.objects.filter(sub_activity_id__in=project_sub_activity_data)
                    if project_sub_sub_activity_data.exists():
                        for sub_sub_activity in project_sub_sub_activity_data:
                            sub_sub_activity.is_active = False
                            sub_sub_activity.save()

                return Response({"status": True, "message": "Activity and related sub-activities deactivated successfully."})
            
            else:
                project_activity_data.is_active = True
                project_activity_data.save()
                return Response({"status": True, "message": "Activity reactivated successfully."})
            
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class GetActiveActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectMainActivitySerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = ProjectActivity.objects.filter(is_active=True)
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
                    'total': count,
                    'data': serializer_data
                })
        except Exception as e:
            return Response({"status": False, 'message': 'Something went wrong', 'error': str(e)})

        
class SubActivityNameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubActivityName.objects.all()
    serializer_class = SubActivityNameSerializer

    def create(self, request, *args, **kwargs):
        try:
            project_activity_id = request.data.get("project_activity_id")
            sub_activity_names = request.data.get("sub_activity_names", [])

            if not project_activity_id:
                return Response({"status": False, "message": "project_activity_id is required."})

            try:
                project_activity = ProjectActivity.objects.get(id=project_activity_id)
            except ProjectActivity.DoesNotExist:
                return Response({"status": False, "message": "Invalid project_activity_id."})

            if not sub_activity_names:
                return Response({"status": False, "message": "sub activity names must be a non-empty list."})

                
            created_ids = []
            for name in sub_activity_names:
                # Create a SubActivity for each name
                sub_activity = SubActivity.objects.create(name=name)

                # Create a SubActivityName entry for each SubActivity
                sub_activity_name = SubActivityName.objects.create(
                    project_main_activity=project_activity
                )
                sub_activity_name.sub_activity.add(sub_activity)
                # created_ids.append(sub_activity_name.id)

            return Response({"status": True, "message": "SubActivityName created successfully."})

        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def list(self, request, *args, **kwargs):
        try:
            project_activity_id = request.data.get("project_activity_id")

            # Filter based on project_activity_id if provided
            if project_activity_id:
                queryset = self.get_queryset().filter(project_main_activity_id=project_activity_id)
            else:
                queryset = self.get_queryset()

            if queryset.exists():
                serialized_subactivitydata = []
                for obj in queryset:
                    context = {'request' : request}
                    serializer = SubActivityNameSerializer(obj,context=context)
                    serialized_subactivitydata.append(serializer.data)

                return Response({
                    "status": True,
                    "message": "SubActivityName data fetched successfully.",
                    "total": len(serialized_subactivitydata),
                    "data": serialized_subactivitydata,
                })
            else:
                return Response({
                    "status": True,
                    "message": "No SubActivityName found.",
                    "total": 0,
                    "data": [],
                })

        except Exception as e:
            return Response({"status": False, "message": str(e)})

class SubActivityUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubActivityName.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            sub_activity_id = self.kwargs.get('sub_activity_id')  # ID of the SubActivity to be updated
            sub_activity_names = request.data.get("sub_activity_names")

            if not sub_activity_names:
                return Response({"status": False, "message": "sub_activity_names must be a non-empty list."})

            try:
                # Fetch the specific SubActivityName object
                sub_activity_name_obj = SubActivityName.objects.get(id=sub_activity_id)
            except SubActivityName.DoesNotExist:
                return Response({"status": False, "message": "Invalid SubActivityName ID."})

            # Fetch all associated SubActivity objects
            sub_activities = sub_activity_name_obj.sub_activity.all()

            if not sub_activities.exists():
                return Response({"status": False, "message": "No associated SubActivities found for this SubActivityName ID."})

            # Update the names of the associated SubActivities
            for sub_activity, new_name in zip(sub_activities, sub_activity_names):
                sub_activity.name = new_name
                sub_activity.save()

            return Response({
                "status": True,
                "message": "SubActivity updated successfully.",
               })

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
    
    def destroy(self, request, *args, **kwargs):
        try:
            sub_activity_id = self.kwargs.get('sub_activity_id')

            if not sub_activity_id:
                return Response({"status": False, "message": "SubActivity ID is required"})

            sub_activity_name_obj = SubActivityName.objects.get(id=sub_activity_id)

            if not sub_activity_name_obj:
                return Response({"status": False, "message": "SubActivityName not found"})

            sub_activity_name_obj.delete()

            return Response({"status": True, "message": "SubActivityName deleted successfully"})

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
class GetActiveSubActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubActivityNameSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = SubActivityName.objects.filter(is_active=True)
            if queryset.exists():
                serialized_subactivitydata = []
                for obj in queryset:
                    context = {'request' : request}
                    serializer = SubActivityNameSerializer(obj,context=context)
                    serialized_subactivitydata.append(serializer.data)
                    return Response({
                        "status": True,
                        "message": "Active SubActivityName data fetched successfully.",
                        "total": len(serialized_subactivitydata),
                        "data": serialized_subactivitydata,
                    })
        except Exception as e:
            return Response({"status": False, "message": str(e)})
        


class ActiveDeactiveSubActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubActivityNameSerializer

    def update(self, request, *args, **kwargs):
        try:
            sub_activity_id = self.kwargs.get('sub_activity_id')
            if not sub_activity_id:
                return Response({"status": False, "message": "SubActivity not found."})
            
            sub_activity_data = SubActivityName.objects.get(id=sub_activity_id)
            if not sub_activity_data:
                return Response({"status": False, "message": "SubActivity not found."})
            
            sub_sub_activity_data = SubSubActivityName.objects.filter(sub_activity_id=sub_activity_data)
            if not sub_sub_activity_data.exists():
                return Response({"status": False, "message": "Sub Sub Activity not found."})
            
            if sub_activity_data.is_active:
                sub_activity_data.is_active = False
                sub_activity_data.save()
                
                for sub_sub_activity in sub_sub_activity_data:
                    sub_sub_activity.is_active = False
                    sub_sub_activity.save()
                    
                return Response({"status": True, "message": "Sub Activity and Sub Sub Activity deactivated successfully."})
            
            elif not sub_activity_data.is_active:
                sub_activity_data.is_active = True
                sub_activity_data.save()
                return Response({"status": True, "message": "Sub Activity reactivated successfully."})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})


class SubSubActivityNameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubSubActivityName.objects.all()
    serializer_class = SubSubActivityNameSerializer

    def create(self, request, *args, **kwargs):
        try:
            sub_activity_id = request.data.get("sub_activity_id")
            sub_sub_activity_names = request.data.get("sub_sub_activity_names", [])

            if not sub_activity_id:
                return Response({"status": False, "message": "sub_activity_id is required."})

            try:
                sub_activity = SubActivityName.objects.get(id=sub_activity_id)
            except SubActivityName.DoesNotExist:
                return Response({"status": False, "message": "Invalid sub_activity_id."})

            if not sub_sub_activity_names:
                return Response({"status": False, "message": "sub_sub_activity_names must be a non-empty list."})

            for name in sub_sub_activity_names:
                # Create SubsubActivity instances
                sub_sub_activity = SubsubActivity.objects.create(name=name)

                # Create SubSubActivityName entry and associate with sub_activity
                sub_sub_activity_name = SubSubActivityName.objects.create(sub_activity_id=sub_activity)
                sub_sub_activity_name.sub_sub_activity.add(sub_sub_activity)

            return Response({"status": True, "message": "SubSubActivityName created successfully."})

        except Exception as e:
            return Response({"status": False, "message": str(e)})

    def list(self, request, *args, **kwargs):
        try:
            sub_activity_id = request.query_params.get("sub_activity_id")

            # Filter based on sub_activity_id if provided
            if sub_activity_id:
                queryset = self.get_queryset().filter(sub_activity_id=sub_activity_id)
            else:
                queryset = self.get_queryset()

            if queryset.exists():
                serialized_data = []
                for obj in queryset:
                    serializer = SubSubActivityNameSerializer(obj, context={'request': request})
                    serialized_data.append(serializer.data)

                return Response({
                    "status": True,
                    "message": "SubSubActivityName data fetched successfully.",
                    "total": len(serialized_data),
                    "data": serialized_data,
                })
            else:
                return Response({
                    "status": True,
                    "message": "No SubSubActivityName found.",
                    "total": 0,
                    "data": [],
                })

        except Exception as e:
            return Response({"status": False, "message": str(e)})


class SubSubActivityUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SubSubActivityName.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            sub_sub_activity_name_id = self.kwargs.get('sub_sub_activity_id')
            sub_sub_activity_names = request.data.get("sub_sub_activity_names")

            if not sub_sub_activity_names:
                return Response({"status": False, "message": "sub_sub_activity_names must be a non-empty list."})

            try:
                # Fetch the specific SubSubActivityName object
                sub_sub_activity_name_obj = SubSubActivityName.objects.get(id=sub_sub_activity_name_id)
            except SubSubActivityName.DoesNotExist:
                return Response({"status": False, "message": "Invalid SubSubActivityName ID."})

            # Fetch all associated SubsubActivity objects
            sub_sub_activities = sub_sub_activity_name_obj.sub_sub_activity.all()

            if not sub_sub_activities.exists():
                return Response({"status": False, "message": "No associated SubSubActivities found for this SubSubActivityName ID."})

            # # Ensure the lengths of the current SubsubActivities and new names match
            # if len(sub_sub_activities) != len(sub_sub_activity_names):
            #     return Response({
            #         "status": False,
            #         "message": "Mismatch between the number of existing SubSubActivities and provided names."
            #     })

            # Update the names of the associated SubSubActivities
            for sub_sub_activity, new_name in zip(sub_sub_activities, sub_sub_activity_names):
                sub_sub_activity.name = new_name
                sub_sub_activity.save()

            return Response({
                "status": True,
                "message": "SubSubActivity updated successfully.",
            })

        except Exception as e:
            return Response({"status": False, "message": str(e)})
        
        
class ActiveDeactiveSubSubActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubSubActivityNameSerializer

    def update(self, request, *args, **kwargs):
        try:
            sub_sub_activity_id = self.kwargs.get('sub_sub_activity_id')
            if not sub_sub_activity_id:
                return Response({"status": False, "message": "SubSubActivity not found."})
            
            sub_sub_activity_data = SubSubActivityName.objects.get(id=sub_sub_activity_id)
            if not sub_sub_activity_data:
                return Response({"status": False, "message": "SubSubActivity not found."})
            
            if sub_sub_activity_data.is_active:
                sub_sub_activity_data.is_active = False
                sub_sub_activity_data.save()
                return Response({"status": True, "message": "SubSubActivity deactivated successfully."})
            elif not sub_sub_activity_data.is_active:
                sub_sub_activity_data.is_active = True
                sub_sub_activity_data.save()
                return Response({"status": True, "message": "SubSubActivity reactivated successfully."})
        except Exception as e:
            return Response({"status": False, "message": str(e)})
    

class GetActiveSubSubActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubSubActivityNameSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = SubSubActivityName.objects.filter(is_active=True)
            if queryset.exists():
                serialized_data = []
                for obj in queryset:
                    serializer = SubSubActivityNameSerializer(obj, context={'request': request})
                    serialized_data.append(serializer.data)
                return Response({
                    "status": True,
                    "message": "Active SubSubActivity data fetched successfully.",
                    "total": len(serialized_data),
                    "data": serialized_data,
                })
        except Exception as e:
            return Response({"status": False, "message": str(e)})