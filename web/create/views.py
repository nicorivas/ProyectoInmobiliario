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

import datetime

import requests # to call the API of Google to get lat-lon
import reversion # to save the first version when creating an appraisal

def appraisal_create(realEstate,timeFrame,user, solicitante, solicitanteCodigo, cliente, clienteRut, tipoTasacion,
                     objetivo,  visita, price):
    '''
    Create appraisal, given a ...?
    '''
    timeDue = timeFrame
    appraisal = Appraisal(
        realEstate=realEstate,
        timeCreated=datetime.datetime.now(),
        timeDue=timeDue,
        price=price,
        solicitante=solicitante,
        solicitanteCodigo=solicitanteCodigo,
        cliente=cliente,
        clienteRut=clienteRut,
        tipoTasacion=tipoTasacion,
        objetivo=objetivo,
        visita=visita)
    with reversion.create_revision():
        appraisal.save()
        reversion.set_user(user)
        reversion.set_comment('Created')
    return appraisal

def apartment_create(building_in,addressNumberFlat):
    '''
    Given a building and a flat number, create an apartment.
    '''
    apartment = Apartment(
        addressRegion=building_in.addressRegion,
        addressCommune=building_in.addressCommune,
        addressStreet=building_in.addressStreet,
        addressNumber=building_in.addressNumber,
        building_in=building_in,
        number=addressNumberFlat)
    apartments = Apartment.objects.all()
    if len(apartments) == 0:
        apartmentId = 1
    else:
        apartmentId = int(apartments.order_by('-id')[0].id)+1
    apartment.id = apartmentId
    apartment.propertyType = RealEstate.TYPE_APARTMENT
    apartment.save()
    return apartment

def building_create(addressRegion,addressCommune,addressStreet,addressNumber):
    '''
    Given an address, create a building
    '''
    building = Building(
        addressRegion=addressRegion,
        addressCommune=addressCommune,
        addressStreet=addressStreet,
        addressNumber=addressNumber)

    # get id
    if len(Building.objects.all()) > 0:
        buildingId = int(Building.objects.all().order_by('-id')[0].id)+1
    else:
        buildingId = 1
    building.propertyType = RealEstate.TYPE_BUILDING
    building.id = buildingId

    # get lat lon
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    url_address = '?address={} {}, {}, {}'.format(
        addressStreet,
        addressNumber,
        addressCommune,
        addressRegion)
    url_key = '&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_address+''+url_key)
    response_json = response.json()
    response_results = response_json['results'][0]['geometry']['location']
    building.lat = response_results['lat']
    building.lon = response_results['lng']
    building.save()
    
    return building

def house_create(addressRegion,addressCommune,addressStreet,addressNumber):
    '''
    Given an address, create a house
    '''
    house = House(
        addressRegion=addressRegion,
        addressCommune=addressCommune,
        addressStreet=addressStreet,
        addressNumber=addressNumber)

    # get id
    if len(House.objects.all()) > 0:
        houseId = int(House.objects.all().order_by('-id')[0].id)+1
    else:
        houseId = 1
    house.propertyType = RealEstate.TYPE_HOUSE
    house.id = houseId

    # get lat lon
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    url_address = '?address={} {}, {}, {}'.format(
        addressStreet,
        addressNumber,
        addressCommune,
        addressRegion)
    url_key = '&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_address+''+url_key)
    response_json = response.json()
    response_results = response_json['results'][0]['geometry']['location']
    house.lat = response_results['lat']
    house.lon = response_results['lng']

    house.save()
    return house

@login_required(login_url='/user/login')
def create(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print('request.POST',request.POST)
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

            print('propertyType',propertyType)

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
                # check if house exists
                try:
                    realEstate = House.objects.get(
                        addressCommune=addressCommune,
                        addressNumber=addressNumber,
                        addressRegion=addressRegion,
                        addressStreet=addressStreet)
                except House.DoesNotExist:
                    # house does not exist, so create it
                    realEstate = house_create(addressRegion,addressCommune,addressStreet,addressNumber)
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
                addressNumberFlat = form_create.cleaned_data['addressNumberFlat_create']
                # check if building exists
                building = None
                try:
                    building = Building.objects.get(
                        addressRegion=addressRegion,
                        addressCommune=addressCommune,
                        addressStreet=addressStreet,
                        addressNumber=addressNumber)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = building_create(addressRegion,addressCommune,addressStreet,addressNumber)
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
                        number=addressNumberFlat)
                except Apartment.DoesNotExist:
                    # flat does not exist, so create it
                    realEstate = apartment_create(building,addressNumberFlat)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Apartment is repeated'}
                    return render(request, 'create/error.html',context)

            # create new appraisal
            #appraisalPrice = form_create.cleaned_data['appraisalPrice_create']
            appraisalPrice = None
            appraisalTimeFrame = form_create.cleaned_data['appraisalTimeFrame_create']
            
            # ToDO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
            appraisal = appraisal_create(realEstate, appraisalTimeFrame, request.user, solicitante,
                        solicitanteCodigo, cliente, clienteRut, tipoTasacion, objetivo, visita, appraisalPrice)
            
            '''
            appraisal = None
            try:
                appraisal = Appraisal.objects.get(realEstate=realEstate) #ver cómo chequear la existencia de un appraisal
            except Appraisal.DoesNotExist:
                appraisal = appraisal_create(realEstate, appraisalTimeFrame, request.user, solicitante,
                        solicitanteCodigo, cliente, clienteRut, tipoTasacion, objetivo, appraisalPrice)
            except MultipleObjectsReturned:
                context = {'error_message': 'More than one appraisal of the same property'}
                return render(request, 'create/error.html', context)
            '''

            # go to appraisal url
            return HttpResponseRedirect(appraisal.url)
        else:
            errordata = form_create.errors.as_data()
            print(errordata)
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
