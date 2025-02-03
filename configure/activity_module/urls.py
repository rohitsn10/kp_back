from django.urls import path
from activity_module.views import *

urlpatterns = [

    path('create_activity', ProjectActivityViewSet.as_view({'post': 'create'}), name='create_activity'),
    path('get_activity', ProjectActivityViewSet.as_view({'get': 'list'}), name='get_activity'),
    path('update_activity/<int:activity_id>', ProjectActivityUpdateViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_activity'),
    
    path('active_deactivate_activity_project/<int:activity_id>', ActiveDeactiveActivityProjectViewSet.as_view({'put': 'update'}), name='activity_project_active_deactivate'),
    path('get_active_activity', GetActiveActivityViewSet.as_view({'get': 'list'}), name='get_active_activity'),

    path('create_sub_activity', SubActivityNameViewSet.as_view({'post': 'create'}), name='create_sub_activity'),
    path('get_sub_activity', SubActivityNameViewSet.as_view({'get': 'list'}), name='get_sub_activity'),
    path('update_sub_activity/<int:sub_activity_id>', SubActivityUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_sub_activity'),

    path('dropdown_get_sub_activity/<int:project_activity_id>', DropDownSubActivityNameViewSet.as_view({'get': 'list'}), name='dropdown_get_sub_activity'),

    path('get_active_sub_activity', GetActiveSubActivityViewSet.as_view({'get': 'list'}), name='get_active_sub_activity'),
    path('active_deactivate_sub_activity/<int:sub_activity_id>', ActiveDeactiveSubActivityViewSet.as_view({'put':'update'}), name='active_deactivate_sub_activity'),


    path('create_sub_sub_activity', SubSubActivityNameViewSet.as_view({'post': 'create'}), name='create_sub_sub_activity'),
    path('get_sub_sub_activity', SubSubActivityNameViewSet.as_view({'get': 'list'}), name='get_sub_sub_activity'),
    path('update_sub_sub_activity/<int:sub_sub_activity_id>', SubSubActivityUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_sub_sub_activity'),

    path('get_active_sub_sub_activity', GetActiveSubSubActivityViewSet.as_view({'get': 'list'}), name='get_active_sub_sub_activity'),
    path('active_deactivate_sub_sub_activity/<int:sub_sub_activity_id>', ActiveDeactiveSubSubActivityViewSet.as_view({'put':'update'}), name='active_deactivate_sub_sub_activity'),

]