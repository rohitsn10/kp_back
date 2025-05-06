from land_module.views import *
from django.urls import path

urlpatterns = [
    path('land_category_create', CreateLandCategoryViewSet.as_view({'post':'create','get':'list'}), name='land_category'),
    path('land_category_update/<int:land_category_id>', UpdateLandCategoryViewSet.as_view({'put':'update','delete':'destroy'}), name='land_category_update'),
    
    path('create_land_bank_master', LandBankMasterCreateViewset.as_view({'post':'create','get':'list'}), name='land_bank'),
    path('update_land_bank_master/<int:land_bank_id>', LandBankMasterUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='land_bank_update'),
    path('approve_land_bank_by_hod/<int:land_bank_id>', ApproveRejectLandBankDataByHODViewset.as_view({'put':'update'}), name='approve_land_bank_by_hod'),

    path('add_data_after_approval_land_bank', AddDataAfterApprovalLandBankViewset.as_view({'post':'create','get':'list'}), name='update_data_after_approval_land_bank'),
    path('update_data_after_approval_land_bank/<int:land_bank_after_approved_data_id>', UpdateDateAfterApprovalLandBankViewset.as_view({'put':'update'}), name='update_data_after_approval_land_bank'),
    path('get_land_bank_id_wise_22_forms_data/<int:land_bank_id>', GetLandBankIdWise22FormsDataViewset.as_view({'get':'list'}), name='get_land_bank_id_wise_22_forms_data'),

    path('add_sfa_data_to_land_bank', AddFSALandBankDataViewset.as_view({'post':'create','get':'list'}), name='add_sfa_data_to_land_bank'),
    path('update_sfa_data_to_land_bank/<int:land_bank_id>', UpdateFSALandBankDataViewset.as_view({'put':'update'}), name='update_sfa_data_to_land_bank'),
    
    path('approve_reject_land_bank_status/<int:land_bank_id>', ApproveRejectLandbankStatus.as_view({'put':'update'}), name='approve_reject_land_bank_status'),
    path('create_land_bank_location', CrateLandBankLocationViewset.as_view({'post':'create','get':'list'}), name='create_land_bank_location'),
    path('landbank_id_wise_location_list/<int:land_bank_id>', LandBankIdWiseLocationViewset.as_view({'get':'list'}), name='landbank_id_wise_location_list'),
    path('update_land_bank_location/<int:land_bank_location_id>', UpdateLandBankLocationViewset.as_view({'put':'update','delete':'destroy'}), name='update_land_bank_location'),
    path('land_location_idwise_survey_number/<int:location_name_id>', LandLocationIdWiseLandSurveyNumberViewset.as_view({'get':'list'}), name='land_location_idwise_survey_number'),

    path('update_land_survey_number/<int:land_survey_number_id>', UpdateLandSurvetNumberViewset.as_view({'put':'update'}), name='update_land_survey_number'),

    path('landbank_excel', LandbankExcelViewSet.as_view({'get':'list'}), name='export_landbank_excel'),
]