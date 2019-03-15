from django.urls import path

from . import views

urlpatterns = [
    path('', views.accountingView, name='accounting'),
    path('ajax_accountingView_url/', views.ajax_accountingView, name='ajax_accountingView_url'),
    path('ajax_accountingView_url2/', views.accountingView, name='ajax_accountingView_url2'),
]