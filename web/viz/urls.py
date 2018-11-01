from django.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path

from . import views

urlpatterns = [
    path('',views.vis,name='vis')
]
