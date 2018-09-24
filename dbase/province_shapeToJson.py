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

def provinces_shape_to_json(source='INE2016',simplify=0,convert=0,translate=0,verbose=0):

    if source == 'INE2016':
        filepath_in = sorted(glob.glob(GEO_DATA_PATH+
            '/sources/INE_CartografiaPrecenso2016/R*/Provincia.shp'))
        filepath_out = [GEO_DATA_PATH+
            '/provincias/shp/provincias_'+slugify(REGION_CODE__NAME[i])+'.shp'
            for i in REGION_CODE__NAME.keys()]
    if simplify:
        shape_simplify(filepath_in,filepath_out,ref=0.001,verbose=verbose)

    if source == 'INE2016':
        filepath_in = ['../data/geo/chile/provincias/shp/provincias_'+
            slugify(REGION_CODE__NAME[i+1])+'.shp'
            for i in range(len(REGION_CODE__NAME))]
        filepath_out = ['../data/geo/chile/provincias/json/provincias_'+
            slugify(REGION_CODE__NAME[i+1])+'.geojson'
            for i in range(len(REGION_CODE__NAME))]

    if convert:
        shape_to_json(filepath_in,filepath_out,verbose=verbose)

    if translate:
        for i, filepath in enumerate(filepath_out):

            if verbose:
                print(filepath[filepath.rfind('/'):])

            file = open(filepath,'r')
            geojson_i = json.load(file)
            file.close()

            if os.path.isfile(filepath):
                os.remove(filepath)

            for feature in geojson_i['features']:
                geojson_o = {}
                geojson_o['properties'] = {}
                name = feature['properties']['NOM_PROVIN']
                code = int(feature['properties']['PROVINCIA'])
                region = i+1
                geojson_o['properties']['name'] = name.title()
                geojson_o['properties']['code'] = code
                geojson_o['properties']['region'] = region
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}

                file = open(GEO_DATA_PATH+'/provincias/json/'+slugify(name)+'.geojson','w')
                file.write(geojson.dumps(geojson_o, sort_keys=True))
                file.write('\n')

provinces_shape_to_json(simplify=0,convert=1,translate=1,verbose=1)
