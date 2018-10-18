#!/usr/bin/env python
import sys
import geojson
import json
import glob
from sqlalchemy import func

sys.path.append('.')
from globals import *
from tools import *

verbose = 1
delete = 1

# Establish connection with database
sql_engine, sql_metadata, sql_connection = dbase_setup()
# Get table
sql_square_table = sql_metadata.tables['square_square']
# Delete all elements of table?
if delete:
    if verbose:
        print("Deleting all values in table 'square_square'")
    sql_engine.execute('delete from square_square')


basepath = GEO_DATA_PATH+'/manzanas/json'
#regions = REGION_NAMES_SLUG
regions = [REGION_CODE__NAME_SLUG[13]]

for region in regions:
    if verbose:
        print(region)
    # All geojson files to upload
    filepath_squares = glob.glob(basepath+'/'+region+'/*.geojson')
    # List of dictionaries to insert. We do it with a list instead of an insert
    # for every square as it is much faster (100x) to bulk insert.
    values = []
    for filepath_square in filepath_squares:
        if verbose == 2:
            print(filepath_square)
        # Load geojson from file to dictionary
        file = open('{}'.format(filepath_square),'r')
        square_geojson = geojson.loads(file.read())
        # Get relevant variables. Convert all geometry types to multipolygon
        # As it is easier to have just one case in the database.
        square_geojson_geometry = square_geojson['geometry']
        if square_geojson_geometry['type'] == "Polygon":
            square_geojson_geometry['type'] = "MultiPolygon"
            square_geojson_geometry['coordinates'] = [square_geojson_geometry['coordinates']]
        square_geojson_geometry_str = json.dumps(square_geojson_geometry)
        # Append dictionary of variables to values. Some names change!
        values.append({
            'code':square_geojson['properties']['code'],
            'region_id':square_geojson['properties']['region'],
            'province_id':square_geojson['properties']['province'],
            'commune_id':square_geojson['properties']['commune'],
            'mpoly':func.ST_GeomFromGeoJSON(square_geojson_geometry_str)})
    # Do the SQL
    if verbose:
        print('Inserting data (SQL)')
    stmt = sql_square_table.insert().values(values)
    sql_connection.execute(stmt)
