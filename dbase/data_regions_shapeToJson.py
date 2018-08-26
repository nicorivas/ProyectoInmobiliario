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
from data_globals.py import *

# These shall be the official names, used everywhere.

def reg_region_name(record):
    # Some region names are encrypted in a strange way, so regularize tu utf-8

    region_name = None
    if type(record) == bytes:
        region_name = u"{}".format(record.decode(encoding='windows-1252'))
    else:
        region_name = (u"{}".format(record))
    region_name = region_name.strip()

    # Some strange data has no name
    if len(region_name) == 0:
        return None

    # Regularize names of regions (WTF)
    if region_name.find('Región del') > -1:
        region_name = region_name[11:]
    if region_name.find('Región de') > -1:
        region_name = region_name[10:]
    if region_name.find('Región') > -1:
        region_name = region_name[7:]
    if region_name == "Libertador Bernardo O'Higgins":
        region_name = "Libertador General Bernardo O'Higgins"
    if region_name == "Aysén del Gral.Ibañez del Campo":
        region_name = "Aysén del General Carlos Ibáñez del Campo"
    if region_name == "Bío-Bío":
        region_name = "Biobío"
    if region_name == 'Zona sin demarcar':
        return None
    return region_name

def with_python():

    '''
    This script converts regions 'shape' files into 'geojson', of the regions of
    Chile. The data of the regions of Chile is shitty, so it is formatted and
    standarized
    '''

    path_in = '../data/geo/chile/regiones/raw/'
    path_out = '../data/geo/chile/regiones/json/'
    sf = shapefile.Reader("{}division_regional".format(path_in))
    shapes = sf.shapes()
    fields = sf.fields

    for shapeRecord in sf.iterShapeRecords():

        region_name = reg_region_name(shapeRecord.record[0])

        region_code = int(shapeRecord.record[4])

        region_surface = float(shapeRecord.record[5])

        region_population = int(shapeRecord.record[7])

        print(fields)

        properties = {
            'name':region_name,
            'id':region_code,
            'iso':iso_code[region_name],
            'surface':region_surface,
            'population':region_population}

        feature = geojson.Feature(
            geometry=shapeRecord.shape.__geo_interface__,
            properties=properties)

        file = open('{}{}.geojson'.format(path_out,slugify(region_name)),'w')

        file.write(geojson.dumps(feature, sort_keys=True))

def with_ogr2ogr(source='INE2016',do_simplify=1,do_convert=1):

    def simplify(filepath_in,filepath_out,ref=1000):
        if not isinstance(filepath_in, collections.Iterable):
            filepath_in = [filepath_in]
        if not isinstance(filepath_out, collections.Iterable):
            filepath_out = [filepath_out]
        print('Simplifying region geometries ({}):'.format(ref))
        for i, fpi in enumerate(filepath_in):
            print(filepath_in[i])
            cmd_simplify = ['ogr2ogr',
                '{}'.format(filepath_out[i]),
                '{}'.format(filepath_in[i]),
                '-simplify',str(ref)]
            call(cmd_simplify)

    def convert(filepath_in,filepath_out):
        if not isinstance(filepath_in, collections.Iterable):
            filepath_in = [filepath_in]
        if not isinstance(filepath_out, collections.Iterable):
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
            geojson_o = {}
            for feature in geojson_i['features']:
                geojson_o['properties'] = {}
                region_name = code_to_region_name[i+1]
                geojson_o['properties']['name'] = region_name
                geojson_o['properties']['code'] = i+1
                geojson_o['properties']['iso'] = region_name_to_iso_code[region_name]
                geojson_o['geometry'] = feature['geometry']
                geojson_o['geometry']['crs'] = {"type":"name","properties":{"name":"EPSG:4326"}}
                #geojson_o['geometry']['crs'] = geojson_i['crs']
                geojson_o['type'] = "Feature"

            file = open(filepath_out[i],'w')
            file.write(geojson.dumps(geojson_o, sort_keys=True))
            file.write('\n')

    # Simplify geometry of shape files
    base_dir = '../data/geo/chile'

    if source == 'INE2016':
        filepath_in = sorted(glob.glob(base_dir+'/sources/INE_CartografiaPrecenso2016/*/Region.shp'))
        filepath_out = [base_dir+'/regiones/shp/'+slugify(code_to_region_name[i+1])+'.shp' for i in range(len(code_to_region_name))]
    elif source == 'IGM':
        filepath_in = base_dir+'/sources/Division_Regional/division_regional.shp'
        filepath_out = base_dir+'/regiones/shp/regiones_{}.shp'.format(source)

    if do_simplify:
        simplify(filepath_in,filepath_out,ref=0.001)

    if source == 'INE2016':
        filepath_in = ['../data/geo/chile/regiones/shp/'+slugify(code_to_region_name[i+1])+'.shp' for i in range(len(code_to_region_name))]
        filepath_out = ['../data/geo/chile/regiones/json/'+slugify(code_to_region_name[i+1])+'.geojson' for i in range(len(code_to_region_name))]
    elif source == 'IGM':
        path_in = '../data/geo/chile/regiones/shp/'
        path_out = '../data/geo/chile/regiones/json/'

    # Convert shape files to GeoJSON (and convert coordinate system)
    if do_convert:
        convert(filepath_in,filepath_out)

with_ogr2ogr(do_simplify=1,do_convert=1)
