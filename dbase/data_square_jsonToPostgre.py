#!/usr/bin/env python
from sqlalchemy import create_engine # for pandas dataframes to postgre
import geojson
import json
import glob
#from geoalchemy.shape import from_shape

engine = create_engine('postgresql://nico:@localhost:5432/data', echo=True)

path_in = '../data/geo/chile/manzanas/json/'

squares = glob.glob(path_in+'*.geojson')
for square in squares:
    file_in = open('{}'.format(square),'r')
    str = file_in.read()
    square_geojson = geojson.loads(str)
    square_geojson_geometry = square_geojson['geometry']
    if square_geojson_geometry['type'] == "Polygon":
        square_geojson_geometry['type'] = "MultiPolygon"
        square_geojson_geometry['coordinates'] = [square_geojson_geometry['coordinates']]
    square_geojson_geometry_str = json.dumps(square_geojson_geometry)
    engine.execute('INSERT INTO square_square (code, region_id, province_id, commune_id, mpoly) VALUES (%s,%s,%s,%s,ST_GeomFromGeoJSON(%s));',(
         square_geojson['properties']['code'],
         square_geojson['properties']['region'],
         square_geojson['properties']['province'],
         square_geojson['properties']['commune'],
         square_geojson_geometry_str))
