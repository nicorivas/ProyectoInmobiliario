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

from evaluation.forms import EvaluationForm
from appraisal.models import AppraisalEvaluation


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
    evaluationForm = EvaluationForm()
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
        if 'evaluadorAppraisal_id' in request.POST.keys():
            evaluationForm = EvaluationForm(request.POST)
            if evaluationForm.is_valid():
                _onTime = evaluationForm.cleaned_data['onTime']
                _completeness = evaluationForm.cleaned_data['completeness']
                _generalQuality = evaluationForm.cleaned_data['generalQuality']
                _correctSurface = evaluationForm.cleaned_data['correctSurface']
                _homologatedReferences = evaluationForm.cleaned_data['homologatedReferences']
                _completeNormative = evaluationForm.cleaned_data['completeNormative']
                _commentText = evaluationForm.cleaned_data['commentText']
                _commentFeedback = evaluationForm.cleaned_data['commentFeedback']
                appraisal = Appraisal.objects.get(pk=request.POST['evaluadorAppraisal_id'])
                appraiser = User.objects.get(pk=request.POST['evaluador_id'])
                evaluation, created = AppraisalEvaluation.objects.update_or_create(
                                        appraisal=appraisal,
                                        #user=appraiser,
                                        defaults={
                                            "appraisal":appraisal,
                                            'user':appraiser,
                                            'onTime':_onTime,
                                            'completeness':_completeness,
                                            'generalQuality':_generalQuality,
                                            'correctSurface': _correctSurface ,
                                            'completeNormative': _completeNormative,
                                            'homologatedReferences': _homologatedReferences,
                                            'commentText':_commentText,
                                            'commentFeedback':_commentFeedback})
                #evaluationForm.save()
                print(evaluation.evaluationResult)


    tasadores = User.objects.filter(groups__name__in=['tasador'])
    tasadores_info = appraiserWork(tasadores)
    visadores = User.objects.filter(groups__name__in=['visador'])
    visadores_info = visadorWork(visadores)

    appraisals_active, appraisals_finished = userAppraisals(request)

    context = {
        'evaluationForm': evaluationForm,
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
