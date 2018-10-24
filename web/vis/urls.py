from django.urls import path

from . import views

urlpatterns = [
    path('',views.vis,name='vis'),
    path('summary/',views.summary_country,name='vis_summary'),
    path('summary/<int:region_id>/',views.summary_region,name='vis_summary'),
    path('summary/<int:region_id>/<int:commune_id>/',views.summary_commune,name='vis_summary'),
]
