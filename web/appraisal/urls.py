from django.urls import path

from . import views
from . import properti
from . import comparable

urlpatterns = [
    path('<int:appraisal_id>/',views.view_appraisal,name='views-appraisal'),
    path('ajax/computeValuations/', views.ajax_computeValuations, name='ajax_computeValuations'),
    
    path('ajax/load_sidebar/', properti.ajax_load_sidebar, name='ajax_load_sidebar_url'),

    path('ajax/photo_modal/', views.ajax_photo_modal, name='ajax_photo_modal_url'),
    path('ajax/photo_save/', views.ajax_photo_save, name='ajax_photo_save_url'),
    path('ajax/photo_remove/', views.ajax_photo_remove, name='ajax_photo_remove_url'),

    path('ajax/load_realestate/', views.ajax_load_realestate, name='ajax_load_realestate_url'),
    
    path('ajax/edit_address_modal/', properti.ajax_edit_address_modal, name='ajax_edit_address_modal_url'),
    path('ajax/edit_address/', properti.ajax_edit_address, name='ajax_edit_address_url'),
    #path('ajax/edit_address/', address.ajax_edit_address, name='ajax_edit_address_url'),
    #path('ajax/add_address_modal/', address.ajax_add_address_modal, name='ajax_add_address_modal_url'),
    #path('ajax/add_address/', address.ajax_add_address, name='ajax_add_address_url'),
    #path('ajax/remove_address/', address.ajax_remove_address, name='ajax_remove_address_url'),
    #path('ajax/remove_addres_modal/', address.ajax_remove_address_modal, name='ajax_remove_address_modal_url'),
    
    path('ajax/show_property/', properti.ajax_show_property, name='ajax_show_property_url'),
    path('ajax/add_property_modal/', properti.ajax_add_property_modal, name='ajax_add_property_modal_url'),
    path('ajax/add_property/', properti.ajax_add_property, name='ajax_add_property_url'),
    path('ajax/edit_property_modal/', properti.ajax_edit_property_modal, name='ajax_edit_property_modal_url'),
    path('ajax/edit_property/', properti.ajax_edit_property, name='ajax_edit_property_url'),
    path('ajax/remove_property/', properti.ajax_remove_property, name='ajax_remove_property_url'),
    path('ajax/add_apartment_modal/', properti.ajax_add_apartment_modal, name='ajax_add_apartment_modal_url'),
    path('ajax/add_apartment/', properti.ajax_add_apartment, name='ajax_add_apartment_url'),
    path('ajax/remove_property/', properti.ajax_remove_property, name='ajax_remove_property_url'),
    path('ajax/save_property/', properti.ajax_save_property, name='ajax_save_property_url'),
    
    path('ajax/add_rol_modal/', views.ajax_add_rol_modal, name='ajax_add_rol_modal_url'),
    path('ajax/add_rol/', views.ajax_add_rol, name='ajax_add_rol_url'),
    path('ajax/edit_rol_modal/', views.ajax_edit_rol_modal, name='ajax_edit_rol_modal_url'),
    path('ajax/edit_rol/', views.ajax_edit_rol, name='ajax_edit_rol_url'),
    path('ajax/remove_rol/', views.ajax_remove_rol, name='ajax_remove_rol_url'),
    
    path('ajax/save_appraisal/', views.ajax_save_appraisal, name='ajax_save_appraisal_url'),

    path('ajax/load_tab_value/', views.ajax_load_tab_value, name="ajax_load_tab_value"),
    path('ajax/load_tab_value_comparable', views.ajax_load_tab_value_comparable, name="ajax_load_tab_value_comparable_url"),

    path('ajax/add_property_comparable_modal/', comparable.ajax_add_property_comparable_modal, name='ajax_add_property_comparable_modal_url'),
    path('ajax/add_property_comparable/', comparable.ajax_add_property_comparable, name='ajax_add_property_comparable_url'),
    path('ajax/edit_property_comparable_modal/', comparable.ajax_edit_property_comparable_modal, name='ajax_edit_property_comparable_modal_url'),
    path('ajax/edit_property_comparable/', comparable.ajax_edit_property_comparable, name='ajax_edit_property_comparable_url'),
    path('ajax/remove_property_comparable/', comparable.ajax_remove_property_comparable, name='ajax_remove_property_comparable_url')
]
