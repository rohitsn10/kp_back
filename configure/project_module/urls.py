
from django.urls import path
from project_module.views import *

urlpatterns = [
    path('create_expense_data', ProjectExpenseCreateViewset.as_view({'post':'create','get':'list'}), name='create_expense_data'),
    path('update_expense_data/<int:expense_id>', ProjectExpenseUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_expense_data'),

    path('create_client_data', ClientDataCreateViewset.as_view({'post':'create','get':'list'}), name='create_client_data'),
    path('update_client_data/<int:client_id>', ProjectClientUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_client_data'),

    path('create_wo_po_data', Wo_Po_DataCreateViewset.as_view({'post':'create','get':'list'}), name='create_wo_po_data'),
    path('update_wo_po_data/<int:wo_po_id>', Wo_Po_DataUpdateViewset.as_view({'put':'update','delete':'destroy'}), name='update_wo_po_data'),

    path('create_main_project', ProjectViewSet.as_view({'post':'create','get':'list'}), name='create_main_project'),

    path('company', CompanyViewSet.as_view({'post':'create','get':'list'}), name='company'),
    path('company/<int:id>', CompanyViewSet.as_view({'put':'update','delete':'destroy'}), name='company'),
]