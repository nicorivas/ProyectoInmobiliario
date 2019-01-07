from django.shortcuts import render
from appraisal.models import Appraisal
from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
import datetime

# Create your views here.

def getTimeFramedAppraisals(tasador, initial, end):
    tasador = int(tasador)
    if tasador==0:
        appraisals = Appraisal.objects.filter(timeFinished__range=[initial, end])
        print(appraisals)
        print('todos')
    else:
        appraisals = Appraisal.objects.filter(tasadorUser= tasador, timeFinished__range=[initial, end])
        print(appraisals)
        print(tasador)
    return appraisals


@login_required(login_url='/user/login')
def accountingView(request):
    if request.method == "POST":
        print(request.POST)
        tasador = request.POST['tasador']
        initial = datetime.datetime.strptime(request.POST['appraisalTimeRequest2'], '%d/%m/%Y %H:%M')
        end = datetime.datetime.strptime(request.POST['appraisalTimeRequest2'],'%d/%m/%Y %H:%M')
        appraisals = getTimeFramedAppraisals(tasador, initial, end)

    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    context = {'tasadores': tasadores}
    return render(request, 'accounting/accounting.html', context)