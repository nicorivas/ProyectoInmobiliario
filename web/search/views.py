from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from data.chile import comunas_regiones
from django.http import HttpResponseRedirect
from django.utils.text import slugify

from .forms import LocationSearchForm
from .forms import AppraisalCreateForm

from building.models import Building
from apartment.models import Apartment
from appraisal.models import Appraisal

import datetime


import requests # to call the API of Google to get lat-lon

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
                buildingId = int(Building.objects.all().order_by('-id')[0].id)+1
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
                appraisal = Appraisal(apartment=apartment,timeCreated=datetime.datetime.now())
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
        address = request.GET.get('address', '')
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        url_address = 'address={}'.format(address)
        response = requests.get(url+''+url_address)
        response_json = response.json()
        response_results = response_json['results']

        addressNumber = ''
        addressStreet = ''
        addressCommune = ''
        addressRegion = ''
        addressCountry = ''

        # CREATE APPRAISAL FORM

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

        #print(resp_json_payload['results'][0]['formatted_address'])

        region_name = ''
        region_id = 0

        for region in comunas_regiones.regiones:
            if region[0].find(addressRegion) >= 0:
                region = region[0]

        form_create = AppraisalCreateForm(
            initial={
                'addressStreet_create':addressStreet,
                'addressNumber_create':addressNumber,
                'addressRegion_create':region,
                })
        form_create.fields['addressCommune_create'].choices = [(a,a) for a in comunas_regiones.regiones_comunas[region]]
        form_create.fields['addressCommune_create'].initial = addressCommune

        # Get buildings to be displayed on map
        buildings = Building.objects.all()
        buildings_json = serializers.serialize("json", Building.objects.all())

        context = {
            'buildings':buildings,
            'buildings_json':buildings_json,
            'form_search':form_search,
            'form_create':form_create}

    return render(request, 'search/index.html', context)

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = comunas_regiones.regiones[region_id]
    communes = comunas_regiones.regiones_comunas[region[1]]
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': enumerate(communes)})
