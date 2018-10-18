#!/usr/bin/env python
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
from globals import *
from tools import *


def communes_shape_to_json(source='INE2016',simplify=0,convert=0,translate=0,verbose=0):

    if source == 'INE2016':
        filepath_in = sorted(glob.glob(GEO_DATA_PATH+
            '/sources/INE_CartografiaPrecenso2016/R*/Comuna.shp'))
        filepath_out = [GEO_DATA_PATH+
            '/comunas/shp/comunas_'+slugify(REGION_CODE__NAME[i])+'.shp'
            for i in REGION_CODE__NAME.keys()]

    if simplify:
        shape_simplify(filepath_in,filepath_out,ref=0.0001,verbose=verbose)

    if source == 'INE2016':
        filepath_in = [GEO_DATA_PATH+'/comunas/shp/comunas_'+
            slugify(REGION_CODE__NAME[i+1])+'.shp'
            for i in range(len(REGION_CODE__NAME))]
        filepath_out = [GEO_DATA_PATH+'/comunas/json/comunas_'+
            slugify(REGION_CODE__NAME[i+1])+'.geojson'
            for i in range(len(REGION_CODE__NAME))]

    if convert:
        shape_to_json(filepath_in,filepath_out,verbose=verbose)

    if translate:
        for filepath in filepath_out:

            if verbose:
                print(filepath[filepath.rfind('/'):])

            file = open(filepath,'r')
            geojson_i = json.load(file)
            file.close()

            '''
            if os.path.isfile(filepath):
                os.remove(filepath)
            '''

            for feature in geojson_i['features']:
                geojson_o = {}
                geojson_o['properties'] = {}
                name = feature['properties']['NOM_COMUNA']
                provincia = int(feature['properties']['PROVINCIA'])
                code = int(feature['properties']['COMUNA'])
                region = int(feature['properties']['REGION'])
                geojson_o['properties']['name'] = name.title()
                geojson_o['properties']['code'] = code
                geojson_o['properties']['region'] = region
                geojson_o['properties']['province'] = provincia
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}

                file = open('../data/geo/chile/comunas/json/'+slugify(name)+'.geojson','w')
                file.write(geojson.dumps(geojson_o, sort_keys=True))
                file.write('\n')

communes_shape_to_json(simplify=0,convert=1,translate=1,verbose=1)
