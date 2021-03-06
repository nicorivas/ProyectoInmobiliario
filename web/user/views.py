from appraisal.models import Appraisal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .forms import EditProfileForm, AuthenticationFormB, PasswordResetForm

from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

from region.models import Region
from commune.models import Commune

import datetime

import reversion
from copy import deepcopy
from reversion.models import Version

from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
#from django.contrib.auth.forms import (
#    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
#)
from django.views.generic.edit import FormView


@login_required(login_url='user/login')
def userAppraisals(request):
    apps = Appraisal.objects.defer('photos')
    try:
        if request.user.groups.values_list('name', flat=True)[0]=='tasador':
            appraisals = apps.filter(tasadorUser=request.user)
        elif request.user.groups.values_list('name',flat=True)[0]=='visador':
            appraisals = apps.filter(visadorUser=request.user)
        else:
            appraisals = apps.all()
    except IndexError:
        appraisals = apps.all()

    appraisals_not_assigned = appraisals.filter(state=Appraisal.STATE_NOT_ASSIGNED).order_by('timeCreated')
    appraisals_active = appraisals.filter(state=Appraisal.STATE_IN_APPRAISAL).order_by('timeCreated')
    appraisals_finished = appraisals.filter(state=Appraisal.STATE_SENT).order_by('timeCreated')
    return [appraisals_not_assigned, appraisals_active, appraisals_finished]

def save_appraisalNF(appraisal, request, comment):
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
    for user in tasadores:
        activeAppraisals = Appraisal.objects.filter(tasadorUser=user)
        try:
            lateAppraisals = [x for x in activeAppraisals if x.daysLeft and x.daysLeft <= 0]
            doneAppraisals = [x for x in activeAppraisals if x.state == Appraisal.STATE_FINISHED]
        except AttributeError:
            continue
        list.append({'user': user, 'activeAppraisals':len(activeAppraisals),
                      'lateAppraisals':len(lateAppraisals), 'doneAppraisals' : len(doneAppraisals)})
    return list

def visadorWork(visadores):
    list = []
    for users in visadores:
        try:
            activeAppraisals = Appraisal.objects.filter(visadorUser=users)
            lateAppraisals = [x for x in activeAppraisals if x.daysLeft <= 0]
            doneAppraisals = [x for x in activeAppraisals if x.state == Appraisal.STATE_FINISHED]
        except AttributeError:
            continue
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
            ret = assign_tasadorNF(request)
        if 'btn_assign_visador' in request.POST.keys():
            ret = assign_visadorNF(request)

    if pk:
        user = User.objects.get(pk=pk)
        userprofile = UserProfile.objects.get(pk=pk)
    else:
        user = request.user
        userprofile = UserProfile.objects.get(user=request.user)

    appraisals_not_assigned, appraisals_active, appraisals_finished = userAppraisals(request)
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
            '''
            '''
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

class PasswordResetView(FormView):
    email_template_name = 'user/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'user/password_reset_form.html'
    #title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)