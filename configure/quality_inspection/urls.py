from django.urls import path
from quality_inspection.views import *

urlpatterns = [
    path('create_items', AddItemsViewSet.as_view({'post': 'create'}), name='create_items'),
    path('active_items', ActiveItemsViewSet.as_view({'put': 'update'}), name='active_items'),
    path('list_items/<int:project_id>', ProjectIdWiseItemsViewSet.as_view({'get': 'list'}), name='list_items'),
    path('list_all_items', ListAllItemsViewSet.as_view({'get': 'list'}), name='list_all_items'),
    path('update_items/<int:item_id>', UpdateItemsViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_items'),

    # path('create_vendor', AddVendorViewSet.as_view({'post': 'create'}), name='create_vendor'),
    # path('list_vendor/<int:project_id>', ProjectIdWiseVendorViewSet.as_view({'get': 'list'}), name='list_vendor'),

    path('quality_inspection_document_upload', QualityInspectionDocumentUploadViewSet.as_view({'post': 'create'}), name='quality_inspection_document_upload'),
    path('quality_inspection_document_list/<int:item_id>/<int:project_id>', QualityInspectionDocumentListViewSet.as_view({'get': 'list'}), name='quality_inspection_document_list'),

    path('create_quality_inspection_observation_report', CreateQualityInspectionObservationViewSet.as_view({'post': 'create'}), name='create_quality_inspection_observation_report'),
    path('get_quality_inspection_observation_report/<int:item_id>/<int:project_id>', GetQualityInspectionObservationViewSet.as_view({'get': 'list'}), name='get_quality_inspection_observation_report'),

    path('mdcc_report_pdf/<int:item_id>', SupplyMDCCGeneratePDFViewSet.as_view({'get': 'list'}), name='mdcc_report_pdf'),
    path('inspection_call_report_pdf/<int:item_id>', SupplyInspectionCallPDFViewSet.as_view({'post': 'create'}), name='inspection_call_report_pdf'),

    path('create_rfi', CreateRFIViewSet.as_view({'post': 'create'}), name='create_rfi'),
    path('get_rfi/<int:project_id>', GetRFIViewSet.as_view({'get': 'list'}), name='get_rfi'),
    path('electrical_get_rfi/<int:project_id>', ElectricalGetRFIViewSet.as_view({'get': 'list'}), name='electrical_get_rfi'),
    path('mechanical_get_rfi/<int:project_id>', MechanicalGetRFIViewSet.as_view({'get': 'list'}), name='mechanical_get_rfi'),
    path('civil_get_rfi/<int:project_id>', CivilGetRFIViewSet.as_view({'get': 'list'}), name='civil_get_rfi'),
    path('update_rfi/<int:rfi_id>', UpdateRFIViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_rfi'),

    path('create_rfi_inspection_outcome', CreateRFIInspectionOutcomeViewSet.as_view({'post': 'create'}), name='create_rfi_inspection_outcome'),
    path('get_rfi_inspection_outcome/<int:rfi_id>', GetRFIInspectionOutcomeViewSet.as_view({'get': 'list'}), name='get_rfi_inspection_outcome'),
    path('update_rfi_inspection_outcome/<int:rfi_id>', UpdateRFIInspectionOutcomeViewSet.as_view({'put': 'update','delete': 'destroy'}), name='update_rfi_inspection_outcome'),
    path('create_files_upload_inspection_outcome', CreateFilesUploadViewSet.as_view({'post': 'create'}), name='create_files_upload_inspection_outcome'),
    path('get_files_upload_inspection_outcome/<int:rfi_id>', GetFilesUploadViewSet.as_view({'get': 'list'}), name='get_files_upload_inspection_outcome'),

    path('rfi_report_pdf/<int:rfi_id>', RFIReportPDFViewSet.as_view({'get': 'list'}), name='rfi_report_pdf'),

]