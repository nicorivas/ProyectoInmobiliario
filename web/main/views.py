from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal, Comment
from django.contrib.auth.models import User
from user.views import appraiserWork, visadorWork

import reversion, datetime
from copy import deepcopy
from reversion.models import Version
from appraisal.forms import FormComment


def save_appraisalNF(appraisal, request, comment):
    print('save_appraisal')
    with reversion.create_revision():
        appraisal.save()
        reversion.set_user(request.user)
        reversion.set_comment(comment)
        return

def assign_tasadorNF(request):
    print(request.POST)
    pk = request.POST.dict()['tasadorAppraisal_id'];
    appraisal = Appraisal.objects.get(pk=pk)
    appraisal.tasadorUser = User.objects.get(pk=request.POST.dict()['tasador'])
    save_appraisalNF(appraisal, request,'Changed tasador')
    return

def assign_visadorNF(request):
    appraisal = Appraisal.objects.get(pk=request.POST.dict()['visadorAppraisal_id'])
    appraisal.visadorUser = User.objects.get(pk=request.POST.dict()['visador'])
    save_appraisalNF(appraisal, request,'Changed visador')
    return

@login_required(login_url='/user/login')
def main(request):

    if request.method == 'POST':
        print(request.POST)
        if 'delete' in request.POST:
            # Handle the delete button, next to every appraisal
            id = int(request.POST['appraisal_id'])
            appraisal = Appraisal.objects.get(pk=id)
            appraisal.delete()
        if 'btn_assign_tasador' in request.POST.keys():
            print(request.POST.dict())
            ret = assign_tasadorNF(request)
        if 'btn_assign_visador' in request.POST.keys():
            print(request.POST.dict())
            ret = assign_visadorNF(request)


    tasadores = User.objects.filter(groups__name__in=['tasador'])
    tasadores_info = appraiserWork(tasadores)
    visadores = User.objects.filter(groups__name__in=['visador'])
    visadores_info = visadorWork(visadores)

    appraisals_active, appraisals_finished = userAppraisals(request)

    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished,
        'tasadores':tasadores_info, 'visadores':visadores_info}

    return render(request, 'main/index.html', context)

def logbook(request):
    '''
    '''
    id = int(request.GET['id'])
    appraisal = Appraisal.objects.get(id=id)
    form = FormComment(label_suffix='')

    return render(request,'main/logbook.html',{'appraisal':appraisal,'form':form})

def comment(request):
    '''
    '''
    print('comment')
    print(request.POST)
    id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=id)
    comment = Comment(
        user=request.user,
        text=request.POST['text'],
        event=int(request.POST['event']),
        timeCreated=datetime.datetime.now(),
        appraisal=appraisal)
    comment.save()

    appraisal.comments.add(comment)
    appraisal.save()

    form = FormComment(label_suffix='')

    return render(request,'main/logbook.html',{'appraisal':appraisal,'form':form})
