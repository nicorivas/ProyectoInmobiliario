from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ajax/logbook/', views.logbook, name='ajax_logbook_url'),
    path('ajax/logbook_close/', views.logbook_close, name='ajax_logbook_close_url'),
    path('ajax/comment/', views.comment, name='ajax_comment_url'),
    path('ajax/delete_comment/', views.delete_comment, name='ajax_delete_comment_url'),
]
