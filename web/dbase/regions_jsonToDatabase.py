#!/usr/bin/env python
import sys
import geojson
import json
import glob
from sqlalchemy import create_engine

sys.path.append('.')
from globals import *
from tools import *

engine = dbase_create_engine()

path_in = GEO_DATA_PATH+'/regiones/json/'
regions = glob.glob(path_in+'*.geojson')

for region in regions:
    file_in = open('{}'.format(region),'r')
    str = file_in.read()
    region_geojson = geojson.loads(str)
    region_geojson_geometry = region_geojson['geometry']
    if region_geojson_geometry['type'] == "Polygon":
        region_geojson_geometry['type'] = "MultiPolygon"
        region_geojson_geometry['coordinates'] = [region_geojson_geometry['coordinates']]
    region_geojson_geometry_str = json.dumps(region_geojson_geometry)
    engine.execute('INSERT INTO region_region (name, code, iso, mpoly) VALUES (%s,%s,%s,ST_GeomFromGeoJSON(%s));',
        (region_geojson['properties']['name'],
         region_geojson['properties']['code'],
         region_geojson['properties']['iso'],
         region_geojson_geometry_str))
