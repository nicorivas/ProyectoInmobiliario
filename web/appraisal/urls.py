from django.urls import path

from . import views

urlpatterns = [
    path('<str:region>/<str:commune>/<str:street>/<int:number>/<int:id_b>/'
         'departamento/<int:numbera>/<int:id_a>/<int:id_appraisal>/',
        views.appraisal,
        name='views-appraisal'),
]
