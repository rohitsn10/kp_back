from django.urls import path
from document_control.views import *

urlpatterns = [
    path('document_management', DocumentViewSet.as_view({'post':'create','get':'list'}), name='document'),
    path('document_management/<int:document_id>', DocumentUpdateViewSet.as_view({'put':'update','delete':'destroy'}), name='document'),
    path('delete_document_files/<int:attachment_id>', DeleteDocumentsFilesView.as_view({'delete':'destroy'}), name='document_active_deactivate'),
]