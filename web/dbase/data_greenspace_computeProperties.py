#!/usr/bin/env python
from pathlib import Path # nice way to manage paths
import glob
import shapefile # read shapes
import geojson # write geojson
from slugify import slugify # for nice filenames
from subprocess import call
import json
import collections
import itertools
import os
import sys
sys.path.append('.')
from data_globals import *
from tools import *

def addCoordinates(filepath):
    #print(filepath[-40:])

    file = open(filepath,'r')
    try:
        commune = json.load(file)
    except json.decoder.JSONDecodeError:
        print('empty file?')
        return False

    file.close()

    for sections in commune['geometry']['coordinates']:
        sections = np.array(sections)
        if len(sections.shape) == 1:
            center = np.zeros(2)
            for section in sections:
                section = np.array(section)
                center += polygonCenter(section)
            center = center/len(sections)
        elif len(sections.shape) == 3:
            if sections.shape[0] == 1:
                section = sections[0]
                center = polygonCenter(section)
        else:
            center = polygonCenter(sections)
        commune['properties']['center'] = center

    file = open(filepath,'w')
    file.write(geojson.dumps(commune, sort_keys=True))
    file.close()

def addArea(filepath):
    #print(filepath[-40:])

    file = open(filepath,'r')
    try:
        commune = json.load(file)
    except json.decoder.JSONDecodeError:
        print('empty file?')
        return False

    file.close()

    coords = getPolygonCoordinates(commune)
    area = 0
    for c in coords:
        area += polygonArea(c)
    commune['properties']['area'] = area

    file = open(filepath,'w')
    file.write(geojson.dumps(commune, sort_keys=True))
    file.close()

path = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/areasverde/json/metropolitana-de-santiago/'
files = glob.glob(path+'*')
for file in files:
    #addCoordinates(file)
    addArea(file)
