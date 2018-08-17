from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes')
]
