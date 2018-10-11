from django.urls import path
from . import views

urlpatterns = [
    #path('tasaciones/', views.appraiserListOfAppraisals.as_view(), name='tasaciones-usuario'),
    path('tasaciones/', views.userAppraisals, name='tasaciones-usuario'),
]