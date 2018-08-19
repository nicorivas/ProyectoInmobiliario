from django.shortcuts import render
from building.models import Building
from apartment.models import Apartment
from django.core import serializers

def building(request,region="",commune="",street="",number=0,id=0):
    '''
    '''
    # Get building to be displayed on map
    building = Building.objects.filter(id=id)

    # This must be only one building
    if len(building) == 0:
        context = {'error_message': 'No se encontró propiedad (por id)'}
        return render(request, 'property/error.html',context)
    elif len(building) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'property/error.html',context)

    building = building[0]
    apartments = building.apartment_set.all()
    context = {'building': building, 'apartments': apartments}
    return render(request, 'property/building.html',context)

def house(request,region="",commune="",street="",number=0,id=0):
    '''
    '''
    # Get building to be displayed on map
    building = Building.objects.filter(id=id)

    # This must be only one building
    if len(building) == 0:
        context = {'error_message': 'No se encontró propiedad (por id)'}
        return render(request, 'property/error.html',context)
    elif len(building) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'property/error.html',context)

    building = building[0]
    apartments = building.apartment_set.all()
    context = {'building': building, 'apartments': apartments}
    return render(request, 'property/building.html',context)

def apartment(request,region="",commune="",street="",number=0,id=0,floor=0,fnumber=0):
    '''
    '''
    # Get building to be displayed on map
    building = Building.objects.filter(id=id)

    # Error checks
    # This must be only one building
    if len(building) == 0:
        context = {'error_message': 'No se encontró propiedad (por id)'}
        return render(request, 'property/error.html',context)
    elif len(building) > 1:
        context = {'error_message': 'Se encontró más de una propiedad (error base!)'}
        return render(request, 'property/error.html',context)
    building=building[0]

    # Get apartment
    apartment = building.apartment_set.filter(floor=floor,number=fnumber)
    # Error checks
    # The apartment must exist
    if len(apartment) == 0:
        context = {'error_message': 'No se encontró departmento'}
        return render(request, 'property/error.html',context)
    elif len(apartment) > 1:
        context = {'error_message': 'Más de un departamento con mismo numero y piso'}
        return render(request, 'property/error.html',context)
    apartment = apartment[0]

    context = {'building': building, 'apartment': apartment}
    return render(request, 'property/apartment.html',context)
