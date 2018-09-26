from django.urls import path

from . import views

urlpatterns = [
    path('<str:region>/<str:commune>/<str:street>/<int:number>/edificio/<int:id>/',
        views.building,
        name='views-building'),
    path('<str:region>/<str:commune>/<str:street>/<int:number>/edificio/<int:id>/<int:floor>/<int:fnumber>/',
        views.apartment,
        name='views-apartment'),
    path('<str:region>/<str:commune>/<str:street>/<int:number>/casa/<int:id>/',
        views.house,
        name='views-house')
]
