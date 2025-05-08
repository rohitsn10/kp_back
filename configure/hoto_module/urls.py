from django.urls import path
from .views import *


urlpatterns = [
    path('upload_main_document', UploadMainDocumentViewSet.as_view({'post': 'create'}), name='upload_main_document'),
    path('view_document/<int:project_id>', ViewDocumentViewSet.as_view({'get': 'list'}), name='view_document'),

    path('add_remarks_to_document/<int:doc_id>', AddRemarksToDocumentViewSet.as_view({'put': 'update'}), name='add_remarks_to_document'),
    path('upload_document/<int:doc_id>', UploadDocumentViewSet.as_view({'put': 'update'}), name='upload_document'),
    path('delete_document', DeleteParticularDocumentViewSet.as_view({'delete': 'destroy'}), name='delete_document'),

    path('verify_document/<int:doc_id>', VerifyDocumentViewSet.as_view({'put': 'update'}), name='verify_document'),

    path('punch_points/<int:doc_id>', PunchPointsViewSet.as_view({'get': 'list', 'post': 'create'}), name='punch_points'),
]