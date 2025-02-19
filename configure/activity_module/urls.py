from django.urls import path
from activity_module.views import *

urlpatterns = [

    path('create_activity', ProjectActivityViewSet.as_view({'post': 'create'}), name='create_activity'),
    path('get_activity', ProjectActivityViewSet.as_view({'get': 'list'}), name='get_activity'),
    path('update_activity/<int:activity_id>', ProjectActivityUpdateViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_activity'),
    
    path('main_project_wise_main_activity/<int:main_project_id>', MainProjectWiseProjectActivity.as_view({'get': 'list'}), name='main_project_wise_main_activity'),

    path('active_deactivate_activity_project/<int:activity_id>', ActiveDeactiveActivityProjectViewSet.as_view({'put': 'update'}), name='activity_project_active_deactivate'),
    path('get_active_activity', GetActiveActivityViewSet.as_view({'get': 'list'}), name='get_active_activity'),

    path('create_sub_activity', SubActivityNameViewSet.as_view({'post': 'create'}), name='create_sub_activity'),
    path('get_sub_activity', SubActivityNameViewSet.as_view({'get': 'list'}), name='get_sub_activity'),
    path('update_sub_activity/<int:sub_activity_id>', SubActivityUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_sub_activity'),

    path('dropdown_get_sub_activity/<int:project_activity_id>', DropDownSubActivityNameViewSet.as_view({'get': 'list'}), name='dropdown_get_sub_activity'),
    path('main_project_wise_sub_activity/<int:main_project_id>', MainProjectWiseSubActivity.as_view({'get': 'list'}), name='main_project_wise_sub_activity'),

    path('multiplte_id_wise_listing_sub_activitys', MultipleIDWiseSubActivityViewSet.as_view({'post': 'create'}), name='multiplte_id_wise_listing_sub_activitys'),
    path('get_active_sub_activity', GetActiveSubActivityViewSet.as_view({'get': 'list'}), name='get_active_sub_activity'),
    path('active_deactivate_sub_activity/<int:sub_activity_id>', ActiveDeactiveSubActivityViewSet.as_view({'put':'update'}), name='active_deactivate_sub_activity'),

    path('create_sub_sub_activity', SubSubActivityNameViewSet.as_view({'post': 'create'}), name='create_sub_sub_activity'),
    path('get_sub_sub_activity', SubSubActivityNameViewSet.as_view({'get': 'list'}), name='get_sub_sub_activity'),

    path('multiplte_id_wise_listing_sub_sub_activitys', MultipleIDWiseSubSubActivityViewSet.as_view({'post': 'create'}), name='listing_get_sub_activity'),
    path('main_project_wise_sub_sub_activity/<int:main_project_id>', MainProjectWiseSubSubActivity.as_view({'get': 'list'}), name='main_project_wise_sub_sub_activity'),
    path('update_sub_sub_activity/<int:sub_sub_activity_id>', SubSubActivityUpdateViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='update_sub_sub_activity'),

    path('get_active_sub_sub_activity', GetActiveSubSubActivityViewSet.as_view({'get': 'list'}), name='get_active_sub_sub_activity'),
    path('active_deactivate_sub_sub_activity/<int:sub_sub_activity_id>', ActiveDeactiveSubSubActivityViewSet.as_view({'put':'update'}), name='active_deactivate_sub_sub_activity'),

]