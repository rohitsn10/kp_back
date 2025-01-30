
from django.urls import path
from project_module.views import *

urlpatterns = [
    path('create_expense_data', ProjectExpenseCreateViewset.as_view({'post':'create','get':'list'}), name='create_expense_data'),
    path('update_expense_data/<int:expense_id>', ProjectExpenseUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_expense_data'),

    path('create_client_data', ClientDataCreateViewset.as_view({'post':'create','get':'list'}), name='create_client_data'),
    path('update_client_data/<int:client_id>', ProjectClientUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_client_data'),

    path('create_wo_po_data', Wo_Po_DataCreateViewset.as_view({'post':'create','get':'list'}), name='create_wo_po_data'),
    path('update_wo_po_data/<int:wo_po_id>', Wo_Po_DataUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_wo_po_data'),

    path('company', CompanyViewSet.as_view({'post':'create','get':'list'}), name='company'),
    path('company/<int:id>', CompanyViewSet.as_view({'put':'update','delete':'destroy'}), name='company'),
    
    # path('create_main_project', ProjectViewSet.as_view({'post':'create','get':'list'}), name='create_main_project'),
    path('update_main_project/<int:project_id>', ProjectUpdateViewSet.as_view({'put':'update'}), name='update_main_project'),

    path('project_active_deactivate/<int:project_id>', ActiveDeactiveProjectViewSet.as_view({'put':'update'}), name='project_active_deactivate'),

    path('getactiveproject',GetActiveProjectViewSet.as_view({'get':'list'}), name='getactiveproject'),

    path('create_milestone', ProjectMilestoneViewSet.as_view({'post': 'create'}), name='create_milestone'),
    path('get_milestone', ProjectMilestoneViewSet.as_view({'get': 'list'}), name='get_milestone'),
    path('update_milestone/<int:milestone_id>', ProjectMilestoneUpdateViewSet.as_view({'put': 'update'}), name='update_milestone'),

    path('milestone_active_deactivate/<int:milestone_id>', ActiveDeactiveMilestoneViewSet.as_view({'put':'update'}), name='milestone_active_deactivate'),
    
    path('getactivemilestone',GetActiveMilestoneViewSet.as_view({'get':'list'}), name='getactivemilestone'),

]