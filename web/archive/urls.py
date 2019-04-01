from django.urls import path
from django.conf.urls import url

from . import views
from logbook import views as logbookviews

urlpatterns = [
    path('', views.archive, name='archive'),
    path('ajax/search', views.ajax_search, name='ajax_search_url'),
    path('ajax/unarchive_appraisal_modal', views.ajax_unarchive_appraisal_modal, name='ajax_unarchive_appraisal_modal_url'),
    path('ajax/unarchive_appraisal', views.ajax_unarchive_appraisal, name='ajax_unarchive_appraisal_url'),
    path('ajax/delete_appraisal_modal', views.ajax_delete_appraisal_modal, name='ajax_delete_appraisal_modal_url'),
    path('ajax/delete_appraisal', views.ajax_delete_appraisal, name='ajax_delete_appraisal_url'),
    path('ajax/logbook/', logbookviews.ajax_logbook, name='ajax_logbook_url'),
]
