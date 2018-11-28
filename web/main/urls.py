from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ajax/logbook/', views.logbook, name='ajax_logbook_url'),
    path('ajax/comment/', views.comment, name='ajax_comment_url'),
]
