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
    path('admin_can_update_user/<int:user_id>', AdminCanUpdateUser.as_view({'put':'update','get':'list'}), name='admin_can_update_user'),
    path('user_update_own_profile_data', UserUpdateOwnProfileDataViewset.as_view({'put':'update','get':'list'}), name='user_update_own_profile_data'),
    path('user_activate_or_deactivate/<int:user_id>', UserDeactivateViewSet.as_view({'put':'update'}), name='user_deactivate'),
    path('admin_can_reset_passowrd/<int:user_id>', AdminResetLoginCountAPIView.as_view({'put':'update'}), name='admin_reset_login_count'),
    path('reset_password', ResetPasswordAPIView.as_view({'put':'update'}), name='reset_password'),
    path('otp_resetpassword', ConfirmOTPAndSetPassword.as_view({'put':'update'}), name='otp_resetpassword'),
    path('privacy_policy/<privacypolicy_key>', PrivacyPolicyViewSet.as_view({'post':'create', 'get':'list'}), name='privacy_policy'),
    path('logout', LogoutViewSet.as_view({'post':'create'}), name='logout'),

    path('create_get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='create_get_department'),
    path('get_department', DepartmentAddView.as_view({'post': 'create', 'get': 'list'}), name='get_department'),
    path('update_delete_department/<int:department_id>', DepartmentUpdatesViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_delete_department'),

    path('assign_user_all_things', AssignUserAllThingsViewSet.as_view({'post': 'create', 'get': 'list'}), name='assign_user_all_things'),

    # ========== NEW ROLE & PERMISSION MANAGEMENT APIs ==========
    
    # Role Management
    path('roles', RoleManagementViewSet.as_view({'get': 'list', 'post': 'create'}), name='role-list-create'),
    path('roles/<int:pk>', RoleManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='role-detail'),
    
    # Module Management
    path('modules', ModuleManagementViewSet.as_view({'get': 'list', 'post': 'create'}), name='module-list-create'),
    path('modules/<int:pk>', ModuleManagementViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='module-detail'),

    # Role Permissions (Read-only)
    path('role-permissions', RolePermissionViewSet.as_view({'get': 'list'}), name='role-permissions-list'),
    path('role-permissions/<int:pk>', RolePermissionViewSet.as_view({'get': 'retrieve'}), name='role-permissions-detail'),

    # Get permissions by module for a specific role
    path('role-permissions-by-module', RolePermissionsByModuleView.as_view(), name='role-permissions-by-module'),

    # User Role Assignments
    path('user-roles', UserRoleAssignmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-roles-list-create'),
    path('user-roles/<int:pk>', UserRoleAssignmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-roles-detail'),

    # Get all roles for a department
    path('department-roles', DepartmentRolesView.as_view(), name='department-roles'),

]