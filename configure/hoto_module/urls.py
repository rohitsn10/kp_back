from django.urls import path
from .views import *


urlpatterns = [
    path('upload_main_document', UploadMainDocumentViewSet.as_view({'post': 'create'}), name='upload_main_document'),
    path('view_document/<int:project_id>', ViewDocumentViewSet.as_view({'get': 'list'}), name='view_document'),
    path('fetch_all_documents_names', FetchAllDocumentsNamesView.as_view(), name='fetch_all_documents'),

    path('add_remarks_to_document/<int:doc_id>', AddRemarksToDocumentViewSet.as_view({'put': 'update'}), name='add_remarks_to_document'),
    path('upload_document/<int:doc_id>', UploadDocumentViewSet.as_view({'put': 'update'}), name='upload_document'),
    path('delete_document', DeleteParticularDocumentViewSet.as_view({'delete': 'destroy'}), name='delete_document'),
    path('verify_document/<int:doc_id>', VerifyDocumentViewSet.as_view({'put': 'update'}), name='verify_document'),

    path('raise_punch_points', RaisePunchPointsViewSet.as_view({'post': 'create'}), name='raise_punch_points'),

    path('completed_punch_points', CompletedPunchPointsViewSet.as_view({'post': 'create'}), name='completed_punch_points'),

    path('verify_completed_punch_points/<int:completed_punch_id>', VerifyCompletedPunchPointsViewSet.as_view({'put': 'update'}), name='verify_completed_punch_points'),

    path('get_all_object_wise_punch_raise_completed_verify', GetAllObjectWisePunchRaiseCompletedVerifyViewSet.as_view({'get': 'list'}), name='get_all_object_wise_punch_raise_completed_verify'),

    path('hoto_certificate', HOTOCertificateViewSet.as_view({'put': 'update'}), name='hoto_certificate'),
]