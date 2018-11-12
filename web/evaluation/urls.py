from django.urls import path, reverse_lazy
from . import views
from django.conf.urls import url
app_name = 'evaluation'

urlpatterns = [
    path('', views.appraiserEvaluationView, name='apprariserEvaluation')
]
