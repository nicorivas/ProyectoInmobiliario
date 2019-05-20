#!/usr/bin/env python
'''
Script to add summary variables to geografic places, such as the number of
real estate in each sector.
'''
from tools import *
from globals import *
from output import *

# Importing DJANGO things
import unidecode
import sys
import os
import django
sys.path.append('/Users/nico/Code/tasador/web/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'map.settings'
django.setup()

# Models
from appraisal.models import Appraisal
from realestate.models import RealEstate
from commune.models import Commune

#apps = Appraisal.objects.all()
#for app in apps:
#    print(app)
#    app.property_main = app.appproperty_set.first()
#    app.save()

communes = Commune.objects.all()
for commune in communes:
    print(commune.name)
    commune.name_simple = unidecode.unidecode(commune.name)
    commune.save()
