from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from data.chile import comunas_regiones
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
#from django.contrib.contenttypes.models import ContentType


from .forms import LocationSearchForm
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

def appraisal_create(property,appraisalTimeFrame):
    '''
    Create appraisal, given a ...?
    '''
    timeDue = appraisalTimeFrame
    appraisal = Appraisal(
        apartment=property,
        propertyType=property.propertyType,
        timeCreated=datetime.datetime.now(),
        timeDue=timeDue)
    appraisal.save()
    return appraisal

def apartment_create(building,addressNumberFlat):
    '''
    Given a building and a flat number, create an apartment.
    '''
    apartment = Apartment(
        addressRegion=building.addressRegion,
        addressCommune=building.addressCommune,
        addressStreet=building.addressStreet,
        addressNumber=building.addressNumber,
        building=building,
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



@login_required(login_url='/')
def create(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_create = AppraisalCreateForm(request.POST)
        # check whether it's valid:
        if form_create.is_valid():

            _propertyType = int(form_create.cleaned_data['propertyType_create'])

            if _propertyType == RealEstate.TYPE_HOUSE:

                _addressRegion = form_create.cleaned_data['addressRegion_create']
                _addressCommune = form_create.cleaned_data['addressCommune_create']
                _addressStreet = form_create.cleaned_data['addressStreet_create']
                _addressNumber = form_create.cleaned_data['addressNumber_create']
                _appraisalTimeFrame = form_create.cleaned_data['appraisalTimeFrame_create']
                # check if house exists
                house = None
                try:
                    house = House.objects.get(
                        addressCommune=_addressCommune,
                        addressNumber=_addressNumber,
                        addressRegion=_addressRegion,
                        addressStreet=_addressStreet)
                except House.DoesNotExist:
                    # flat does not exist, so create it
                    house = house_create(_addressRegion,_addressCommune,_addressStreet,_addressNumber)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'House is repeated'}
                    return render(request, 'create/error.html', context)

                # go to appraisal url
                return HttpResponseRedirect(appraisal.url)

            elif _propertyType == RealEstate.TYPE_BUILDING:

                context = {'error_message': 'Cannot create buildings yet'}
                return render(request, 'create/error.html',context)

            elif _propertyType == RealEstate.TYPE_APARTMENT:

                _addressRegion = form_create.cleaned_data['addressRegion_create']
                _addressCommune = form_create.cleaned_data['addressCommune_create']
                _addressStreet = form_create.cleaned_data['addressStreet_create']
                _addressNumber = form_create.cleaned_data['addressNumber_create']
                _addressNumberFlat = form_create.cleaned_data['addressNumberFlat_create']
                _appraisalTimeFrame = form_create.cleaned_data['appraisalTimeFrame_create']
                # check if building exists
                building = None
                try:
                    building = Building.objects.get(
                        addressRegion=_addressRegion,
                        addressCommune=_addressCommune,
                        addressStreet=_addressStreet,
                        addressNumber=_addressNumber)
                except Building.DoesNotExist:
                    # building does not exist, so create it
                    building = building_create(_addressRegion,_addressCommune,_addressStreet,_addressNumber)
                except MultipleObjectsReturned:
                    context = {'error_message': 'Building is repeated'}
                    return render(request, 'create/error.html',context)

                # check if flat exists
                realestate = None
                try:
                    realestate = RealEstate.objects.get(
                        building=building,
                        number=_addressNumberFlat)
                except RealEstate.DoesNotExist:
                    # flat does not exist, so create it
                    realestate = realestate_create(building,_addressNumberFlat)
                except MultipleObjectsReturned:
                    # error
                    context = {'error_message': 'Real estate is repeated'}
                    return render(request, 'create/error.html',context)

            # create new appraisal
            try:
                appraisal = Appraisal.objects.get(realestate=realestate) #ver cómo chequear la existencia de un appraisal
            except Appraisal.DoesNotExist:
                appraisal = appraisal_create(house, _appraisalTimeFrame)
            except MultipleObjectsReturned:
                context = {'error_message': 'More than one appraisal of the same property'}
                return render(request, 'create/error.html', context)

            # go to appraisal url
            return HttpResponseRedirect(appraisal.url)
        else:
            print(form_create.errors)

        context = {'form_create':form_create}

    else:

        # SEARCH FORM

        form_search = LocationSearchForm

        # IF WE HAVE AN ADDRESS

        address = request.GET.get('address', '')

        addressStreet = ''
        addressNumber = 0
        addressRegion = 13

        if address != '':

            # GET DATA FROM GOOGLE API

            url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            url_address = 'address={}'.format(address)
            url_key = '&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
            url_language = '&language=es'
            response = requests.get(url+''+url_address+''+url_key+''+url_language)
            response_json = response.json()
            response_results = response_json['results']

            addressNumber = ''
            addressStreet = ''
            addressCommune = ''
            addressRegion = ''
            addressCountry = ''

            for address_component in response_results[0]['address_components']:
                types = address_component['types']
                if 'street_number' in types:
                    addressNumber = address_component['long_name']
                if 'route' in types:
                    addressStreet = address_component['short_name']
                if 'locality' in types:
                    addressCommune = address_component['long_name']
                if 'administrative_area_level_1' in types:
                    addressRegion = address_component['long_name']
                if 'country' in types:
                    addressCountry = address_component['long_name']

            region_name = (addressRegion.split('Región')[1]).strip()
            region = Region.objects.get(name__icontains=region_name)
            commune = Commune.objects.get(name__icontains=addressCommune)

        else:

            region = Region.objects.get(code=addressRegion)
            commune = Commune.objects.get(name__icontains='Providencia')

        form_create = AppraisalCreateForm(
            initial={
                'addressStreet_create':addressStreet,
                'addressNumber_create':addressNumber,
                'addressRegion_create':region,
                },label_suffix='')

        communes = Commune.objects.filter(region=region.code).order_by('name')

        form_create.fields['addressCommune_create'].queryset = communes
        form_create.fields['addressCommune_create'].initial = commune

        # Get buildings to be displayed on map
        buildings = Building.objects.all()
        buildings_json = serializers.serialize("json", Building.objects.all())

        # Get houses to be displayed on map
        houses = House.objects.all()
        houses_json = serializers.serialize("json", House.objects.all())

        context = {
            #'buildings':buildings,
            'buildings_json':buildings_json,
            'houses_json':houses_json,
            'form_search':form_search,
            'form_create':form_create}

    return render(request, 'create/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})
