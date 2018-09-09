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

def with_ogr2ogr(source='INE2016',do_simplify=1,do_convert=1):

    def simplify(filepath_in,filepath_out,ref=1000):
        if not isinstance(filepath_in, list):
            filepath_in = [filepath_in]
        if not isinstance(filepath_out, list):
            filepath_out = [filepath_out]

        print('Simplifying commune geometries ({}):'.format(ref))
        for i, fpi in enumerate(filepath_in):
            print(fpi)
            cmd_simplify = ['ogr2ogr',
                '{}'.format(filepath_out[i]),
                '{}'.format(filepath_in[i]),
                '-simplify',str(ref)]
            call(cmd_simplify)

    def convert(filepath_in,filepath_out, observe=0):

        if not isinstance(filepath_in, list):
            filepath_in = [filepath_in]
        if not isinstance(filepath_out, list):
            filepath_out = [filepath_out]

        print('Converting to GeoJSON')
        for i, fpi in enumerate(filepath_in):

            print(filepath_in[i])

            # Remove output if its already there
            if os.path.isfile(filepath_out[i]):
                os.remove(filepath_out[i])

            # All the magic is done by ogr2ogr
            cmd_convert = ['ogr2ogr',
                '-f','GeoJSON',
                '-t_srs','EPSG:4326',
                '{}'.format(filepath_out[i]),
                '{}'.format(filepath_in[i])]
            call(cmd_convert)

            # We already have a GeoJSON file, we now check and modify its
            # properties
            file_json = open(filepath_out[i],'r')
            geojson_i = json.load(file_json)
            file_json.close()

            if observe:
                print(geojson_i.keys())
                print(geojson_i['type'])
                print(geojson_i['name'])
                print(geojson_i['crs'])
                print(geojson_i['features'][0])
                exit(0)

            for i, feature in enumerate(geojson_i['features']):
                geojson_o = {}
                geojson_o['properties'] = {}
                region = int(feature['properties']['REGION'])
                provincia = int(feature['properties']['PROVINCIA'])
                comuna = int(feature['properties']['COMUNA'])
                geojson_o['properties']['region'] = region
                geojson_o['properties']['province'] = provincia
                geojson_o['properties']['commune'] = comuna
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}

                path = '../data/geo/chile/areasverde/json/{}/'.format(slugify(code_to_region_name[region]))
                if not os.path.exists(path):
                    os.makedirs(path)
                file = open(path+'{}_{}.geojson'.format(slugify(code_to_commune_name[comuna]),i),'w')
                file.write(geojson.dumps(geojson_o, sort_keys=True))
                file.write('\n')

    # Simplify geometry of shape files
    base_dir = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile'

    if source == 'INE2016':
        #for i in range(len(code_to_region_name)):
        filepath_in = sorted(glob.glob(base_dir+
            '/sources/INE_CartografiaPrecenso2016/R*/Area_Verde.shp'))
        filepath_out = [base_dir+
            '/areasverde/shp/areasverde_'+slugify(code_to_region_name[i])+'.shp'
            for i in code_to_region_name.keys()]

    if do_simplify:
        simplify(filepath_in,filepath_out,ref=0.000000001)

    if source == 'INE2016':
        filepath_in = ['../data/geo/chile/areasverde/shp/areasverde_'+
            slugify(code_to_region_name[i+1])+'.shp'
            for i in range(len(code_to_region_name))]
        filepath_out = ['../data/geo/chile/areasverde/json/areasverde_'+
            slugify(code_to_region_name[i+1])+'.geojson'
            for i in range(len(code_to_region_name))]

    # Convert shape files to GeoJSON (and convert coordinate system)
    if do_convert:
        convert(filepath_in,filepath_out)

with_ogr2ogr(do_simplify=1,do_convert=1)

'''
f = open('regiones-provincias-comunas.json','r')
j = json.load(f)
d = {}
for region in j:
    for provincia in region['provincias']:
        for comuna in provincia['comunas']:
            d[comuna['name']] = int(comuna['code'])

f.close()
'''
