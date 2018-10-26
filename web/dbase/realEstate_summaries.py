#!/usr/bin/env python
'''
Script to add summary variables to geografic places, such as the number of
real estate in each sector.
'''
from tools import *
from globals import *
from output import *

# Importing DJANGO things
import sys
import os
import django
sys.path.append('/Users/nico/Code/tasador/web/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

# Models
from region.models import Region
from commune.models import Commune
from realestate.models import RealEstate
from building.models import Building
from apartment.models import Apartment
from house.models import House

def countApartments(region,out):
    apts = Apartment.objects.filter(addressRegion=region)
    region.dataApartmentCount = len(apts)
    out.info('Region: {} {}'.format(region.name,region.dataApartmentCount))
    region.save()

    communes = Commune.objects.filter(region=region)
    for commune in communes:
        commune.dataApartmentCount = len(apts.filter(addressCommune=commune))
        out.info('Commune: {} {}'.format(commune.name,commune.dataApartmentCount))
        commune.save()

def countHouses(region,out):
    hss = House.objects.filter(addressRegion=region)
    region.dataHouseCount = len(hss)
    out.info('Region: {} {}'.format(region.name,region.dataHouseCount))
    region.save()

    communes = Commune.objects.filter(region=region)
    for commune in communes:
        commune.dataHouseCount = len(hss.filter(addressCommune=commune))
        out.info('Commune: {} {}'.format(commune.name,commune.dataHouseCount))
        commune.save()

if __name__ == "__main__":
    out = Messenger()
    regions = Region.objects.filter(code=13)
    for region in regions:
        countApartments(region,out)
        countHouses(region,out)
