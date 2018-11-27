from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.view_create, name='create'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
	path('ajax/populate_from_file/', views.populate_from_file, name='ajax_populate_from_file'),
]
