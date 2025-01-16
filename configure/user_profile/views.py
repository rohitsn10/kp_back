from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from user_profile.models import *
from user_profile.serializers import * 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, Permission
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import filters
from rest_framework import viewsets
import ipdb 
from user_profile.function_call import *
from django.conf import settings
import jwt 
from django.contrib.auth.hashers import make_password
import random





class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    lookup_url_kwarg = 'pk'

class GroupIdWisePermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_id = request.query_params.get('group_id')
        user = request.user

        group_permissions_ids = []
        group_name = None
        if group_id is not None:
            try:
                group = Group.objects.get(id=group_id)
                group_name = group.name
                group_permissions_ids = group.permissions.values_list('id', flat=True)
            except Group.DoesNotExist:
                return Response({'status': False, 'message': 'Group not found!'})

        # Get all available permissions for the model
        all_permissions = Permission.objects.filter(group=group_id)
        permission_dict = {}

        for permission in all_permissions:
            model_name = permission.content_type.model
            if model_name not in permission_dict:
                permission_dict[model_name] = {
                    'name': model_name,
                    'isAdd': False,
                    'add': None,
                    'isChange': False,
                    'change': None,
                    'isDelete': False,
                    'delete': None,
                    'isView': False,
                    'view': None,
                }

            # Check which permission is available and update the dictionary
            # Additionally, check if the permission is in the specified group
            if permission.codename == f'add_{model_name}':
                permission_dict[model_name]['isAdd'] = permission.id in group_permissions_ids
                permission_dict[model_name]['add'] = permission.id
            elif permission.codename == f'change_{model_name}':
                permission_dict[model_name]['isChange'] = permission.id in group_permissions_ids
                permission_dict[model_name]['change'] = permission.id
            elif permission.codename == f'delete_{model_name}':
                permission_dict[model_name]['isDelete'] = permission.id in group_permissions_ids
                permission_dict[model_name]['delete'] = permission.id
            elif permission.codename == f'view_{model_name}':
                permission_dict[model_name]['isView'] = permission.id in group_permissions_ids
                permission_dict[model_name]['view'] = permission.id

        # Convert dictionary to a list
        permission_data = list(permission_dict.values())

        return Response({
            'status': True,
            'message': 'Permission List!',
            'group_id': group_id,
            'group_name': group_name,
            'data': permission_data
        })



class PermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # if not request.user.has_perm('auth.view_permission'):
            #     return Response({'status': False, 'message': "You don't have permission to perform this action"})

            user = request.user

            group_permissions_ids = []

            # Get all available permissions for the model
            all_permissions = Permission.objects.all()
            permission_dict = {}

            for permission in all_permissions:
                model_name = permission.content_type.model
                if model_name not in permission_dict:
                    permission_dict[model_name] = {
                        'name': model_name,
                        'isAdd': False,
                        'add': None,
                        'isChange': False,
                        'change': None,
                        'isDelete': False,
                        'delete': None,
                        'isView': False,
                        'view': None,
                    }

                # Check which permission is available and update the dictionary
                # Additionally, check if the permission is in the specified group
                if permission.codename == f'add_{model_name}':
                    permission_dict[model_name]['isAdd'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['add'] = permission.id
                elif permission.codename == f'change_{model_name}':
                    permission_dict[model_name]['isChange'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['change'] = permission.id
                elif permission.codename == f'delete_{model_name}':
                    permission_dict[model_name]['isDelete'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['delete'] = permission.id
                elif permission.codename == f'view_{model_name}':
                    permission_dict[model_name]['isView'] = permission.id in group_permissions_ids
                    permission_dict[model_name]['view'] = permission.id

            # Convert dictionary to a list
            permission_data = list(permission_dict.values())

            return Response({
                'status': True,
                'message': 'Permission List!',
                'data': permission_data
            })
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})



class CreateGroupWithPermissionViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            permissions = request.data.get('permissions',[])

            if not name:
                return Response({"status": False,'message': 'Group name is required','data':[]})
            if not permissions:
                return Response({"status": False,'message': 'Permissions is required','data':[]})
            
            group = Group.objects.create(name = name)
            for permission in permissions:
                group.permissions.add(permission)
            group.save()
            serializer = GroupSerializer(group)
            data = serializer.data
            return Response({"status": True, "message": "Group created successfully!", "data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = GroupSerializer(page, many=True)
                    serializer = self.get_paginated_response(serializer.data)
                else:
                    serializer = GroupSerializer(queryset, many=True)
                count = serializer.data['count']
                limit = int(request.GET.get('page_size', 10))
                return Response({"status": True, "message":"Group List Successfully", 
                                'total_page': (count + limit - 1) // limit,
                                'count':count,
                                'data': serializer.data['results']})
            else:
                return Response({"status": False,"message":"No data found!","data":[]})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})

class UpdateGroupWithPermissionViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def update(self, request, *args, **kwargs):
        try:
            group_id = kwargs.get('group_id')
            name = request.data.get('name')
            permissions = request.data.get('permissions',[])

            if not group_id:
                return Response({"status": False,'message': 'Group id is required','data':[]})
            if not name:
                return Response({"status": False,'message': 'Group name is required','data':[]})
            if not permissions:
                return Response({"status": False,'message': 'Permissions is required','data':[]})
            
            group = Group.objects.filter(id = group_id).first()   # get group by id
            if not group:
                return Response({"status": False,"message": "Group not found!","data":[]})
            group.name = name   # update group name
            group.permissions.clear()  # remove all permissions from group
            for permission in permissions:
                group.permissions.add(permission)  # add new permissions to group
            group.save()
            serializer = GroupSerializer(group)
            data = serializer.data
            return Response({"status": True, "message": "Group updated successfully!", "data": data})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        

    def destroy(self, request, *args, **kwargs):
        # if group is assign to any user then it will not delete other wise it will delete
        try:
            group_id = kwargs.get('group_id')
            group = Group.objects.filter(id = group_id).first()
            if not group:
                return Response({"status": False,"message": "Group not found!","data":[]})
            if group.user_set.exists():  # check if group is assign to any user
                return Response({"status": False,"message": "This Group is assign to user, so it can not be deleted!","data":[]})
            group.delete()
            return Response({"status": True, "message": "Group deleted successfully!", "data": []})
        except Exception as e:
            return Response({"status": False,"message": str(e),"data":[]})
        
        

class LoginAPIView(ViewSet):
    def create(self, request):
        try:
            email = request.data.get('email', '').strip()
            password = request.data.get('password', '').strip()
            login_type = request.data.get('login_type', '').strip() 
            device_id = request.data.get('device_id', '').strip()
            device_type = request.data.get('device_type', '').strip()
            device_token = request.data.get('device_token', '').strip()


            # Validate email and password inputs
            if not email:
                return Response({"status": False, 'message': 'Email is required', "data": []})
            if not password:
                return Response({"status": False, 'message': 'Password is required', "data": []})
            if not login_type or login_type not in ['mobile', 'desktop']:
                return Response({"status": False, 'message': 'Invalid type parameter!', "data": []})
            
            # if login_type == 'mobile':
            #     if not device_id:
            #         return Response({"status": False, 'message': 'Device ID is required for mobile login', "data": []})
            #     if not device_type:
            #         return Response({"status": False, 'message': 'Device Type is required for mobile login', "data": []})
            #     if not device_token:
            #         return Response({"status": False, 'message': 'Device Token is required for mobile login', "data": []})


            # Check if user exists
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({"status": False, "message": "Invalid email or password!", "data": []})

           # Authenticate user
            user_auth = authenticate_user_by_email(email, password)
            if not user_auth:
                return Response({"status": False, "message": "Invalid email or password!", "data": []})
            
            if login_type == 'mobile':
                user.device_id = device_id
                user.device_type = device_type
                user.device_token = device_token
                user.save()

            # Successful login - generate JWT token
            refresh = RefreshToken.for_user(user_auth)
            access_token = str(refresh.access_token)
            
            serializer = LoginUserSerializer(user_auth, context={'request': request})
            data = serializer.data
            data['token'] = access_token
            
             # If type is mobile, encode all data into a JWT token
            if login_type == 'mobile':
                encoded_data = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
                print(encoded_data,"============================")
                return Response({"status": True, "message": "You are logged in!", "token": encoded_data})

            return Response({"status": True, "message": "You are logged in!", "data": data})
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response({"status": False, 'message': "Something went wrong!", 'data': []})

class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().exclude(is_superuser=True)
    serializer_class = CustomUserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            email = request.data.get('email','')
            full_name = request.data.get('full_name','')
            phone = request.data.get('phone','')
            address = request.data.get('address','')
            password = request.data.get('password')
            group_ids = request.data.get('user_role',[])  # List of group IDs
            
            # Validate required fields
            if not email:
                return Response({"status": False, "message": "Email is required", "data": []})
            if not full_name:
                return Response({"status": False, "message": "Username is required", "data": []})
            if not phone:
                return Response({"status": False, "message": "Phone is required", "data": []})
            if not password:
                return Response({"status": False, "message": "Password is required", "data": []})
            if not group_ids or not isinstance(group_ids, list):
                return Response({"status": False, "message": "User roles must be a list of group IDs", "data": []})
            
            # Check for duplicate email or username
            if CustomUser.objects.filter(email=email).exists():
                return Response({"status": False, "message": "Email already exists", "data": []})
            # if CustomUser.objects.filter(username=username).exists():
            #     return Response({"status": False, "message": "Username already exists", "data": []})
            
            # Validate groups
            groups = []
            for group_id in group_ids:
                try:
                    group = Group.objects.get(id=group_id)
                    groups.append(group)
                except Group.DoesNotExist:
                    return Response({"status": False, "message": f"Invalid group ID: {group_id}", "data": []})
            
            # Create user
            user = CustomUser.objects.create(
                email=email,
                full_name=full_name,
                phone=phone,
                address=address
            )
            user.set_password(password)
            user.save()

            # Assign user to groups
            for group in groups:
                user.groups.add(group)
            user.save()
            return Response({"status": True, "message": "User created successfully!"})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset()).order_by('-id')
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "User List Successfully", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        


class SplashScreenViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        try:
            token = request.headers.get('token', '').strip()
            if not token:
                return Response({"status": False, "message": "Login required!", "data": []})
            try:
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return Response({"status": False, "message": "Token has expired!", "data": []})
            except jwt.InvalidTokenError:
                return Response({"status": False, "message": "Invalid token!", "data": []})

            # Extract user_id from the token payload
            user_id = decoded_data.get("id")
            if not user_id:
                return Response({"status": False, "message": "Invalid token payload!", "data": []})

            # Validate user exists in the database
            user = CustomUser.objects.filter(id=user_id).first()
            if not user:
                return Response({"status": False, "message": "User does not exist!", "data": []})

            return Response({"status": True, "message": "Token validated successfully!", "data": {"token": token}})

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Splash screen error: {str(e)}", exc_info=True)
            return Response({"status": False, "message": "Something went wrong!", "data": []})



class UserUpdateOwnProfileDataViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateOwnProfileDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            full_name = request.data.get('full_name', '')
            phone = request.data.get('phone', '')
            address = request.data.get('address', '')
            dob = request.data.get('dob', '')
            profile_image = request.data.get('profile_image', '')

            if not full_name:
                return Response({"status": False, "message": "First name is required", "data": []})
            if not phone:
                return Response({"status": False, "message": "Phone number is required", "data": []})

            user_data = CustomUser.objects.get(id=user.id)
            if full_name is not None:
                user_data.full_name = full_name
            if phone is not None:
                user_data.phone = phone
            if dob is not None:
                user_data.dob = dob
            if address:
                user_data.address = address
            if profile_image is not None and not isinstance(profile_image, str):
                user_data.profile_image = profile_image

            user_data.save()
            serializer = self.serializer_class(user, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Profile updated successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})
        

    def list(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = self.serializer_class(user, context={'request': request})
            data = serializer.data
            return Response({"status": True, "message": "Profile data fetched successfully!", "data": data})
        except Exception as e:
            return Response({"status": False, "message": str(e), "data": []})

        
class LoginAPIView(ViewSet):
    def create(self, request):
        try:
            email = request.data.get('email', '').strip()
            password = request.data.get('password', '').strip()
            login_type = request.data.get('login_type', '').strip() 
            device_id = request.data.get('device_id', '').strip()
            device_type = request.data.get('device_type', '').strip()
            device_token = request.data.get('device_token', '').strip()


            # Validate email and password inputs
            if not email:
                return Response({"status": False, 'message': 'Email is required', "data": []})
            if not password:
                return Response({"status": False, 'message': 'Password is required', "data": []})
            if not login_type or login_type not in ['mobile', 'desktop']:
                return Response({"status": False, 'message': 'Invalid type parameter!', "data": []})

            # if login_type == 'mobile':
            #     if not device_id:
            #         return Response({"status": False, 'message': 'Device ID is required for mobile login', "data": []})
            #     if not device_type:
            #         return Response({"status": False, 'message': 'Device Type is required for mobile login', "data": []})
            #     if not device_token:
            #         return Response({"status": False, 'message': 'Device Token is required for mobile login', "data": []})
            if login_type == 'mobile':
                if not device_id:
                    return Response({"status": False, 'message': 'Device ID is required for mobile login', "data": []})
                if not device_type:
                    return Response({"status": False, 'message': 'Device Type is required for mobile login', "data": []})
                if not device_token:
                    return Response({"status": False, 'message': 'Device Token is required for mobile login', "data": []})


            # Check if user exists
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({"status": False, "message": "Invalid email or password!", "data": []})

           # Authenticate user
            user = authenticate_user_by_email(email, password)
            if not user:
                return Response({"status": False, "message": "Invalid email or password!", "data": []})
            auth_user = authenticate_user_by_email(email, password)
            if not auth_user:
                return Response({"status": False, "message": "Invalid email or password!"})

            if login_type == 'mobile':
                user.device_id = device_id
                user.device_type = device_type
                user.device_token = device_token
                user.save()

            # Successful login - generate JWT token
            refresh = RefreshToken.for_user(user)
            serializer = LoginUserSerializer(user, context={'request': request})
            refresh = RefreshToken.for_user(auth_user)
            serializer = LoginUserSerializer(auth_user, context={'request': request})
            data = serializer.data
            data['token'] = str(refresh.access_token)

             # If type is mobile, encode all data into a JWT token
            if login_type == 'mobile':
                encoded_data = jwt.encode(data, settings.SECRET_KEY, algorithm='HS256')
                return Response({"status": True, "message": "You are logged in!", "data": encoded_data})

            return Response({"status": True, "message": "You are logged in!", "data": data})

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response({"status": False, 'message': "Something went wrong!", 'data': []})
        

class UserDeactivateViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def update(self, request, *args, **kwargs):
        # Get the list of user IDs to be updated from the request
        user_ids = request.data.get('user_ids', [])

        if not user_ids:
            return Response({
                    "status": False,
                    "message": "No user IDs provided."
                })

        users = CustomUser.objects.filter(id__in=user_ids)

        if not users.exists():
            return Response({
                    "status": False,
                    "message": "No matching users found."
                })

        users.update(is_active=False)

        return Response({
                "status": True,
                "message": "user have been deactivated."
            })


class ResetPasswordAPIView(viewsets.ModelViewSet):
    def update(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response({"status": False, "message": "User is not authenticated", "data": []})

        old_password = request.data.get('old_password')

        if not check_password(old_password, user.password):
            return Response({"status": False, "message": "Old password is incorrect", "data": []})

        try:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            return Response({"status": True,"message": "Otp genrate successfully", "data": []})
        except CustomUser.DoesNotExist:
            return Response({"status": False,"message": "User not found", "data": []})

class ConfirmOTPAndSetPassword(viewsets.ModelViewSet):
    def update(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response({"status": False, "message": "User is not authenticated", "data": []})

        otp_data = request.data.get('otp')
        new_password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not otp_data or not new_password or not confirm_password:
            return Response({"status": False, "message": "OTP, new password, and confirm password are required", "data": []})

        if otp_data != user.otp:
            return Response({"status": False, "message": "Invalid OTP", "data": []})

        if new_password != confirm_password:
            return Response({"status": False, "message": "Password and confirm password do not match", "data": []})

        if check_password(new_password, user.old_password):
            return Response({"status": False, "message": "New password cannot be the same as the old password", "data": []})

        user.old_password = new_password
        user.password = make_password(new_password)
        user.otp = None
        user.save()

        return Response({"status": True, "message": "Password reset successfully", "data": []})




