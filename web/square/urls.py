from django.urls import path

from . import views

urlpatterns = [
    path('<int:code>/',
        views.square,
        name='views-square'),
]
