from django.urls import path

from . import views

urlpatterns = [
    path('<str:region>/<str:commune>/<str:street>/<int:number>/<int:res_type>/'
         '<int:building_id>/<int:apartment_number>/<int:apartment_id>/<int:appraisal_id>/',
        views.appraisal,
        name='views-appraisal'),
    path('<str:region>/<str:commune>/<str:street>/<int:number>/<int:res_type>/'
         '<int:house_id>/<int:appraisal_id>/',
        views.appraisal,
        name='views-appraisal'),
    #path('<str:region>/<str:commune>/<str:street>/<int:number>/<int:id_b>/'
    #     'casa/<int:numbera>/<int:id_a>/<int:id_appraisal>/',
    #    views.appraisal,
    #    name='views-appraisal'),
    path('ajax/computeValuations/', views.ajax_computeValuations, name='ajax_computeValuations')
]
