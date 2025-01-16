from django.urls import path
from activity_module.views import *

urlpatterns = [

    path('create_activity', ProjectActivityViewSet.as_view({'post': 'create'}), name='create_activity'),
    path('get_activity', ProjectActivityViewSet.as_view({'get': 'list'}), name='get_activity'),
    path('update_activity/<int:activity_id>', ProjectActivityUpdateViewSet.as_view({'put': 'update'}), name='update_activity'),
    
]