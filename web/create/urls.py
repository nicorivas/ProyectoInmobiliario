from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.view_create, name='create'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
	path('ajax/import_request/', views.import_request, name='ajax_import_request'),
    path('ajax/load_grupo/',views.ajax_load_grupo, name="ajax_load_grupo_url")
]
