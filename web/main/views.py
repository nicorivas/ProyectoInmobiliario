from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from appraisal.models import Appraisal

@login_required(login_url='/')
def main(request):

    appraisals_active = Appraisal.objects.filter(Q(state=Appraisal.STATE_ACTIVE)|Q(state=Appraisal.STATE_PAUSED)).order_by('timeCreated')

    appraisals_finished = Appraisal.objects.filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')

    context = {
        'appraisals_active':appraisals_active,
        'appraisals_finished':appraisals_finished}

    return render(request, 'main/index.html',context)
