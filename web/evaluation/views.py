from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.views import userAppraisals, appraiserWork
from appraisal.models import AppraisalEvaluation, Appraisal
from .forms import EvaluationForm

from django.core.exceptions import ObjectDoesNotExist

def appraiserEvaluationView(request):
    print(request)

    if request.method == 'POST':

        print(request.POST)
        evaluationForm = EvaluationForm(request.POST)
        if evaluationForm.is_valid():
            evaluationForm.save()
            _onTime = evaluationForm.cleaned_data['onTime']
            _completeness = evaluationForm.cleaned_data['completeness']
            _generalQuality = evaluationForm.cleaned_data['generalQuality']
            _commentText = evaluationForm.cleaned_data['commentText']
            _commentFeedback = evaluationForm.cleaned_data['commentFeedback']
            appraisal = Appraisal.objects.get(pk=request.POST['evaluadorAppraisal_id'])
            appraiser = User.objects.get(pk=request.POST['evaluador_id'])
            evaluation, created = AppraisalEvaluation.objects.update_or_create(
                                    appraisal=appraisal,
                                    user=appraiser,
                                    onTime=_onTime,
                                    completeness=_completeness,
                                    generalQuality=_generalQuality,
                                    commentText=_commentText,
                                    commentFeedback=_commentFeedback)

            print(evaluation.appraisalEvaluationMean)


    appraisals_active, appraisals_finished = userAppraisals(request)
    print(appraisals_finished)
    evaluationForm = EvaluationForm()
    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    visadores = list(User.objects.filter(groups__name__in=['visador']))
    lista = appraiserWork(tasadores)
    context = {'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished, 'evaluationForm': evaluationForm, 'lista':lista,
                'tasadores': tasadores,'visadores': visadores,}
    return render(request, 'appraiser_evaluation.html', context)
