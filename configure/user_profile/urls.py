from django.urls import path
from user_profile.views import *

urlpatterns = [
    
    path('group_id_wise_permission_list', GroupIdWisePermissionListAPIView.as_view(), name='group_id_wise_permission_list'),
    path('permission_list', PermissionListAPIView.as_view(), name='permission_list'),
    path('group_create_with_permissions', CreateGroupWithPermissionViewSet.as_view({'post':'create','get':'list'}), name='group_create_with_permissions'),
    path('group_update_with_permissions/<int:group_id>', UpdateGroupWithPermissionViewSet.as_view({'put':'update','get':'list'}), name='group_update_with_permissions'),
    path('group_delete/<int:group_id>', UpdateGroupWithPermissionViewSet.as_view({'delete':'destroy'}), name='group_delete'),

    path('login', LoginAPIView.as_view({'post':'create'}), name='login'),
    path('splash_screen', SplashScreenViewSet.as_view({'post':'create'}), name='splash_screen'),
    path('user_create', CreateUserViewSet.as_view({'post':'create','get':'list'}), name='user_create'),
    path('user_update_own_profile_data', UserUpdateOwnProfileDataViewset.as_view({'put':'update','get':'list'}), name='user_update_own_profile_data'),
    path('user_deactivate', UserDeactivateViewSet.as_view({'put':'update'}), name='user_deactivate'),
    path('reset_password', ResetPasswordAPIView.as_view({'put':'update'}), name='reset_password'),
    path('otp_resetpassword', ConfirmOTPAndSetPassword.as_view({'put':'update'}), name='otp_resetpassword'),
    path('privacy_policy', PrivacyPolicyViewSet.as_view({'post':'create', 'get':'list'}), name='privacy_policy'),

    path('create_get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_department'),
    path('get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='get_department'),
    path('update_delete_department/<int:department_id>', DepartmentUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_department'),
    
]