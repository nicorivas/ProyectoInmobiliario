from appraisal.models import Appraisal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .forms import EditProfileForm, AuthenticationFormB

from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

from region.models import Region
from commune.models import Commune

import datetime

import reversion
from copy import deepcopy
from reversion.models import Version

@login_required(login_url='user/login')
def userAppraisals(request):
    apps = Appraisal.objects.defer('photos')
    try:
        if request.user.groups.values_list('name', flat=True)[0]=='tasador':
            appraisals_active = apps.filter(tasadorUser=request.user).filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = apps.filter(tasadorUser=request.user).filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
        elif request.user.groups.values_list('name',flat=True)[0]=='visador':
            appraisals_active = apps.filter(visadorUser=request.user).filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = apps.filter(visadorUser=request.user).filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
        else:
            appraisals_active = apps.filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = apps.filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
    except IndexError:
        appraisals_active = apps.filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
        appraisals_finished = apps.filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
    return [appraisals_active, appraisals_finished]

def save_appraisalNF(appraisal, request, comment):
    print('save_appraisal')
    with reversion.create_revision():
        appraisal.save()
        reversion.set_user(request.user)
        reversion.set_comment(comment)
        return

def assign_visadorNF(request):
    appraisal = Appraisal.objects.get(pk=request.POST.dict()['visadorAppraisal_id'])
    appraisal.visadorUser = User.objects.get(pk=request.POST.dict()['visador'])
    save_appraisalNF(appraisal, request,'Changed visador')
    return

def assign_tasadorNF(request):
    appraisal = Appraisal.objects.get(pk=request.POST.dict()['tasadorAppraisal_id'])
    appraisal.tasadorUser = User.objects.get(pk=request.POST.dict()['tasador'])
    save_appraisalNF(appraisal, request,'Changed tasador')
    return

def appraiserWork(tasadores):
    list = []
    for users in tasadores:
        activeAppraisals = Appraisal.objects.filter(tasadorUser=users)
        lateAppraisals = [x for x in activeAppraisals if x.daysLeft <= 0]
        doneAppraisals = [x for x in activeAppraisals if x.state == Appraisal.STATE_FINISHED]
        list.append({'user': users, 'activeAppraisals':len(activeAppraisals),
                      'lateAppraisals':len(lateAppraisals), 'doneAppraisals' : len(doneAppraisals)})
    return list

def visadorWork(visadores):
    list = []
    for users in visadores:
        activeAppraisals = Appraisal.objects.filter(visadorUser=users)
        lateAppraisals = [x for x in activeAppraisals if x.daysLeft <= 0]
        doneAppraisals = [x for x in activeAppraisals if x.state == Appraisal.STATE_FINISHED]
        list.append({'user': users, 'activeAppraisals':len(activeAppraisals),
                      'lateAppraisals':len(lateAppraisals), 'doneAppraisals' : len(doneAppraisals)})
    return list


@login_required(login_url='user/login')
def view_profile(request, pk=None):

    if request.method == 'POST':
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

    if pk:
        user = User.objects.get(pk=pk)
        userprofile = UserProfile.objects.get(pk=pk)
    else:
        user = request.user
        userprofile = UserProfile.objects.get(user=request.user)

    appraisals_active, appraisals_finished = userAppraisals(request)
    tasadores = list(User.objects.filter(groups__name__in=['tasador']))
    visadores = list(User.objects.filter(groups__name__in=['visador']))
    lista = appraiserWork(tasadores)
    context = {'user': user, 'userprofile': userprofile, 'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished, 'tasadores': tasadores, 'visadores': visadores, 'lista': lista}
    return render(request, 'user/profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    try:
        user = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user = UserProfile.objects.create(user=request.user, first_name=request.user.first_name,
                                          last_name=request.user.last_name, email=request.user.email)
    if request.method == 'POST':
        form_profile = EditProfileForm(request.POST, instance=user)
        if form_profile.is_valid():
            form_profile.save()
            _first_name = form_profile.cleaned_data['first_name']
            _last_name = form_profile.cleaned_data['last_name']
            _email = form_profile.cleaned_data['email']
            _addressRegion = form_profile.cleaned_data['addressRegion']
            _addressCommune = form_profile.cleaned_data['addressCommune']
            _addressStreet = form_profile.cleaned_data['addressStreet']
            _addressNumber = form_profile.cleaned_data['addressNumber']
            UserProfile.objects.filter(user=request.user).update(first_name=_first_name,
                                                                 last_name=_last_name,
                                                                 email=_email,
                                                                 addressRegion=_addressRegion,
                                                                 addressCommune=_addressCommune,
                                                                 addressStreet=_addressStreet,
                                                                 addressNumber=_addressNumber)
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('user:profile')
        else:
            #messages.error(request, _('Please correct the error below.'))
            print(form_profile.errors)
    else:
        form_profile = EditProfileForm(instance=user)
        form_profile.fields['addressRegion'].initial = 13
        communes = Commune.objects.only('name').filter(region=13).order_by('name')
        form_profile.fields['addressCommune'].queryset = communes

    return render(request, 'user/profile_edit.html', {'form_profile': form_profile})



@login_required(login_url='user/login')
def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})

def login(request):
    form_login = AuthenticationFormB()
    context = {'form_login':form_login}
    return render(request,'user/login.html',context)



