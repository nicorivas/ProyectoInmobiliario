from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.archive, name='archive'),
    path('ajax/search', views.ajax_search, name='ajax_search_url'),
]
