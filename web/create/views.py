from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from .forms import AppraisalCreateForm

from region.models import Region
from commune.models import Commune

from realestate.models import RealEstate
from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal
from . import create

import datetime

import requests # to call the API of Google to get lat-lon
import reversion # to save the first version when creating an appraisal

@login_required(login_url='/user/login')
def view_create(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form_create = AppraisalCreateForm(request.POST)
        # check whether it's valid:
        if form_create.is_valid():

            propertyType = int(form_create.cleaned_data['propertyType_create'])
            cliente = form_create.cleaned_data['cliente_create']
            clienteRut = form_create.cleaned_data['clienteRut_create']
            solicitanteCodigo = form_create.cleaned_data['solicitanteCodigo_create']
            tipoTasacion = form_create.cleaned_data['tipoTasacion_create']
            objetivo = form_create.cleaned_data['objetivo_create']
            visita = form_create.cleaned_data['visita_create']

            if form_create.cleaned_data['solicitante_create'] == "0":
                solicitante = form_create.cleaned_data['solicitanteOther_create']
            else:
                solicitante = form_create.cleaned_data['solicitante_create']


            realEstate = None
            if propertyType == RealEstate.TYPE_HOUSE:

                addressRegion = form_create.cleaned_data['addressRegion_create']
                addressCommune = form_create.cleaned_data['addressCommune_create']
                addressStreet = form_create.cleaned_data['addressStreet_create']
                addressNumber = form_create.cleaned_data['addressNumber_create']
                addressNumber2 = form_create.cleaned_data['addressNumber2_create']
                # check if house exists
                try:
                    realEstate = House.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        addressNumber2=addressNumber2)
                except House.DoesNotExist:
                    # house does not exist, so create it
                    realEstate = create.house_create(addressRegion,addressCommune,addressStreet,addressNumber,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'House is repeated'}
                    return render(request, 'create/error.html', context)

            elif propertyType == RealEstate.TYPE_BUILDING:

                context = {'error_message': 'Cannot create buildings yet'}
                return render(request, 'create/error.html',context)

            elif propertyType == RealEstate.TYPE_APARTMENT:

                addressRegion = form_create.cleaned_data['addressRegion_create']
                addressCommune = form_create.cleaned_data['addressCommune_create']
                addressStreet = form_create.cleaned_data['addressStreet_create']
                addressNumber = form_create.cleaned_data['addressNumber_create']
                addressNumber2 = form_create.cleaned_data['addressNumber2_create']

                # check if building exists
                building = None
                try:
                    building = Building.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        propertyType=RealEstate.TYPE_BUILDING)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = create.building_create(addressRegion,addressCommune,addressStreet,addressNumber)
                except MultipleObjectsReturned:
                    context = {'error_message': 'Building is repeated'}
                    return render(request, 'create/error.html',context)

                # check if flat exists
                realEstate = None
                try:
                    realEstate = Apartment.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber,
                        addressNumber2=addressNumber2,
                        propertyType=RealEstate.TYPE_APARTMENT)
                except Apartment.DoesNotExist:
                    # flat does not exist, so create it
                    realEstate = create.apartment_create(building,addressNumber2)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Apartment is repeated'}
                    return render(request, 'create/error.html',context)

            # create new appraisal
            #appraisalPrice = form_create.cleaned_data['appraisalPrice_create']
            appraisalPrice = None
            appraisalTimeFrame = form_create.cleaned_data['appraisalTimeFrame_create']
            
            # ToDO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
            appraisal = create.appraisal_create(realEstate.realestate_ptr, appraisalTimeFrame, request.user, solicitante,
                        solicitanteCodigo, cliente, clienteRut, tipoTasacion, objetivo, visita, appraisalPrice)

            # go to appraisal url
            return HttpResponseRedirect(appraisal.url)
        else:
            errordata = form_create.errors.as_data()
            message = {'error_message':'Validation Error, for now is price appraisal'}
            context = {'form_create': form_create, 'message': message}
            if '__all__' in errordata.keys():
                message = errordata['__all__'][0].message
            else:
                message = ""
            context = {'form_create':form_create,'message':message}            
            return render(request, 'create/error.html', context)

    else:

        address = request.GET.get('address', '')

        region = Region.objects.only('name','code').get(code=13)

        # Sort communes
        communes = Commune.objects.only('name').filter(region=13).order_by('name')
        commune = Commune.objects.only('name').get(name__icontains='Providencia')

        # Set initial values
        form_create_initial = {'addressRegion_create':region}
        form_create = AppraisalCreateForm({'addressRegion_create':13},label_suffix='')
        form_create.fields['addressCommune_create'].queryset = communes
        form_create.fields['addressCommune_create'].initial = commune

        context = {'form_create': form_create}

        return render(request, 'create/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})
