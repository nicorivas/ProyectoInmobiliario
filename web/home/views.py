from django.views.generic import FormView
from django.shortcuts import render
from .forms import LocationSearchForm

#class SampleFormView(FormView):
#    form_class = LocationSearchForm
#    template_name = "sample_map/index.html"

def home(request):
    form = LocationSearchForm
    context = {'form':form}
    return render(request, 'home/index.html',context)
