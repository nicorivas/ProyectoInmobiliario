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

def squares_shape_to_json(source='INE2016',simplify=0,convert=0,translate=0,verbose=0):

    regiones = [13]

    if source == 'INE2016':
        filepath_in = sorted([GEO_DATA_PATH+
            '/sources/INE_CartografiaPrecenso2016/R{:02d}/Manzana_Precensal.shp'.format(i)
            for i in regiones])
        filepath_out = [GEO_DATA_PATH+
            '/manzanas/shp/manzanas_'+slugify(REGION_CODE__NAME[i])+'.shp'
            for i in regiones]

    if simplify:
        shape_simplify(filepath_in,filepath_out,ref=0.00001,verbose=verbose)

    if source == 'INE2016':
        filepath_in = [GEO_DATA_PATH+'/manzanas/shp/manzanas_'+
            slugify(REGION_CODE__NAME[i])+'.shp'
            for i in regiones]
        filepath_out = [GEO_DATA_PATH+'/manzanas/json/manzanas_'+
            slugify(REGION_CODE__NAME[i])+'.geojson'
            for i in regiones]
            
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
                region = int(feature['properties']['REGION'])
                provincia = int(feature['properties']['PROVINCIA'])
                comuna = int(feature['properties']['COMUNA'])
                code = int(feature['properties']['MANZENT'])
                geojson_o['properties']['region'] = region
                geojson_o['properties']['province'] = provincia
                geojson_o['properties']['commune'] = comuna
                geojson_o['properties']['code'] = code
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}

                path = GEO_DATA_PATH+'/manzanas/json/{}/'.format(slugify(REGION_CODE__NAME[region]))
                if not os.path.exists(path):
                    os.makedirs(path)

                if not comuna in COMMUNE_CODE__NAME.keys():
                    print(region)
                    print(province)
                    print(comuna)
                    print(code)

                file = open(path+'{}_{}.geojson'.format(slugify(COMMUNE_CODE__NAME[comuna]),code),'w')
                file.write(geojson.dumps(geojson_o, sort_keys=True))
                file.write('\n')
                file.close()

squares_shape_to_json(simplify=0,convert=0,translate=1,verbose=1)
