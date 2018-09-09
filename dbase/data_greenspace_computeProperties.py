#!/usr/bin/env python
from pathlib import Path # nice way to manage paths
import glob
import shapefile # read shapes
import geojson # write geojson
from slugify import slugify # for nice filenames
from subprocess import call
import json
import collections
import os
import sys
sys.path.append('.')
from data_globals import *
from tools import *

def addCoordinates(filepath):
    print(filepath[-40:])

    file = open(filepath,'r')
    commune = json.load(file)
    file.close()

    for sections in commune['geometry']['coordinates']:
        if (len(sections) == 1):
            print('wut')
            continue
        center = polygonCenter(sections)
        commune['properties']['center'] = center

    file = open(filepath,'w')
    file.write(geojson.dumps(commune, sort_keys=True))
    file.close()

def addArea(filepath):
    print(filepath[-40:])

    file = open(filepath,'r')
    commune = json.load(file)
    file.close()

    for sections in commune['geometry']['coordinates']:
        print('sections',sections)
        if (len(sections) == 1):
            print('wut')
            continue
        center = polygonArea(sections)
        commune['properties']['area'] = center

    file = open(filepath,'w')
    file.write(geojson.dumps(commune, sort_keys=True))
    file.close()

path = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/areasverde/json/metropolitana-de-santiago/'
files = glob.glob(path+'*')
for file in files:
    addCoordinates(file)
    addArea(file)
