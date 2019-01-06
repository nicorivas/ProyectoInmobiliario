from django.shortcuts import render
from appraisal.models import Appraisal
from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='/user/login')
def accountingView(request):
    if request.method == "GET":
        tasadores = list(User.objects.filter(groups__name__in=['tasador']))


    context = {'tasadores':tasadores}
    return render(request, 'accounting/accounting.html', context)