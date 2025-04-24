from django.urls import path
from quality_inspection.views import *

urlpatterns = [
    path('create_items', AddItemsViewSet.as_view({'post': 'create'}), name='create_items'),
    path('active_items', ActiveItemsViewSet.as_view({'put': 'update'}), name='active_items'),
    path('list_items/<int:project_id>', ProjectIdWiseItemsViewSet.as_view({'get': 'list'}), name='list_items'),
    path('update_items/<int:item_id>', UpdateItemsViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_items'),

    # path('create_vendor', AddVendorViewSet.as_view({'post': 'create'}), name='create_vendor'),
    # path('list_vendor/<int:project_id>', ProjectIdWiseVendorViewSet.as_view({'get': 'list'}), name='list_vendor'),
]