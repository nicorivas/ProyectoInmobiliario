from django.urls import path

from . import views

urlpatterns = [
    path('<int:code>/',
        views.province,
        name='views-province'),
]
