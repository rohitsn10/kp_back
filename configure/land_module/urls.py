from land_module.views import *
from django.urls import path

urlpatterns = [
    path('land_category_create', CreateLandCategoryViewSet.as_view({'post':'create','get':'list'}), name='land_category'),
    path('land_category_update/<int:land_category_id>', UpdateLandCategoryViewSet.as_view({'put':'update','get':'list'}), name='land_category_update'),
    
    path('create_land_bank_master', LandBankMasterCreateViewset.as_view({'post':'create','get':'list'}), name='land_bank'),
]