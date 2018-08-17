from django.views.generic import FormView
from django.shortcuts import render
from .forms import LocationSearchForm

from appraisal.models import Appraisal

#class SampleFormView(FormView):
#    form_class = LocationSearchForm
#    template_name = "sample_map/index.html"

def home(request):
    form = LocationSearchForm

    appraisals = Appraisal.objects.all().order_by('timeCreated')

    context = {'form':form,'appraisals':appraisals}

    return render(request, 'home/index.html',context)
