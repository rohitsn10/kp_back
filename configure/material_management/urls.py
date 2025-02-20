from material_management.views import *
from django.urls import path

urlpatterns = [
    path('material_management_create', MaterialManagementCreateViewSet.as_view({'post':'create','get':'list'}), name='material_management_create'),
    path('material_management_update/<int:material_id>', MaterialManagementUpdateViewSet.as_view({'put':'update','delete':'destroy'}), name='material_management_update'),
    path('update_only_delivered_date_of_material/<int:material_id>', UpddateOnlyDeliverDateOfMaterialViewSet.as_view({'put':'update'}), name='update_only_delivered_date_of_material'),
    
    path('add_inspection_of_material', AddInspectionOfMaterialViewset.as_view({'post':'create','get':'list'}), name='add_inspection_of_material'),
    path('material_id_wise_get_inspection/<int:material_id>',MaterialIdwiseGetInspectionViewset.as_view({'get':'list'}), name='material_id_wise_get_inspection'),
    path('approval_action_inspection/<int:inspection_id>', ApprovedInspectionViewset.as_view({'put':'update'}), name='approval_action_inspection'),

]