from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal
from django.contrib.auth.models import User

import reversion
from copy import deepcopy
from reversion.models import Version


def save_appraisalNF(appraisal, request, comment):
    print('save_appraisal')
    with reversion.create_revision():
        appraisal.save()
        reversion.set_user(request.user)
        reversion.set_comment(comment)
        return

def assign_tasadorNF(request):
    appraisal = Appraisal.objects.get(pk=request.POST.dict()['tasadorAppraisal_id'])
    appraisal.tasadorUser = User.objects.get(pk=request.POST.dict()['tasador'])
    save_appraisalNF(appraisal, request,'Changed tasador')
    return

@login_required(login_url='/user/login')
def main(request):

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle the delete button, next to every appraisal
            id = int(request.POST['appraisal_id'])
            appraisal = Appraisal.objects.get(pk=id)
            appraisal.delete()
        if 'btn_assign_tasador' in request.POST.keys():
            print(request.POST.dict())
            ret = assign_tasadorNF(request)


    tasadores = User.objects.filter(groups__name__in=['tasador'])
    appraisals_active, appraisals_finished = userAppraisals(request)
    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished,
        'tasadores':tasadores}

    return render(request, 'main/index.html', context)

