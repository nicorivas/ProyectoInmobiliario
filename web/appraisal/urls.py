from django.urls import path

from . import views

urlpatterns = [
    path('<int:appraisal_id>/',views.view_appraisal,name='views-appraisal'),
    path('ajax/computeValuations/', views.ajax_computeValuations, name='ajax_computeValuations'),
    path('ajax/upload_photo/', views.ajax_upload_photo, name='ajax_upload_photo_url')
]
