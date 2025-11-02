from django.urls import path
from .views import *




urlpatterns = [
    path('upload_main_document', UploadMainDocumentViewSet.as_view({'post': 'create'}), name='upload_main_document'),
    path('view_document/<int:project_id>', ViewDocumentViewSet.as_view({'get': 'list'}), name='view_document'),
    path('fetch_all_documents_names/<int:project_id>', FetchAllDocumentsNamesView.as_view(), name='fetch_all_documents'),
    path('add_remarks_to_document/<int:project_id>', AddRemarksToDocumentViewSet.as_view({'put': 'update'}), name='add_remarks_to_document'),
    path('upload_document/<int:project_id>', UploadDocumentViewSet.as_view({'put': 'create_or_update'}), name='upload_document'),
    path('delete_document/<int:project_id>', DeleteParticularDocumentViewSet.as_view({'delete': 'destroy'}), name='delete_document'),
    path('verify_document/<int:project_id>', VerifyDocumentViewSet.as_view({'put': 'update'}), name='verify_document'),

    path('raise_punch_points/<int:project_id>', RaisePunchPointsViewSet.as_view({'post': 'create'}), name='raise_punch_points'),
    path('accepted_rejected_punch_points/<int:project_id>', AcceptedRejectedPunchPointsViewSet.as_view({'post': 'create'}), name='accepted_rejected_punch_points'),
    path('mark_punch_points_completed/<int:project_id>', MarkPunchPointsCompletedViewSet.as_view({'put': 'update'}), name='mark_punch_points_completed'),  # Added URL
    path('verify_completed_punch_points/<int:project_id>', VerifyCompletedPunchPointsViewSet.as_view({'put': 'update'}), name='verify_completed_punch_points'),
    path('get_all_project_wise_punch_raise_completed_verify/<int:project_id>', GetAllProjectWisePunchRaiseCompletedVerifyViewSet.as_view({'get': 'list'}), name='get_all_project_wise_punch_raise_completed_verify'),

    path('hoto_certificate', HOTOCertificateViewSet.as_view({'put': 'update'}), name='hoto_certificate'),
]