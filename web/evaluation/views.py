from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.views import userAppraisals, appraiserWork
from .forms import EvaluationForm

def appraiserEvaluationView(request):
    if request.method == 'POST':
        print(request)
        evaluationForm = EvaluationForm(request.Post, instance=user)
        if evaluationForm.is_valid():
            evaluationForm.save()
            _onTime = evaluationForm.cleaned_data['onTime']
            _completeness = evaluationForm.cleaned_data['completeness']
            _generalQuality = evaluationForm.cleaned_data['generalQuality']
            _commentText = evaluationForm.cleaned_data['commentText']
            _commentFeedback = evaluationForm.cleaned_data['commentFeedback']

    appraisals_active, appraisals_finished = userAppraisals(request)
    evaluationForm = EvaluationForm()
    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    visadores = list(User.objects.filter(groups__name__in=['visador']))
    lista = appraiserWork(tasadores)
    context = {'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished, 'evaluationForm': evaluationForm, 'lista':lista,
                'tasadores': tasadores,'visadores': visadores,}
    return render(request, 'appraiser_evaluation.html', context)
