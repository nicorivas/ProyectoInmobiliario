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

    def convert(filepath_in,filepath_out):
        if not isinstance(filepath_in, list):
            filepath_in = [filepath_in]
        if not isinstance(filepath_out, list):
            filepath_out = [filepath_out]

        print('Converting to GeoJSON')
        for i, fpi in enumerate(filepath_in):
            if os.path.isfile(filepath_out[i]):
                os.remove(filepath_out[i])
            print(filepath_in[i])
            cmd_convert = ['ogr2ogr',
                '-f','GeoJSON',
                '-t_srs','EPSG:4326',
                '{}'.format(filepath_out[i]),
                '{}'.format(filepath_in[i])]
            call(cmd_convert)

            file_json = open(filepath_out[i],'r')
            geojson_i = json.load(file_json)
            file_json.close()
            if os.path.isfile(filepath_out[i]):
                os.remove(filepath_out[i])
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

    # Simplify geometry of shape files
    base_dir = '/Users/nico/Code/ProyectoInmobiliario/data/geo/chile'

    if source == 'INE2016':
        #for i in range(len(code_to_region_name)):
        filepath_in = sorted(glob.glob(base_dir+
            '/sources/INE_CartografiaPrecenso2016/R*/Comuna.shp'))
        filepath_out = [base_dir+
            '/comunas/shp/comunas_'+slugify(code_to_region_name[i])+'.shp'
            for i in code_to_region_name.keys()]

    if do_simplify:
        simplify(filepath_in,filepath_out,ref=0.0001)

    if source == 'INE2016':
        filepath_in = ['../data/geo/chile/comunas/shp/comunas_'+
            slugify(code_to_region_name[i+1])+'.shp'
            for i in range(len(code_to_region_name))]
        filepath_out = ['../data/geo/chile/comunas/json/comunas_'+
            slugify(code_to_region_name[i+1])+'.geojson'
            for i in range(len(code_to_region_name))]

    # Convert shape files to GeoJSON (and convert coordinate system)
    if do_convert:
        convert(filepath_in,filepath_out)

with_ogr2ogr(do_simplify=1,do_convert=1)
