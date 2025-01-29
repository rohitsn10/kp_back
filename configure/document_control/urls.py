from django.urls import path
from document_control.views import *

urlpatterns = [
    path('documentmanagement', DocumentViewSet.as_view({'post':'create','get':'list'}), name='document'),
    path('documentmanagement/<int:document_id>', DocumentUpdateViewSet.as_view({'put':'update','delete':'destroy'}), name='document'),
]