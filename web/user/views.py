from appraisal.models import Appraisal
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User, Group
from .forms import EditProfileForm, UserForm
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

from region.models import Region
from commune.models import Commune


@login_required(login_url='user/login')
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        userprofile = UserProfile.objects.get(pk=pk)
    else:
        user = request.user
        userprofile = UserProfile.objects.get(user=request.user)

    context = {'user': user, 'userprofile': userprofile}
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
        #user_form = UserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=user)
        #if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            #user_form.save()
            profile_form.save()
            #_first_name = user_form.cleaned_data['first_name']
            #_last_name = user_form.cleaned_data['last_name']
            #_email = user_form.cleaned_data['email']
            _first_name = profile_form.cleaned_data['first_name']
            _last_name = profile_form.cleaned_data['last_name']
            _email = profile_form.cleaned_data['email']
            _addressRegion = profile_form.cleaned_data['addressRegion']
            _addressCommune = profile_form.cleaned_data['addressCommune']
            _addressStreet = profile_form.cleaned_data['addressStreet']
            _addressNumber = profile_form.cleaned_data['addressNumber']
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
            print('error')
    else:
        #user_form = UserForm(instance=request.user)
        profile_form = EditProfileForm(instance=user)

    return render(request, 'user/profile_edit.html', {
        #'user_form': user_form,
        'profile_form': profile_form
    })


@login_required(login_url='user/login')
def userAppraisals(request):
    try:
        if request.user.groups.values_list('name',flat=True)[0]=='tasador':
            appraisals_active = Appraisal.objects.filter(tasadorUser=request.user).filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = Appraisal.objects.filter(tasadorUser=request.user).filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
        elif request.user.groups.values_list('name',flat=True)[0]=='visador':
            appraisals_active = Appraisal.objects.filter(visadorUser=request.user).filter(
                state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = Appraisal.objects.filter(visadorUser=request.user).filter(
                state=Appraisal.STATE_FINISHED).order_by('timeCreated')
        else:
            appraisals_active = Appraisal.objects.filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
            appraisals_finished = Appraisal.objects.filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
    except IndexError:
        appraisals_active = Appraisal.objects.filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
        appraisals_finished = Appraisal.objects.filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')

    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished}
    return render(request, 'user/index.html', context)

@login_required(login_url='user/login')
def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})

