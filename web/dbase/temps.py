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
from appraisal.models import Appraisal
from realestate.models import RealEstate

apps = Appraisal.objects.all()
for app in apps:
    print(app)
    app.property_main = app.appproperty_set.first()
    app.save()