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

def address_to_coordinates(address):
    '''
    Given an address (string that Google would understand)
    return coordinates in lat long
    '''
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url_address = 'address={}'.format(address)
    url_key='&key=AIzaSyDgwKrK7tfcd9kCtS9RKSBsM5wYkTuuc7E'
    response = requests.get(url+''+url_address+url_key)
    resp_json_payload = response.json()
    if len(resp_json_payload['results']) == 0:
        return False
    else:
        return [
            resp_json_payload['results'][0]['geometry']['location']['lat'],
            resp_json_payload['results'][0]['geometry']['location']['lng']
            ]

def appraisal_create(realEstate, timeFrame, user, solicitante, solicitanteCodigo, cliente, clienteRut, tipoTasacion,
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
    address = '{} {}, {}, {}'.format(addressStreet,addressNumber,addressCommune,addressRegion)
    latlng = address_to_coordinates(address)
    if not isinstance(latlng,type(False)):
        building.lat = latlng[0]
        building.lon = latlng[1]
    
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
    address = '{} {}, {}, {}'.format(addressStreet,addressNumber,addressCommune,addressRegion)
    latlng = address_to_coordinates(address)
    if not isinstance(latlng,type(False)):
        house.lat = latlng[0]
        house.lon = latlng[1]

    house.save()
    return house