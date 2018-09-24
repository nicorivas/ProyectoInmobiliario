from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),
    path('ajax/house-selected-option/', views.apt_block, name='house_selected_option')
]
