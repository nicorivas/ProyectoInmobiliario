#!/usr/bin/env python
from tools import *
from globals import *

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

def countApartments(region):
    apts = Apartment.objects.filter(addressRegion=region)
    region.dataApartmentCount = len(apts)
    info('Region: {} {}'.format(region.name,region.dataApartmentCount))
    region.save()

    communes = Commune.objects.filter(region=region)
    for commune in communes:
        commune.dataApartmentCount = len(apts.filter(addressCommune=commune))
        info('Commune: {} {}'.format(commune.name,commune.dataApartmentCount))
        commune.save()

regions = Region.objects.all()
for region in regions:
    countApartments(region)
