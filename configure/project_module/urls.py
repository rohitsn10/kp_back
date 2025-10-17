
from django.urls import path
from project_module.views import *

urlpatterns = [
    path('create_expense_data', ProjectExpenseCreateViewset.as_view({'post':'create','get':'list'}), name='create_expense_data'),
    path('update_expense_data/<int:expense_id>', ProjectExpenseUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_expense_data'),
    path('project_id_wise_get_expense_data/<int:project_id>',ProjectIdWIseGetExpenseDataViewSet.as_view({'get':'list'}), name='project_id_wise_get_expense_data'),

    path('create_client_data', ClientDataCreateViewset.as_view({'post':'create','get':'list'}), name='create_client_data'),
    path('update_client_data/<int:client_id>', ProjectClientUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_client_data'),
    path('project_id_wise_get_client_data/<int:project_id>',ProjectIdWIseGetClientDataViewSet.as_view({'get':'list'}), name='project_id_wise_get_client_data'),
    
    path('create_wo_po_data', Wo_Po_DataCreateViewset.as_view({'post':'create','get':'list'}), name='create_wo_po_data'),
    path('update_wo_po_data/<int:wo_po_id>', Wo_Po_DataUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_wo_po_data'),

    path('company', CompanyViewSet.as_view({'post':'create','get':'list'}), name='company'),
    path('company/<int:id>', CompanyViewSet.as_view({'put':'update','delete':'destroy'}), name='company'),

    path('electricity',ElectricityViewSet.as_view({'post':'create','get':'list'}), name='electricity'),
    path('update_electricity/<int:id>',UpdateElectricityViewSet.as_view({'put':'update', 'delete': 'destroy'}), name='update_electricity'),
    
    path('create_main_project', ProjectViewSet.as_view({'post':'create','get':'list'}), name='create_main_project'),
    path('update_main_project/<int:project_id>', ProjectUpdateViewSet.as_view({'put':'update', 'delete': 'destroy'}), name='update_main_project'),
    path('project_id_wise_get_project_data/<int:project_id>',ProjectIdWIseGetProjectDataViewSet.as_view({'get':'list'}), name='project_id_wise_get_project_data'),

    path('project_active_deactivate/<int:project_id>', ActiveDeactiveProjectViewSet.as_view({'put':'update'}), name='project_active_deactivate'),

    path('getactiveproject',GetActiveProjectViewSet.as_view({'get':'list'}), name='getactiveproject'),
    path('numberofprojects', NumberofProjectViewSet.as_view({'get':'list'}), name='numberofprojects'),

    path('create_milestone', ProjectMilestoneViewSet.as_view({'post': 'create'}), name='create_milestone'),
    path('get_milestone', ProjectMilestoneViewSet.as_view({'get': 'list'}), name='get_milestone'),
    path('milestone_id_wise_get_milestone/<int:milestone_id>', IdWiseProjectMilestoneViewSet.as_view({'get': 'list'}), name='get_milestone'),
    path('update_milestone/<int:milestone_id>', ProjectMilestoneUpdateViewSet.as_view({'put': 'update'}), name='update_milestone'),
    path('milestone_completed/<int:milestone_id>', ProjectMilestoneCompletedViewSet.as_view({'put': 'update'}), name='completed_milestone'),
    path('upcoming_milestone', UpcomingMilestoneViewSet.as_view({'get':'list'}), name='upcoming_milestone'),

    path('starting_milestone/<int:milestone_id>', ProjectMilestoneStartViewSet.as_view({'put': 'update'}), name='starting_milestone'),

    path('milestone_active_deactivate/<int:milestone_id>', ActiveDeactiveMilestoneViewSet.as_view({'put':'update'}), name='milestone_active_deactivate'),
    
    path('getactivemilestone',GetActiveMilestoneViewSet.as_view({'get':'list'}), name='getactivemilestone'),
    
    # path('add_drawing_and_design',AddDrawingandDesignViewSet.as_view({'post':'create','get':'list'}), name='add_drawing_design'),
    path('get_drawing_and_design',AddDrawingandDesignViewSet.as_view({'get':'list'}), name='get_drawing_design'),
    path('upload_excel_drawing_and_design',UploadExcelDrawingDataView.as_view(), name='UploadDrawingDataView'),
    path('update_drawing_and_design/<int:drawing_and_design_id>',DrawingandDesignUpdateViewSet.as_view({'put':'update','delete':'destroy'}), name='update_drawing_design'),
    path('approval_or_commented_action_on_drawing_and_design/<int:drawing_and_design_id>', ApprovalOrCommentedActionOnDrawingandDesignViewSet.as_view({'put':'update'}), name='approval_or_commented_action_on_drawing_and_design'),
    path('projcet_idwise_get_drawing_and_design/<int:project_id>',ProjectIdwiseGetDrawingandDesignViewSet.as_view({'get':'list'}), name='projcet_idwise_get_drawing_and_design'),
    path('drawing_id_wise_get_drawing_and_design/<int:drawing_and_design_id>',DrawingIdWiseGetDrawingandDesignViewSet.as_view({'get':'list'}), name='drawing_id_wise_get_drawing_and_design'),
    path('drawing_and_design_resubmitted_action/<int:drawing_and_design_id>',DrawingandDesignResubmittedActionViewSet.as_view({'put':'update'}), name='drawing_and_design_resubmitted_action'),

    path('create_inflow_payment_on_milestone',InFlowPaymentOnMilestoneViewSet.as_view({'post':'create','get':'list'}), name='create_inflow_payment_on_milestone'),
    path('update_inflow_payment_on_milestone/<int:inflow_payment_on_milestone_id>',UpdateInflowPaymentMiletoneViewSet.as_view({'put':'update','delete':'destroy'}), name='update_inflow_payment_on_milestone'),
    path('milestone_id_wise_get_inflow_payment_on_milestone/<int:milestone_id>',MilestoneIdWiseGetInflowPaymentOnMilestoneViewSet.as_view({'get':'list'}), name='milestone_id_wise_get_inflow_payment_on_milestone'),
    
    path('project_id_wise_landbank_location/<int:project_id>',ProjectIdwiseGetLandBankLocationViewSet.as_view({'get':'list'}), name='project_id_wise_landbank_location'),

    path('drawing_dashboard_count', DrawingDashboardCountViewSet.as_view({'get':'list'}), name='drawing_dashboard_count'),

    
    path('upload_project_progress/', UploadExcelProgressView.as_view(), name='upload_project_progress'),
    path('get_progress/', ProjectProgressListView.as_view(), name='get_progress'),

    ## Approved Land Bank Data
    path('land_bank_data_approved_by_project_hod/', ApprovedLandBankByProjectHODDataViewSet.as_view(), name='approved_land_bank_data'),

]