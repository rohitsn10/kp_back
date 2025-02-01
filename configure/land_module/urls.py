from land_module.views import *
from django.urls import path

urlpatterns = [
    path('land_category_create', CreateLandCategoryViewSet.as_view({'post':'create','get':'list'}), name='land_category'),
    path('land_category_update/<int:land_category_id>', UpdateLandCategoryViewSet.as_view({'put':'update','delete':'destroy'}), name='land_category_update'),
    
    path('create_land_bank_master', LandBankMasterCreateViewset.as_view({'post':'create','get':'list'}), name='land_bank'),
    path('update_land_bank_master/<int:land_bank_id>', LandBankMasterUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='land_bank_update'),
    path('approve_land_bank_by_hod/<int:land_bank_id>', ApproveRejectLandBankDataByHODViewset.as_view({'put':'update'}), name='approve_land_bank_by_hod'),

    path('update_data_after_approval_land_bank', UpdateDataAfterApprovalLandBankViewset.as_view({'post':'create','get':'list'}), name='update_data_after_approval_land_bank'),
    path('add_sfa_data_to_land_bank/<int:land_bank_id>', AddFSALandBankDataViewset.as_view({'put':'update'}), name='add_sfa_data_to_land_bank'),
    
    path('status_update_land_bank/<int:land_bank_id>', LandBankStatusUpdateViewset.as_view({'put':'update'}), name='update_data_after_approval_land_bank'),
    path('create_land_bank_location', CrateLandBankLocationViewset.as_view({'post':'create','get':'list'}), name='create_land_bank_location'),
    path('landbank_id_wise_location_list/<int:land_bank_id>', LandBankIdWiseLocationViewset.as_view({'get':'list'}), name='landbank_id_wise_location_list'),
    path('update_land_bank_location/<int:land_bank_location_id>', UpdateLandBankLocationViewset.as_view({'put':'update','delete':'destroy'}), name='update_land_bank_location'),
    path('land_location_idwise_survey_number/<int:location_name_id>', LandLocationIdWiseLandSurveyNumberViewset.as_view({'get':'list'}), name='land_location_idwise_survey_number'),
]