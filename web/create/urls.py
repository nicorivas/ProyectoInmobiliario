from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_create, name='create'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
]
