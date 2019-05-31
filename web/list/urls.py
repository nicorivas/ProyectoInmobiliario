from django.urls import path
from . import views
from . import modals
from appraisal import properti as appraisal_views
from logbook import views as logbookviews

urlpatterns = [
    path('', views.main, name='main'),
    path('imported', views.imported_appraisals, name='appraisals_imported'),
    path('ajax/logbook/', logbookviews.ajax_logbook, name='ajax_logbook_url'),
    path('ajax/logbook_close/', logbookviews.ajax_logbook_close, name='ajax_logbook_close_url'),
    path('ajax/logbook_change_event/', logbookviews.ajax_logbook_change_event, name='ajax_logbook_change_event_url'),
    path('ajax/accept_appraisal/', views.ajax_accept_appraisal, name='ajax_accept_appraisal_url'),
    path('ajax/reject_appraisal/', views.ajax_reject_appraisal, name='ajax_reject_appraisal_url'),
    path('ajax/archive_appraisal/', views.ajax_archive_appraisal, name='ajax_archive_appraisal_url'),
    
    path('ajax/assign_tasador_modal/', modals.ajax_assign_tasador_modal, name='ajax_assign_tasador_modal_url'),
    path('ajax/assign_tasador/', modals.ajax_assign_tasador, name='ajax_assign_tasador_url'),
    path('ajax/assign_tasador_tasadores',modals.ajax_assign_tasador_tasadores, name="ajax_assign_tasador_tasadores_url"),
    path('ajax/unassign_tasador/', modals.ajax_unassign_tasador, name='ajax_unassign_tasador_url'),
    
    path('ajax/assign_visador_modal/', modals.ajax_assign_visador_modal, name='ajax_assign_visador_modal_url'),
    path('ajax/assign_visador/', modals.ajax_assign_visador, name='ajax_assign_visador_url'),
    path('ajax/assign_visador_visadores',modals.ajax_assign_visador_visadores, name="ajax_assign_visador_visadores_url"),
    path('ajax/unassign_visador/', modals.ajax_unassign_visador, name='ajax_unassign_visador_url'),

    path('ajax/comment/', views.ajax_comment, name='ajax_comment_url'),
    path('ajax/validate_cliente/', views.ajax_validate_cliente, name='ajax_validate_cliente_url'),
    path('ajax/unvalidate_cliente/', views.ajax_unvalidate_cliente, name='ajax_unvalidate_cliente_url'),
    path('ajax/delete_comment/', views.ajax_delete_comment, name='ajax_delete_comment_url'),
    path('ajax/get_appraisal_row/',views.ajax_get_appraisal_row,name="ajax_get_appraisal_row_url"),
    path('ajax/evaluate_modal/', views.ajax_evaluate_modal, name='ajax_evaluate_modal_url'),
    path('ajax/evaluate_modal_close/', views.ajax_evaluate_modal_close, name='ajax_evaluate_modal_close_url'),
    path('ajax/enviar_a_visador/', views.ajax_enviar_a_visador, name='ajax_enviar_a_visador_url'),
    path('ajax/devolver_a_tasador/', views.ajax_devolver_a_tasador, name='ajax_devolver_a_tasador_url'),
    path('ajax/enviar_a_cliente/', views.ajax_enviar_a_cliente, name='ajax_enviar_a_cliente_url'),
    path('ajax/devolver_a_visador/', views.ajax_devolver_a_visador, name='ajax_devolver_a_visador_url'),
    path('ajax/mark_as_returned/', views.ajax_mark_as_returned, name='ajax_mark_as_returned_url'),
    path('ajax/solve_conflict/', views.ajax_solve_conflict, name='ajax_solve_conflict_url'),
    path('ajax/upload_report/', views.ajax_upload_report, name='ajax_upload_report_url'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
    path('ajax/save_time_due/', views.ajax_save_time_due, name='ajax_save_time_due'),
    path('ajax/expenses_modal/', views.ajax_expenses_modal, name='ajax_appraisal_expenses_modal_url'),
    path('ajax/expenses/save', views.ajax_save_expenses, name='ajax_save_expenses_url'),
    path('ajax/expenses/delete', views.ajax_delete_expenses, name='ajax_delete_expenses_url'),
    path('ajax/edit_address_modal/', appraisal_views.ajax_edit_address_modal, name='ajax_edit_address_modal_url'),
    path('ajax/edit_address/', appraisal_views.ajax_edit_address, name='ajax_edit_address_url'),
]
