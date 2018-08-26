from django.urls import path

from . import views

urlpatterns = [
    path('<int:code>/',
        views.commune,
        name='views-commune'),
]
