#!/usr/bin/env python
import os
import sys
import glob # getting files with wildcards
import shapefile # read shapes
import json # read/write json
import geojson # read/write geojson
from slugify import slugify # for nice filenames

sys.path.append('.')
from globals import *
from tools import *

def regions_shape_to_json(source='INE2016',simplify=0,convert=0,translate=0,verbose=0):

    if source == 'INE2016':
        filepath_in = sorted(glob.glob(GEO_DATA_PATH+'/sources/INE_CartografiaPrecenso2016/*/Region.shp'))
        filepath_out = [GEO_DATA_PATH+'/regiones/shp/'+slugify(REGION_CODE__NAME[i+1])+'.shp' for i in range(len(REGION_CODE__NAME))]
    elif source == 'IGM':
        filepath_in = GEO_DATA_PATH+'/sources/Division_Regional/division_regional.shp'
        filepath_out = GEO_DATA_PATH+'/regiones/shp/regiones_{}.shp'.format(source)

    if simplify:
        shape_simplify(filepath_in,filepath_out,ref=0.001,verbose=verbose)

    if source == 'INE2016':
        filepath_in = ['../data/geo/chile/regiones/shp/'+slugify(REGION_CODE__NAME[i+1])+'.shp' for i in range(len(REGION_CODE__NAME))]
        filepath_out = ['../data/geo/chile/regiones/json/'+slugify(REGION_CODE__NAME[i+1])+'.geojson' for i in range(len(REGION_CODE__NAME))]
    elif source == 'IGM':
        path_in = '../data/geo/chile/regiones/shp/'
        path_out = '../data/geo/chile/regiones/json/'

    if convert:
        shape_to_json(filepath_in,filepath_out,verbose=verbose)

    if translate:
        for i, filepath in enumerate(filepath_out):

            file = open(filepath,'r')
            geojson_i = json.load(file)
            file.close()

            geojson_o = {}
            for feature in geojson_i['features']:
                geojson_o['properties'] = {}
                region_name = REGION_CODE__NAME[i+1]
                geojson_o['properties']['name'] = region_name
                geojson_o['properties']['code'] = i+1
                geojson_o['properties']['iso'] = REGION_NAME__ISO_CODE[region_name]
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}
                #geojson_o['geometry']['crs'] = geojson_i['crs']
                geojson_o['type'] = "Feature"

            file = open(filepath,'w')
            file.write(geojson.dumps(geojson_o, sort_keys=True))
            file.write('\n')

regions_shape_to_json(simplify=0,convert=1,translate=1,verbose=1)
