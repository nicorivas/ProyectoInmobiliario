from django.urls import path

from . import views

urlpatterns = [
    path('<int:appraisal_id>/',views.view_appraisal,name='views-appraisal'),
    path('ajax/computeValuations/', views.ajax_computeValuations, name='ajax_computeValuations'),
    path('ajax/upload_photo/', views.ajax_upload_photo, name='ajax_upload_photo_url'),
    path('ajax/load_realestate/', views.ajax_load_realestate, name='ajax_load_realestate_url'),
    path('ajax/edit_address_modal/', views.ajax_edit_address_modal, name='ajax_edit_address_modal_url'),
    path('ajax/edit_address/', views.ajax_edit_address, name='ajax_edit_address_url'),
    path('ajax/add_address_modal/', views.ajax_add_address_modal, name='ajax_add_address_modal_url'),
    path('ajax/add_address/', views.ajax_add_address, name='ajax_add_address_url'),
    path('ajax/remove_address/', views.ajax_remove_address, name='ajax_remove_address_url'),
    path('ajax/remove_addres_modal/', views.ajax_remove_address_modal, name='ajax_remove_address_modal_url'),
    path('ajax/show_property/', views.ajax_show_property, name='ajax_show_property_url'),
    path('ajax/add_property_modal/', views.ajax_add_property_modal, name='ajax_add_property_modal_url'),
    path('ajax/add_property/', views.ajax_add_property, name='ajax_add_property_url'),
    path('ajax/edit_property_modal/', views.ajax_edit_property_modal, name='ajax_edit_property_modal_url'),
    path('ajax/edit_property/', views.ajax_edit_property, name='ajax_edit_property_url'),
    path('ajax/remove_property/', views.ajax_remove_property, name='ajax_remove_property_url'),
    path('ajax/add_apartment_modal/', views.ajax_add_apartment_modal, name='ajax_add_apartment_modal_url'),
    path('ajax/add_apartment/', views.ajax_add_apartment, name='ajax_add_apartment_url'),
    path('ajax/save_property/', views.ajax_save_property, name='ajax_save_property_url')
]
