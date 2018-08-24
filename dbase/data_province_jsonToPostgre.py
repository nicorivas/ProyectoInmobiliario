#!/usr/bin/env python
from sqlalchemy import create_engine # for pandas dataframes to postgre
import geojson
import json
import glob
#from geoalchemy.shape import from_shape

engine = create_engine('postgresql://nico:@localhost:5432/data', echo=True)

path_in = '../data/geo/chile/provincias/json/'

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
    engine.execute('INSERT INTO province_province (name, code, region_id, mpoly) VALUES (%s,%s,%s,ST_GeomFromGeoJSON(%s));',
        (region_geojson['properties']['name'],
         region_geojson['properties']['code'],
         region_geojson['properties']['region'],
         region_geojson_geometry_str))