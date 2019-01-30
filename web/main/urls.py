from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('imported', views.imported_appraisals, name='appraisals_imported'),
    path('ajax/logbook/', views.ajax_logbook, name='ajax_logbook_url'),
    path('ajax/logbook_close/', views.ajax_logbook_close, name='ajax_logbook_close_url'),
    path('ajax/logbook_change_event/', views.ajax_logbook_change_event, name='ajax_logbook_change_event_url'),
    path('ajax/accept_appraisal/', views.ajax_accept_appraisal, name='ajax_accept_appraisal_url'),
    path('ajax/reject_appraisal/', views.ajax_reject_appraisal, name='ajax_reject_appraisal_url'),
    path('ajax/delete_appraisal/', views.ajax_delete_appraisal, name='ajax_delete_appraisal_url'),
    path('ajax/assign_tasador_modal/', views.ajax_assign_tasador_modal, name='ajax_assign_tasador_modal_url'),
    path('ajax/assign_visador_modal/', views.ajax_assign_visador_modal, name='ajax_assign_visador_modal_url'),
    path('ajax/assign_tasador/', views.ajax_assign_tasador, name='ajax_assign_tasador_url'),
    path('ajax/assign_visador/', views.ajax_assign_visador, name='ajax_assign_visador_url'),
    path('ajax/unassign_tasador/', views.ajax_unassign_tasador, name='ajax_unassign_tasador_url'),
    path('ajax/unassign_visador/', views.ajax_unassign_visador, name='ajax_unassign_visador_url'),
    path('ajax/comment/', views.ajax_comment, name='ajax_comment_url'),
    path('ajax/validate_cliente/', views.ajax_validate_cliente, name='ajax_validate_cliente_url'),
    path('ajax/unvalidate_cliente/', views.ajax_unvalidate_cliente, name='ajax_unvalidate_cliente_url'),
    path('ajax/delete_comment/', views.ajax_delete_comment, name='ajax_delete_comment_url'),
    path('ajax/get_appraisal_row/',views.ajax_get_appraisal_row,name="ajax_get_appraisal_row_url"),
    path('ajax/evaluate_modal/', views.ajax_evaluate_modal, name='ajax_evaluate_modal_url'),
    path('ajax/evaluate_modal_close/', views.ajax_evaluate_modal_close, name='ajax_evaluate_modal_close_url')
]
