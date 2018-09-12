from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from appraisal.models import Appraisal

#class SampleFormView(FormView):
#    form_class = LocationSearchForm
#    template_name = "sample_map/index.html"

@login_required(login_url='/')
def main(request):

    appraisals = Appraisal.objects.all().order_by('timeCreated')

    context = {'appraisals':appraisals}

    return render(request, 'main/index.html',context)
