from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.forms import EditProfileForm, AuthenticationFormB, EvaluationForm
from user.views import userAppraisals, appraiserWork

def appraiserEvaluationView(request):
    appraisals_active, appraisals_finished = userAppraisals(request)
    form_user = EvaluationForm()
    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    visadores = list(User.objects.filter(groups__name__in=['visador']))
    lista = appraiserWork(tasadores)
    context = {'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished, 'form_user':form_user, 'lista':lista, 'tasadores': tasadores,
               'visadores': visadores,}
    return render(request, 'appraiser_evaluation.html', context)
