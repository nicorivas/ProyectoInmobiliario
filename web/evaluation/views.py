from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.views import userAppraisals, appraiserWork, assign_visadorNF, assign_tasadorNF
from appraisal.models import AppraisalEvaluation, Appraisal
from .forms import EvaluationForm

from django.core.exceptions import ObjectDoesNotExist

def get_appraisalEvaluations(request):
    try:
        appraisalEvaluation = AppraisalEvaluation.objects.get(pk=request.POST['evaluadorAppraisal_id'])
        evaluationForm = EvaluationForm(instance=appraisalEvaluation)
        print(appraisalEvaluation.appraisalEvaluationMean)
        return evaluationForm
    except AppraisalEvaluation.DoesNotExist:
        return "Zooom"


def appraiserEvaluationView(request):
    evaluationForm = EvaluationForm()
    if request.method == 'POST':
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
                                            #user=appraiser,
                                            defaults={
                                                "appraisal":appraisal,
                                                'user':appraiser,
                                                'onTime':_onTime,
                                                'completeness':_completeness,
                                                'generalQuality':_generalQuality,
                                                'commentText':_commentText,
                                                'commentFeedback':_commentFeedback})

                    print(evaluation, created)
                    print(evaluation.appraisalEvaluationMean)


    appraisals_active, appraisals_finished = userAppraisals(request)
    for i in appraisals_finished: #Asegurarse de que toda tasación tenga una evaluación
        try:
            x = AppraisalEvaluation.objects.get(appraisal=i)
        except AppraisalEvaluation.DoesNotExist:
            x = AppraisalEvaluation(appraisal=i)
            x.save()

    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    visadores = list(User.objects.filter(groups__name__in=['visador']))
    lista = appraiserWork(tasadores)
    context = {'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished, 'evaluationForm': evaluationForm, 'lista':lista,
                'tasadores': tasadores,'visadores': visadores,}
    return render(request, 'appraiser_evaluation.html', context)
