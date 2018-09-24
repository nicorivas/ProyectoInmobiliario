from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from data.chile import comunas_regiones
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from .forms import LocationSearchForm
from .forms import AppraisalCreateForm

from region.models import Region
from commune.models import Commune

from house.models import House
from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal

import datetime


import requests # to call the API of Google to get lat-lon

@login_required(login_url='/')
def search(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_create = AppraisalCreateForm(request.POST)
        # check whether it's valid:
        if form_create.is_valid():

            _addressRegion = form_create.cleaned_data['addressRegion_create']
            _addressCommune = form_create.cleaned_data['addressCommune_create']
            _addressStreet = form_create.cleaned_data['addressStreet_create']
            _addressNumber = form_create.cleaned_data['addressNumber_create']
            _addressNumberFlat = form_create.cleaned_data['addressNumberFlat_create']
            _appraisalTimeFrame = form_create.cleaned_data['appraisalTimeFrame_create']


            # check if building exists
            buildings = Building.objects.filter(
                addressRegion=_addressRegion,
                addressCommune=_addressCommune,
                addressStreet=_addressStreet,
                addressNumber=_addressNumber)

            if len(buildings) == 0:
                # building does not exist, so create it
                building = Building(
                    addressRegion=_addressRegion,
                    addressCommune=_addressCommune,
                    addressStreet=_addressStreet,
                    addressNumber=_addressNumber)
                # save to database
                if len(Building.objects.all()) > 0:
                    buildingId = int(Building.objects.all().order_by('-id')[0].id)+1
                else:
                    buildingId = 1
                # get lat lon

                url = 'https://maps.googleapis.com/maps/api/geocode/json?'
                url_address = 'address={} {}, {}, {}'.format(_addressStreet,_addressNumber,_addressCommune,_addressRegion)
                response = requests.get(url+''+url_address)
                response_json = response.json()
                print(response_json)
                response_results = response_json['results'][0]['geometry']['location']
                building.lat = response_results['lat']
                building.lon = response_results['lng']

                building.id = buildingId
                building.save()
            elif len(buildings) > 1:
                # there is more than one building, error
                context = {'error_message': 'Building is repeated'}
                return render(request, 'search/error.html',context)
            else:
                building = buildings[0]
                buildingId = building.id

            # check if flat exists
            apartment = Apartment.objects.filter(
                building=building,
                number=_addressNumberFlat)
            if len(apartment) == 0:
                apartment = Apartment(
                    building=building,
                    number=_addressNumberFlat)
                apartments = Apartment.objects.all()
                if len(apartments) == 0:
                    apartmentId = 1
                else:
                    apartmentId = int(apartments.order_by('-id')[0].id)+1
                apartment.id = apartmentId
                apartment.save()
            elif len(apartment) > 1:
                # error
                context = {'error_message': 'Apartment is repeated'}
                return render(request, 'search/error.html',context)
            else:
                apartment = apartment[0]
                apartmentId = apartment.id

            # create new appraisal
            appraisal = Appraisal.objects.filter(
                apartment=apartment)
            if len(appraisal) == 0:
                timeDue = datetime.now() + timedelta(_appraisalTimeFrame)
                print(timeDue)
                appraisal = Appraisal(apartment=apartment,timeCreated=datetime.datetime.now(), timeDue=timeDue)
                appraisal.save()
            elif len(appraisal) > 1:
                context = {'error_message': 'More than one appraisal of the same property'}
                return render(request, 'search/error.html',context)
            else:
                appraisal = appraisal[0]
            appraisalId = appraisal.id

            # go to appraisal url
            return HttpResponseRedirect('/appraisal/{}/{}/{}/{}/{}/departamento/{}/{}/{}/'.format(
                slugify(_addressRegion),slugify(_addressCommune),
                slugify(_addressStreet),slugify(_addressNumber),
                slugify(buildingId),slugify(_addressNumberFlat),
                slugify(apartmentId),slugify(appraisalId)
            ))
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

    return render(request, 'search/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})

def apt_block(request):
    if str(request.GET.get('type')) == 'c':
        return render(request, 'hr/house_selected_option.html')
    else:
        return HttpResponse('')