from django.urls import path

from . import views

urlpatterns = [
    path('<str:region>/<str:commune>/<str:street>/<str:number>/<int:res_type>/'
         '<int:building_id>/<int:apartment_id>/<int:appraisal_id>/',
        views.view_appraisal,
        name='views-appraisal'),
    path('<str:region>/<str:commune>/<str:street>/<str:number>/<int:res_type>/'
         '<int:house_id>/<int:appraisal_id>/',
        views.view_appraisal,
        name='views-appraisal'),
    path('<int:appraisal_id>/',
        views.view_appraisal,
        name='views-appraisal'),
    path('ajax/computeValuations/', views.ajax_computeValuations, name='ajax_computeValuations'),
    path('ajax/upload_photo/', views.ajax_upload_photo, name='ajax_upload_photo_url')
]
