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
import math
import matplotlib.pyplot as plt
sys.path.append('.')
from data_globals import *
from tools import *

def addCoordinates(filepath):
    print(filepath[-20:])

    file = open(filepath,'r')
    square = json.load(file)
    file.close()

    for sections in square['geometry']['coordinates']:
        if (len(sections) == 1):
            print('wut')
            continue
        center = polygonCenter(sections)
        square['properties']['center'] = center

    file = open(filepath,'w')
    file.write(geojson.dumps(square, sort_keys=True))
    file.close()

def greenSpaces(filepath_square):

    print(filepath_square[-40:])

    file = open(filepath_square,'r')
    square = json.load(file)
    file.close()

    square_center = square["properties"]["center"]
    square_region_code = square["properties"]["region"]

    greens = []

    # iterate over all communes, but check first distance to commune and
    # skip if its too far away:
    greenspaces = []
    for commune_name in COMMUNES_NAME_SLUG:
        commune_code = COMMUNE_NAME_SLUG_TO_CODE[commune_name]
        if (commune_code >= square_region_code*1000 and
            commune_code < (square_region_code+1)*1000):
            commune = loadCommune(commune_name)
            commune_polygons = getPolygonCoordinates(commune)
            dist = 0
            for cp in commune_polygons:
                dist += pointToPolygonDistance(square_center,cp)
            dist /= len(commune_polygons)
            if dist > 0.01: continue

            print(commune_name)

            greenspaces += loadGreenspaces(commune_name)

    for greenspace in greenspaces:
        greenspace_polygons = getPolygonCoordinates(greenspace)
        dist = 0
        for gp in greenspace_polygons:
            dist += pointToPolygonDistance(square_center,gp)
        dist = dist/len(greenspace_polygons)

        if dist > 0.01:
            continue

        area = greenspace["properties"]["area"]
        greens.append([area,dist])

    square['properties']['greenspace'] = greens

    file = open(filepath_square,'w')
    file.write(geojson.dumps(square, sort_keys=True))
    file.close()


path = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile/manzanas/json/metropolitana-de-santiago/'

#files = glob.glob(path+'*')
#for file in files:
#    addCoordinates(file)

# Get all relevant green spaces
for commune_name in COMMUNES_NAME_SLUG:
    if (COMMUNE_NAME_SLUG_TO_CODE[commune_name] >= 13000 and
        COMMUNE_NAME_SLUG_TO_CODE[commune_name] <  14000):
       files = glob.glob(path+'{}*'.format(commune_name))
       for file in files:
           greenSpaces(file)
