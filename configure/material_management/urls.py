from material_management.views import *
from django.urls import path

urlpatterns = [
    path('material_management_create', MaterialManagementCreateViewSet.as_view({'post':'create','get':'list'}), name='material_management_create'),
    path('material_management_update/<int:material_id>', MaterialManagementUpdateViewSet.as_view({'put':'update','delete':'destroy'}), name='material_management_update'),

]