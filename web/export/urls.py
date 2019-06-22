from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ajax/export/', views.export, name='export_url')
]