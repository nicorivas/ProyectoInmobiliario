from region.models import Region
from commune.models import Commune
from realestate.models import RealEstate
#from house.models import House
#from building.models import Building
#from apartment.models import Apartment
from appraisal.models import Appraisal, Comment, Rol, Photo
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render

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

def createRealEstate(**kwargs):
    '''
    Crea real estate, o devuelve uno si ya existe.
    Kwargs están abstraidos porque pueden haber distintos criterios de igualdad.
    En general se ocupan addressStreet, addressNumber, addressCommune y addressRegion.
    Es decir: NO PUEDEN HABER DOS REAL ESTATE CON LA MISMA DIRECCION.
    '''
    try:
        real_estate = RealEstate.objects.get(**kwargs)
        return False
    except RealEstate.DoesNotExist:
        real_estate = RealEstate(**kwargs)
        real_estate.save()
        return real_estate
    except MultipleObjectsReturned:
        return False

def createOrGetRealEstate(**kwargs):
    '''
    Crea real estate, o devuelve uno si ya existe.
    Kwargs están abstraidos porque pueden haber distintos criterios de igualdad.
    En general se ocupan addressStreet, addressNumber, addressCommune y addressRegion.
    Es decir: NO PUEDEN HABER DOS REAL ESTATE CON LA MISMA DIRECCION.
    '''
    try:
        real_estate = RealEstate.objects.get(**kwargs)
        return real_estate, True
    except RealEstate.DoesNotExist:
        real_estate = RealEstate(**kwargs)
        real_estate.save()
        return real_estate, False
    except MultipleObjectsReturned:
        real_estate = RealEstate.objects.filter(**kwargs)
        return real_estate.first(), False

def createAppraisal(request,real_estate,rol="",**kwargs):
    '''
    Crea appraisal. Lo más común es desde create/views.py, donde se explicitan los kwargs.
    # TODO: VER COMO CHECKEAR EXISTENCIA DE APPRAISAL
    '''
    appraisal = Appraisal(**kwargs)
    appraisal.state = Appraisal.STATE_NOTASSIGNED
    appraisal.timeCreated = datetime.datetime.now()
    appraisal.save()
    
    comment = Comment(
        event=Comment.EVENT_TASACION_INGRESADA,
        user=request.user,
        timeCreated=datetime.datetime.now(datetime.timezone.utc))
    comment.save()
    appraisal.comments.add(comment)
    appraisal.real_estates.add(real_estate)
    appraisal.photos.create(category=Photo.PHOTO_CATEGORY_EMPLAZAMIENTO,fixed=True)
    appraisal.photos.create(category=Photo.PHOTO_CATEGORY_ENTORNO,fixed=True)
    appraisal.photos.create(category=Photo.PHOTO_CATEGORY_FACHADA,fixed=True)
    appraisal.photos.create(category=Photo.PHOTO_CATEGORY_ESPACIOS_COMUNES,fixed=True)
    appraisal.save()
    
    return appraisal