import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()
from building.models import Building
from django.core.exceptions import ObjectDoesNotExist

def borrarConstruccionesSinPropiedad(propertyType):

    #Borra Construcciones que tengan un prepertyType, pero ningúna propiedad asociada

    if propertyType not in dict(Building.propertyType_choices):
        return "Tipo de propiedad no existe"

    buildings = Building.objects.filter(propertyType=propertyType)

    for building in buildings:
        try:
            if propertyType==Building.TYPE_CASA:
                dummy = building.house
            elif propertyType==Building.TYPE_DEPARTAMENTO:
                dummy = building.apartmentbuilding
            elif propertyType==Building.TYPE_TERRENO:
                dummy = building.terrain
            continue
        except ObjectDoesNotExist:
            print(building)
            print("borrado")
            building.delete()


borrarConstruccionesSinPropiedad(Building.TYPE_CASA)
borrarConstruccionesSinPropiedad(Building.TYPE_TERRENO)
borrarConstruccionesSinPropiedad(Building.TYPE_DEPARTAMENTO)