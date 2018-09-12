from django.views.generic import FormView
from django.shortcuts import render

from appraisal.models import Appraisal

#class SampleFormView(FormView):
#    form_class = LocationSearchForm
#    template_name = "sample_map/index.html"

def home(request):

    return render(request, 'home/index.html')
