from material_management.views import *
from django.urls import path

urlpatterns = [
    path('material_management_create', MaterialManagementCreateViewSet.as_view({'post':'create','get':'list'}), name='material_management_create'),

]